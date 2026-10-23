---
author: fzipi
categories:
  - Blog
date: '2026-11-10T09:00:00-03:00'
tags:
  - CRS-Logging
  - Logging
  - Tutorial
  - ModSecurity
images:
  - /images/2026/11/crs-logging-kibana-dashboard.png
title: 'Logging with OWASP CRS, Part 2: A CRS Dashboard on the Elastic Stack'
slug: 'crs-logging-part-2-elastic-stack'
series: crs-logging
draft: true
---

{{< series-link part="1" >}}Part 1{{< /series-link >}} covered what ModSecurity and CRS write to disk and what to look for in it. This post turns that into a dashboard on the Elastic Stack: Logstash tails the JSON audit log, flattens it into fields that are easy to aggregate, Elasticsearch stores it, and Kibana shows it. Everything runs from one Docker Compose file, and the dashboard is imported for you.

{{< figure src="/images/2026/11/crs-logging-kibana-dashboard.png" caption="The CRS overview dashboard in Kibana, after a few hundred requests from the traffic generator." >}}

## Run it

You need Docker with Compose and about 4 GB of free memory (Elasticsearch, Kibana and Logstash are all JVM or Node processes with opinions about heap). Download {{< resource-link text="crs-logging-elk.zip" file="crs-logging-elk.zip" >}} (it is also at the end of this post), unpack it, and start the stack:

```bash
unzip crs-logging-elk.zip
cd crs-logging/elk
docker compose up -d
```

The first start takes a minute or two: Elasticsearch has to come up before Logstash and Kibana start, and a one-shot container then imports the dashboard. When `docker compose ps -a` shows `kibana-setup` as exited with code 0 (or `docker compose wait kibana-setup` returns), generate some traffic:

```bash
../generate-traffic.sh 300
```

Then open <http://localhost:5601/app/dashboards> and pick "OWASP CRS - ModSecurity overview". The WAF itself answers on <http://localhost:8080>; point your own scanner at it if you prefer real traffic. `docker compose down -v` throws everything away.

Every port is published on `127.0.0.1` only, since nothing in this stack asks for a password. To open it from another machine, set `BIND_ADDR` to an address you trust, such as your Tailscale address, and pass the same address to the traffic generator: `BIND_ADDR=100.64.0.10 docker compose up -d`, then `TARGET=http://100.64.0.10:8080 ../generate-traffic.sh 300`.

The archive keeps the folder layout the stack expects: the compose file mounts `../waf/`, and you run `../generate-traffic.sh` from the `elk` folder. Here are the same files one by one; the rest of this post walks through them.

{{< resources title="Elastic Stack files" pattern="^elk/" expanded="true" >}}

{{< resources title="Shared WAF configuration and traffic generator" pattern="^(waf/|generate-traffic)" expanded="true" >}}

## The stack

```yaml
# elk/compose.yaml (abridged; the full file is attached above)
name: crs-elk

services:
  waf:
    image: owasp/modsecurity-crs:4.30.0-nginx-alpine-202610180210
    ports:
      - "${BIND_ADDR:-127.0.0.1}:${WAF_PORT:-8080}:8080"
    environment:
      BACKEND: http://backend:80
      PORT: "8080"
      BLOCKING_PARANOIA: "1"
      DETECTION_PARANOIA: "2"
      MODSEC_AUDIT_ENGINE: RelevantOnly
      MODSEC_AUDIT_LOG_FORMAT: JSON
      MODSEC_AUDIT_LOG_TYPE: Serial
      MODSEC_AUDIT_LOG: /var/log/modsecurity/audit/modsec_audit.log
      MODSEC_AUDIT_LOG_PARTS: ABIJFHZ   # no response body
    volumes:
      - waf-logs:/var/log/modsecurity/audit
      - ../waf/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf:/etc/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf:ro
      - ../waf/nginx-realip.conf:/etc/nginx/conf.d/realip.conf:ro

  backend:
    image: traefik/whoami:v1.12.0

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:9.5.5
    environment:
      discovery.type: single-node
      xpack.security.enabled: "false"
      xpack.ml.enabled: "false"
      cluster.routing.allocation.disk.threshold_enabled: "false"
      ES_JAVA_OPTS: -Xms1g -Xmx1g
    volumes:
      - es-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:9.5.5
    environment:
      ELASTICSEARCH_HOSTS: http://elasticsearch:9200
    ports:
      - "${BIND_ADDR:-127.0.0.1}:5601:5601"

  logstash:
    image: docker.elastic.co/logstash/logstash:9.5.5
    environment:
      LS_JAVA_OPTS: -Xms512m -Xmx512m
      PIPELINE_ECS_COMPATIBILITY: disabled
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline:ro
      - ./logstash/scripts:/usr/share/logstash/scripts:ro
      - ./logstash/templates:/usr/share/logstash/templates:ro
      - waf-logs:/var/log/modsecurity/audit:ro

  kibana-setup:
    image: curlimages/curl:8.23.0
    volumes:
      - ./kibana:/kibana:ro
    command: >
      sh -c 'curl -sf -X POST "http://kibana:5601/api/saved_objects/_import?overwrite=true"
      -H "kbn-xsrf: true" --form file=@/kibana/crs-dashboard.ndjson'

volumes:
  waf-logs:
  es-data:
  logstash-data:
```

A few things worth pointing out.

**The WAF** is the official CRS container, configured exactly as the checklist in Part 1 says: audit log in JSON, one line per transaction, written to a named volume that Logstash mounts read-only. It blocks at paranoia level 1 and evaluates level 2, and it gets the two files from the shared `waf/` directory: the phase 5 summary rule and the realip snippet that makes ModSecurity log the client address from `X-Forwarded-For`. The ELK stack does not need the error log; everything it needs is in the audit log, so NGINX keeps logging errors to `stderr` where `docker compose logs waf` can show them.

**The volume** is the handoff. The container runs NGINX as an unprivileged user and `/var/log/modsecurity/audit` is the one log directory it owns, which is why the audit log lives there. Any file-based shipper (Filebeat, Elastic Agent, Fluent Bit, Vector) can take Logstash's place by mounting the same volume.

**Elasticsearch and Kibana** run with security disabled, machine learning off, a 1 GB heap, and disk watermarks ignored. That last one keeps the lab working on a laptop with a nearly full disk; it is not something you want in production, and neither is the lack of authentication. We only run one Elasticsearch node, so the index template sets zero replicas.

**The setup container** calls Kibana's saved objects import API once Kibana reports healthy. That is the whole provisioning story: one NDJSON file, one `curl`.

## The Logstash pipeline

The pipeline is short because the audit log is already JSON. Logstash reads the file, parses each line, calls a Ruby script that adds the flat fields, and writes to a daily index.

```ruby
# elk/logstash/pipeline/modsec-audit.conf
input {
  file {
    path => "/var/log/modsecurity/audit/modsec_audit.log"
    start_position => "beginning"
    sincedb_path => "/usr/share/logstash/data/sincedb-modsec-audit"
    codec => "json"
    tags => ["modsec-audit"]
  }
}

filter {
  if "_jsonparsefailure" in [tags] {
    drop { }
  }

  # ctime format, local time of the WAF process; the container runs in UTC
  date {
    match => ["[transaction][time_stamp]", "EEE MMM dd HH:mm:ss yyyy", "EEE MMM  d HH:mm:ss yyyy"]
    timezone => "UTC"
    target => "@timestamp"
  }

  ruby {
    path => "/usr/share/logstash/scripts/modsec_flatten.rb"
  }

  mutate {
    remove_field => ["@version", "host", "path", "event"]
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "modsec-audit-%{+YYYY.MM.dd}"
    data_stream => false
    manage_template => true
    template => "/usr/share/logstash/templates/modsec-audit.json"
    template_name => "modsec-audit"
    template_overwrite => true
    ecs_compatibility => disabled
  }
}
```

Two patterns in the `date` filter because `ctime` pads single-digit days with a space (`Oct  2`). If your WAF runs with a time zone set, change `timezone` accordingly; ModSecurity does not write one.

### Flattening the record

Elasticsearch can index the nested `transaction` object as it is, but it is awkward to build charts on: `messages` is an array of objects, the rule tags are two levels down, and the fields you want to filter on are mixed with the ones you only want to read. The {{< resource-link text="Ruby script" file="elk/logstash/scripts/modsec_flatten.rb" >}} walks the record once and adds:

| Field | From | Used for |
|---|---|---|
| `modsec.blocked` | `transaction.is_interrupted` | blocked vs. logged only |
| `modsec.unique_id` | `transaction.unique_id` | correlating with the error log |
| `client.ip`, `http.request.method`, `url.path`, `url.query`, `http.response.status_code`, `user_agent.original` | the request and response blocks | the usual slicing |
| `modsec.rule.ids`, `modsec.rule.messages`, `modsec.rule.severities`, `modsec.rule.tags`, `modsec.rule.files` | each entry of `messages` | top rules, severity |
| `modsec.rule.count`, `modsec.rule.top_severity` | derived | headline numbers |
| `modsec.attack` | the `attack-*` tags, prefix removed | attack categories |
| `modsec.paranoia_level` | the `paranoia-level/N` tags | which PL the matches belong to |
| `modsec.anomaly.*` | the summary rule's message | inbound and outbound scores, per-PL breakdown, per-category scores, thresholds |
| `modsec.paranoia.blocking`, `modsec.paranoia.detection` | the summary rule's message | what the WAF was configured for at the time |
| `modsec.matches` | each entry of `messages` | one object per rule match, stored but not indexed, for reading |

The arrays are the trick that makes a single document per transaction work in Kibana: a terms aggregation on `modsec.rule.ids` counts each transaction once per rule that matched, which is exactly what "top rules" means. The script leaves the blocking evaluation rules (949110, 959100) and the correlation rules out of those arrays, otherwise 949110 would be the top rule on every dashboard, telling you nothing. They stay in `modsec.matches` for completeness.

The summary line from Part 1 is parsed with one regular expression into integers. If the summary rule is not installed, the script falls back to the "Total Score" in the 949110 message, so blocked transactions still get an `inbound_blocking` score; everything else stays empty, and the score panels will tell you so.

The script also removes `transaction.response.body`. The lab already leaves part `E` out of the audit log, so there is nothing to remove there, but you may point the pipeline at a WAF that logs it. The response body is either the 403 page or your application's answer to a request that was not blocked, and neither belongs in a log index.

### The index template

The {{< resource-link text="template" file="elk/logstash/templates/modsec-audit.json" >}} does three things. It maps the flat fields with the right types (`ip` for addresses, `keyword` for everything you aggregate on, `integer` for scores). It maps the request and response headers as `flattened`, so that arbitrary header names do not create new fields in the mapping. And it marks `transaction.messages`, `transaction.producer` and `modsec.matches` as not indexed: they are in the document for you to read in Discover, but they do not cost anything to store beyond the source. Logstash installs it as a composable index template on startup; Logstash 9 uses the `_index_template` API for that, which is why the file has the `template` wrapper.

## The dashboard

The dashboard, a data view and a saved Discover session are in {{< resource-link text="kibana/crs-dashboard.ndjson" file="elk/kibana/crs-dashboard.ndjson" >}}. Kibana's Lens panels are stored as rather verbose JSON, so instead of maintaining that by hand there is a small Python script, `build-dashboard.py`, that generates the file. If you want to add a panel, edit the script and run it again; if you prefer clicking, edit the dashboard in Kibana and export it from Stack Management.

What is on it, top to bottom, and which question from Part 1 each panel answers:

- **Transactions logged, blocked, rule matches, distinct clients.** The headline numbers. The ratio of blocked to logged tells you how much of what CRS sees it also stops.
- **Transactions over time, blocked vs. logged only.** Spikes are either an attack or a deploy that introduced a false positive. The split tells you which.
- **Attack categories.** A donut of the `attack-*` tags. The categories that never appear are the ones to double-check, as discussed in Part 1.
- **Top rules** and **most targeted paths**, each with a "blocked" column. The false positive signature is a rule with a high count on a path your users actually use; `911100` on `/api/profile/42` in the screenshot is the deliberate one from the traffic generator (a `PUT` against CRS's default method policy).
- **Top clients.** Scanners stand out. With the realip snippet in place these are the addresses from `X-Forwarded-For`, not the load balancer's.
- **Paranoia level of matched rules** and **highest severity per transaction.** The first shows how much of your signal comes from the level you are not enforcing yet.
- **Inbound anomaly score distribution.** One bar per score value at the detection paranoia level. A healthy site has a wall at 5 (one critical rule, blocked) and a tail; a site with a false positive problem has a hump at 2 or 3.
- **Highest inbound score per interval, blocking PL vs. detection PL.** The two lines from the summary rule. The gap between them is what raising the paranoia level would block.
- **Transactions.** The saved Discover session, newest first, with the columns that matter. Click a row to expand the full audit record, including every header and every matched rule.

The dashboard restores its own time range (last 24 hours) and refreshes every 30 seconds. Click on any value, a rule ID, a path, a client address, and Kibana adds it as a filter to every other panel, which is how most investigations go: start from a suspicious rule, narrow to a client, read the transactions.

## Adapting it

**Your own WAF instead of the lab one.** Any ModSecurity v3 producing a JSON audit log works; point the `file` input at it (or replace it with a Beats input and run Filebeat next to the WAF). ModSecurity v2 writes a different JSON layout and, more often, the native format; the Ruby script expects the v3 layout. Coraza's JSON audit log uses other field names (`transaction.id`, `transaction.timestamp`, `transaction.response.status`) and stores each rule match as its alert line (`messages[].error_message`) rather than as structured fields, so the script would have to parse those lines with regular expressions, which is what {{< series-link part="3" >}}Part 3{{< /series-link >}} does in Alloy.

**More than one WAF.** Add a field in the pipeline, for example from the file path or a Filebeat tag, and a filter control on the dashboard. The `transaction.server_id` field (a hash of the NGINX server name) is there too but is not friendly to read.

**Retention.** The index is daily, so an index lifecycle policy on `modsec-audit-*` is all you need. Audit records with request bodies are not small; a busy site at `RelevantOnly` can produce gigabytes a day, most of it from scanners.

**Alerting.** Kibana's rules can watch the same queries. The two we suggest to start with are "more than N blocked transactions from one client in five minutes" (a scanner, or a bot) and "a rule that never matched before matched more than N times in an hour" (a new false positive after a deploy, or a new campaign).

{{< series-link part="3" >}}Part 3{{< /series-link >}} swaps both halves: the WAF becomes Coraza, the same CRS release on a different engine, and the dashboard moves to Grafana and Loki, with a different and lighter approach: no document flattening at all, labels and regular expressions instead.

{{< series-nav >}}

## Download

Everything this post uses, in one archive. It unpacks to a `crs-logging/` folder with a short README.

{{< resources title="All files" pattern="[.]zip$" >}}

{{< related-pages "CRS-Logging" >}}
