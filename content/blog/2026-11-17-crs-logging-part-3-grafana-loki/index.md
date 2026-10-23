---
author: fzipi
categories:
  - Blog
date: '2026-11-17T09:00:00-03:00'
tags:
  - CRS-Logging
  - Logging
  - Tutorial
  - Coraza
images:
  - /images/2026/11/crs-logging-grafana-dashboard.png
title: 'Logging with OWASP CRS, Part 3: Coraza Logs on Grafana and Loki'
slug: 'crs-logging-part-3-grafana-loki'
series: crs-logging
draft: true
---

{{< series-link part="1" >}}Part 1{{< /series-link >}} explained what CRS logs and what to look for. {{< series-link part="2" >}}Part 2{{< /series-link >}} built a dashboard on the Elastic Stack for ModSecurity, by flattening its JSON audit log into fields. This post changes both halves. The WAF is [Coraza](https://coraza.io/), the OWASP WAF engine written in Go, running the same CRS release inside Caddy. The log platform is Grafana and Loki, which takes the opposite approach to Elasticsearch: no document model, no index template. Loki stores log lines as they are, with a handful of labels, and the dashboard extracts what it needs at query time. The whole stack fits in about a gigabyte of memory.

{{< figure src="/images/2026/11/crs-logging-grafana-dashboard.png" caption="The CRS overview dashboard in Grafana, fed by Coraza's logs through Loki." >}}

## Run it

Download {{< resource-link text="crs-logging-grafana-loki.zip" file="crs-logging-grafana-loki.zip" >}} (it is also at the end of this post), unpack it, start the stack and send it some traffic:

```bash
unzip crs-logging-grafana-loki.zip
cd crs-logging/grafana-loki
docker compose up -d
../generate-traffic.sh 300
```

Open <http://localhost:3000/d/crs-coraza-overview>. There is no login; Grafana is provisioned with anonymous admin access because this is a lab. The WAF answers on <http://localhost:8080> (set `WAF_PORT` if you want the Elastic stack from Part 2 running at the same time). `docker compose down -v` resets everything. All ports are published on `127.0.0.1` only; set `BIND_ADDR` to reach the stack from another machine, as described in Part 2.

The archive keeps the folder layout the stack expects: the compose file mounts `../waf/`, and you run `../generate-traffic.sh` from the `grafana-loki` folder. Here are the same files one by one:

{{< resources title="Coraza, Grafana and Loki files" pattern="^grafana-loki/" expanded="true" >}}

{{< resources title="Shared summary rule and traffic generator" pattern="^(waf/|generate-traffic)" expanded="true" >}}

## Coraza, CRS and Caddy

The CRS project publishes [Coraza images](https://github.com/coreruleset/coraza-crs-docker) next to the ModSecurity ones, with Caddy, NGINX and Apache variants. We use the Caddy one: Caddy runs [coraza-caddy](https://github.com/corazawaf/coraza-caddy), the most widely used Coraza integration, and the whole thing is a single Go binary. Like the ModSecurity image, it is configured through environment variables (`BLOCKING_PARANOIA`, `DETECTION_PARANOIA`, `CORAZA_AUDIT_*`), and the CRS rules are the same files, at the same version.

The logs are where it gets interesting. Coraza speaks the same rule language and writes alerts in the same bracketed format as ModSecurity, so almost everything in Part 1 applies. Here is a rule match as Coraza writes it:

```text
[client "203.0.113.77"] Coraza: Warning. SQL Injection Attack Detected via libinjection
  [file "/opt/coraza/owasp-crs/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf"] [line "10060"]
  [id "942100"] [rev ""] [msg "SQL Injection Attack Detected via libinjection"]
  [data "Matched Data: s&1c found within ARGS:id: 1' OR 1=1--"] [severity "critical"]
  [ver "OWASP_CRS/4.30.0"] [maturity "0"] [accuracy "0"] [tag "application-multi"]
  [tag "language-multi"] [tag "platform-multi"] [tag "attack-sqli"] [tag "paranoia-level/1"]
  [tag "OWASP_CRS"] [tag "OWASP_CRS/ATTACK-SQLI"] [tag "capec/1000/152/248/66"]
  [hostname ""] [uri "/?id=1%27%20OR%201=1--"] [unique_id "qRJvybmnRhuIaVTS"]
```

Compare it with the ModSecurity line in Part 1 and the differences are small but real:

| | ModSecurity v3 on NGINX (Part 2) | Coraza on Caddy (this post) |
|---|---|---|
| Where alerts go | NGINX error log, per-rule lines at `info` level | Caddy's JSON log, logger `http.handlers.waf`, as the `msg` field |
| Client address | trailing `client: 203.0.113.77,` added by NGINX | `[client "203.0.113.77"]` prefix |
| Request line | trailing `request: "GET /... HTTP/1.1"` | not included; use `[uri]` |
| `[uri]` | path only | path and query string |
| Severity | a number (`[severity "2"]`) | a word (`[severity "critical"]`) |
| Unique ID | `179269749060.964266` | `qRJvybmnRhuIaVTS` |
| CRS score report (980170) | never logged, see Part 1 | logged |
| `RelevantOnly` audit log | status matches, **or** a rule with `auditlog` matched | status matches, nothing else |
| Status of a blocked request in the audit log | 403 | 0 |

Two of those rows need action.

**The score report works.** Coraza logs CRS's own rule 980170, the `Anomaly Scores: (Inbound Scores: blocking=5, detection=25, ...)` line that ModSecurity v3 drops. We still install the summary rule from Part 1, so that both stacks produce the same `key=value` line and the same queries work on either, but if you run Coraza you can also rely on 980170.

**`RelevantOnly` means something narrower.** ModSecurity writes a transaction to the audit log when its status matches `SecAuditLogRelevantStatus` or when a rule that has `auditlog` matched. Coraza only looks at the status. A request that scored but was not blocked comes back 200, which does not match the default pattern, so it never reaches Coraza's audit log, and those are exactly the possible false positives you want to read. The fix is a tiny rule that turns the audit engine on for any transaction CRS gave points to:

```apache
SecRule TX:DETECTION_ANOMALY_SCORE "@gt 0" \
    "id:99902,\
    phase:5,\
    pass,\
    t:none,\
    nolog,\
    ctl:auditEngine=On"
```

It runs in phase 5, before Coraza decides whether to write the audit record, and only switches logging on for that one transaction. Clean requests stay out of the log, as before.

Coraza also leaves the response status at 0 for a transaction it interrupted, because Caddy writes the 403 after Coraza is done. The audit record's `is_interrupted` field is the reliable "blocked" flag.

## Two logs, two streams

Loki is a different kind of store from Elasticsearch. It indexes labels, not content, and its query language, LogQL, is built around grep-like filtering followed by extraction. It is very good at "show me the lines" and at counting lines by label. What it does not do well is unpack an array inside a JSON document: `| json` on an audit record gives you `messages_0_...`, `messages_1_...` and so on, which you cannot aggregate by rule.

So this stack uses both logs from Part 1, each for what it is good at:

- **Caddy's log** has one line per rule match. That is the natural unit for "top rules", "attack categories", "paranoia level" and "severity". It becomes the `waf-alerts` stream.
- **The JSON audit log** has one line per transaction. That is the unit for "blocked vs. logged only" and for reading the full evidence. It becomes the `waf-audit` stream.

Both carry Coraza's transaction ID, so a rule match in the first stream can be matched with its transaction in the second.

## The stack

```yaml
# grafana-loki/compose.yaml (abridged; the full file is attached above)
name: crs-grafana-loki

services:
  waf:
    image: ghcr.io/coreruleset/coraza-crs:4.30.0-caddy-alpine-202610110510
    ports:
      - "${BIND_ADDR:-127.0.0.1}:${WAF_PORT:-8080}:8080"
    environment:
      BLOCKING_PARANOIA: "1"
      DETECTION_PARANOIA: "2"
      CORAZA_AUDIT_ENGINE: RelevantOnly
      CORAZA_AUDIT_LOG_FORMAT: JSON
      CORAZA_AUDIT_LOG_TYPE: Serial
      CORAZA_AUDIT_LOG: /var/log/coraza/audit.log
      CORAZA_AUDIT_LOG_PARTS: ABIJFHZ   # no response body
    volumes:
      - waf-logs:/var/log/coraza
      - ./coraza/Caddyfile:/config/caddy/Caddyfile:ro
      - ../waf/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf:/opt/coraza/rules.d/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf:ro
      - ./coraza/audit-relevant.conf:/opt/coraza/rules.d/audit-relevant.conf:ro

  backend:
    image: traefik/whoami:v1.12.0

  loki:
    image: grafana/loki:3.7.9
    command: -config.file=/etc/loki/loki-config.yaml
    volumes:
      - ./loki/loki-config.yaml:/etc/loki/loki-config.yaml:ro
      - loki-data:/loki

  alloy:
    image: grafana/alloy:v1.21.1
    command: ["run", "--server.http.listen-addr=0.0.0.0:12345", "--storage.path=/var/lib/alloy/data", "/etc/alloy/config.alloy"]
    volumes:
      - ./alloy/config.alloy:/etc/alloy/config.alloy:ro
      - waf-logs:/var/log/coraza:ro
      - alloy-data:/var/lib/alloy/data
    ports:
      - "${BIND_ADDR:-127.0.0.1}:12345:12345"

  grafana:
    image: grafana/grafana:13.2.4
    environment:
      GF_AUTH_ANONYMOUS_ENABLED: "true"
      GF_AUTH_ANONYMOUS_ORG_ROLE: Admin
      GF_AUTH_DISABLE_LOGIN_FORM: "true"
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
      - ./grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana-data:/var/lib/grafana
    ports:
      - "${BIND_ADDR:-127.0.0.1}:3000:3000"

volumes:
  waf-logs:
  loki-data:
  alloy-data:
  grafana-data:
```

The WAF gets three files. The summary rule is the same file Part 2 uses, dropped into `/opt/coraza/rules.d/`, which the image includes after CRS. The audit relevance rule is the one above. And the {{< resource-link text="Caddyfile" file="grafana-loki/coraza/Caddyfile" >}} replaces the one the image generates, for two reasons:

```caddyfile
{
	order coraza_waf first

	log {
		output file /var/log/coraza/caddy.log
		format json {
			time_format rfc3339_nano
		}
		level INFO
	}

	servers {
		trusted_proxies static private_ranges 100.64.0.0/10
		client_ip_headers X-Forwarded-For
	}
}

:8080 {
	coraza_waf {
		include /opt/coraza/config/coraza.conf
		include /opt/coraza/config.d/*.conf
		include /opt/coraza/config/crs-setup.conf
		include /opt/coraza/owasp-crs/rules/*.conf
		include /opt/coraza/rules.d/*.conf
	}

	reverse_proxy backend:80
}
```

First, the log. Coraza does not have an error log of its own inside Caddy; it writes alerts through Caddy's logger, which the generated configuration sends to `stderr`. Here it goes to a file on the shared volume, as JSON with readable timestamps. The level matters in the same way NGINX's does in Part 2: coraza-caddy logs CRITICAL and ERROR matches at `error`, WARNING matches and blocking decisions at `warn`, and NOTICE matches at `info`, so `INFO` is the level that shows them all.

Second, the client address. Caddy's `trusted_proxies` and `client_ip_headers` make Caddy, and with it Coraza, use the address from `X-Forwarded-For` when the request comes from a trusted proxy. It is the same policy as the realip snippet in Part 2, including the same warning: in production, trust your load balancers and nothing else.

Loki runs as a single binary with filesystem storage, the `tsdb` index and structured metadata enabled. It has no write-ahead log, deliberately: with the WAL on, Loki throttles and silently loses writes when the disk holding its data directory is more than 90% full, and that is a common state for a laptop. Keep the WAL on in production and give Loki a disk of its own.

Grafana is provisioned from files: a Loki data source and a dashboard provider pointing at the `dashboards/` directory. Edit the JSON, and Grafana picks it up within ten seconds.

## The Alloy pipeline

[Grafana Alloy](https://grafana.com/docs/alloy/latest/) is the collector that replaced Promtail. Its configuration is a small graph: a file matcher feeds a file source, the source feeds a processing pipeline, the pipeline feeds a Loki writer. The {{< resource-link text="full file" file="grafana-loki/alloy/config.alloy" >}} has both streams; here is the one for the alerts, which does the interesting work.

```alloy
local.file_match "waf_alerts" {
	path_targets = [{
		__path__ = "/var/log/coraza/caddy.log",
		job      = "waf-alerts",
	}]
}

loki.source.file "waf_alerts" {
	targets    = local.file_match.waf_alerts.targets
	forward_to = [loki.process.waf_alerts.receiver]
}

loki.process "waf_alerts" {
	// Caddy writes JSON; Coraza's alerts are the "msg" of the WAF logger.
	stage.json {
		expressions = { ts = "ts", logger = "logger", alert = "msg" }
	}
	stage.match {
		selector = "{job=\"waf-alerts\"} != \"http.handlers.waf\""
		action   = "drop"
	}
	stage.match {
		selector = "{job=\"waf-alerts\"} != \"Coraza: \""
		action   = "drop"
	}
	stage.timestamp {
		source = "ts"
		format = "RFC3339Nano"
	}

	// From here on the log line is the Coraza alert itself.
	stage.output { source = "alert" }

	// "Warning" is a rule match, "Access denied" is the verdict.
	stage.regex {
		expression = "^\\[client \\\"(?P<client_ip>[^\\\"]*)\\\"\\] Coraza: (?P<kind>Warning|Access denied)"
	}

	// The bracketed key/value pairs. One regex per field keeps them independent:
	// a field that is missing on a line simply stays empty.
	stage.regex { expression = "\\[id \\\"(?P<rule_id>\\d+)\\\"\\]" }
	stage.regex { expression = "\\[msg \\\"(?P<msg>[^\\\"]*)\\\"\\]" }
	stage.regex { expression = "\\[data \\\"(?P<data>[^\\\"]*)\\\"\\]" }
	stage.regex { expression = "\\[severity \\\"(?P<severity_word>[a-z]+)\\\"\\]" }
	stage.regex { expression = "\\[tag \\\"attack-(?P<attack>[^\\\"]+)\\\"\\]" }
	stage.regex { expression = "\\[tag \\\"paranoia-level/(?P<paranoia_level>\\d)\\\"\\]" }
	// Coraza's [uri] includes the query string: keep the path separately for grouping.
	stage.regex { expression = "\\[uri \\\"(?P<uri>(?P<path>[^\\\"?]*)[^\\\"]*)\\\"\\]" }
	stage.regex { expression = "\\[unique_id \\\"(?P<unique_id>[^\\\"]*)\\\"\\]" }

	// Rule 949110 carries the total score; our summary rule carries everything.
	stage.regex { expression = "Total Score: (?P<total_score>\\d+)" }
	stage.regex {
		expression = "inbound_blocking=(?P<inbound_blocking>\\d+) inbound_detection=(?P<inbound_detection>\\d+) inbound_pl=(?P<pl1>\\d+)-(?P<pl2>\\d+)-(?P<pl3>\\d+)-(?P<pl4>\\d+) inbound_threshold=(?P<inbound_threshold>\\d+) outbound_blocking=(?P<outbound_blocking>\\d+) outbound_detection=(?P<outbound_detection>\\d+)"
	}

	// Classify: alert, block, summary (rule 99901) or report (CRS's 980170).
	stage.template {
		source   = "event"
		template = "{{ if eq .kind \"Access denied\" }}block{{ else if eq .rule_id \"99901\" }}summary{{ else if eq .rule_id \"980170\" }}report{{ else }}alert{{ end }}"
	}
	stage.template {
		source   = "severity"
		template = "{{ if and .severity_word (ne .severity_word \"unknown\") }}{{ ToUpper .severity_word }}{{ end }}"
	}

	// Labels: low cardinality only.
	stage.labels {
		values = { event = "", rule_id = "", attack = "", paranoia_level = "", severity = "" }
	}

	// Everything else travels as structured metadata.
	stage.structured_metadata {
		values = {
			msg = "", data = "", uri = "", path = "", unique_id = "", client_ip = "",
			total_score = "", inbound_blocking = "", inbound_detection = "", inbound_threshold = "",
			outbound_blocking = "", outbound_detection = "", pl1 = "", pl2 = "", pl3 = "", pl4 = "",
		}
	}

	forward_to = [loki.write.default.receiver]
}
```

The first half deals with Caddy: parse the JSON, keep only the WAF logger's alert lines, take the timestamp, and replace the stored line with the alert itself, so that what you read in Grafana is the familiar bracketed format rather than JSON with escaped quotes. The second half would work almost unchanged on a ModSecurity error log; only the client prefix and the severity differ.

The design decision in this file is which fields become labels. In Loki, every distinct combination of label values is a stream, and streams are what cost memory and index space. `event`, `attack`, `paranoia_level` and `severity` have a handful of values each. `rule_id` has a few hundred, which is fine for a lab and acceptable for most production WAFs, and it is the field every "top rules" query groups by, so it earns its place. Everything with unbounded cardinality (URI and path, client address, transaction ID, the matched data) goes into [structured metadata](https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/): stored with the line, filterable and groupable in queries, but not a stream dimension. If you run this on a busy WAF and Loki complains about the number of streams, move `rule_id` to structured metadata as well and the queries still work.

The audit stream is simpler: `stage.json` pulls out the timestamp, transaction ID, client address, method, URI, status and `is_interrupted`, and `blocked` and `method` become labels. The line itself is the whole JSON record. That is why the compose file leaves part `E`, the response body, out of the audit log: unlike the Logstash pipeline in Part 2, nothing here would strip it before it reaches Loki.

Alloy's own UI at <http://localhost:12345> shows the pipeline graph and, under each component, the last lines that went through it with their extracted values. It is the fastest way to debug a regular expression.

## The queries

With that shape in Loki, the dashboard queries read almost like the questions from Part 1. A few representative ones:

```logql
# Rule matches over time, by attack category
sum by (attack) (count_over_time({job="waf-alerts", event="alert", attack!=""}[$__auto]))

# Top rules, with their message (structured metadata can be grouped on, too)
topk(15, sum by (rule_id, msg) (count_over_time({job="waf-alerts", event="alert"} | msg != "" [$__range])))

# Most targeted paths
topk(15, sum by (path) (count_over_time({job="waf-alerts", event="alert"} | path != "" [$__range])))

# Blocked vs. logged-only transactions
sum by (blocked) (count_over_time({job="waf-audit"}[$__auto]))

# Highest detection-level score per interval, from the summary rule
max(max_over_time({job="waf-alerts", event="summary"} | unwrap inbound_detection [$__auto]))

# What a higher paranoia level would have blocked
{job="waf-alerts", event="summary"} | inbound_blocking < 5 | inbound_detection >= 5

# Everything about one transaction
{job=~"waf-.*"} | unique_id = "qRJvybmnRhuIaVTS"
```

The last two are not on the dashboard; they are the ones you type in Explore. The `unique_id` filter is the Loki equivalent of clicking a row in Kibana: it returns the rule matches and the audit record of the same request, from both streams, in one result.

## The dashboard

{{< resource-link text="grafana/dashboards/crs-overview.json" file="grafana-loki/grafana/dashboards/crs-overview.json" >}} has the same panels as the Kibana dashboard in Part 2, so we will not repeat the list. Two differences are worth knowing.

It has two variables at the top, **attack category** and **rule ID**, populated from Loki's label values. Pick `sqli` and every alert-level panel narrows to SQL injection; pick a rule ID and you see where and from whom that one rule fires, which is the view you want when deciding whether to write an exclusion for it.

And the bottom two panels are log panels rather than a table: **recent alerts**, reformatted with `line_format` to show the rule, the message, the URI, the client and the matched data on one line, and **transactions** from the audit log. Expanding a line in the second one shows the complete JSON audit record, which is the evidence from Part 1 in its original form. Expanding a line in the first shows its labels and structured metadata, including the `unique_id` you can copy into Explore.

The traffic is the same generator as in Part 2 and CRS is the same release, so the two dashboards are directly comparable. They mostly agree, which is the point of CRS running on both engines. The one difference you will notice is the `TRACE` request: NGINX rejects it with a 405 before ModSecurity sees it, while Caddy passes it to Coraza, and CRS blocks it.

## Adapting it

**Coraza on NGINX or Apache.** The same image comes in `nginx` and `apache` variants. The alerts then go to the web server's error log instead of Caddy's JSON log: drop the JSON stage and the first two filters, and match the alert lines on `Coraza: ` directly.

**ModSecurity.** If you run ModSecurity with Loki, the alert half of the pipeline needs three changes: the client address is the trailing `client: 203.0.113.11,` field on NGINX (or a `[client 203.0.113.11:54321]` prefix on Apache), the severity is a number, and the error log must be at `info` level on NGINX. The audit stream needs the ModSecurity field names: `transaction.unique_id`, `transaction.time_stamp`, `transaction.response.http_code`. Part 2's ModSecurity configuration works as is for the WAF side.

**Alerting.** Grafana's alert rules take the same LogQL. "More than 20 blocked requests from one client in five minutes" is `sum by (client_ip) (count_over_time({job="waf-alerts", event="block"} | client_ip != "" [5m])) > 20`, and "a rule that was quiet last week is loud today" is a comparison of two `count_over_time` ranges with `offset`.

**Which stack?** The two halves are independent: either engine works with either log platform, and the summary rule makes their output comparable. Part 2's Elastic approach pays off when you want to search inside the request (any header, any parameter) and build ad hoc charts over many fields; it costs more memory and some care with the index mapping. This post's Loki approach is lighter, keeps the logs byte for byte, and fits naturally next to the metrics and traces you may already have in Grafana; it asks you to think about labels up front. If you already run one of the two, use that one. If you run neither, start with Loki: it is the smaller thing to operate.

{{< series-nav >}}

## Download

Everything this post uses, in one archive. It unpacks to a `crs-logging/` folder with a short README.

{{< resources title="All files" pattern="[.]zip$" >}}

{{< related-pages "CRS-Logging" >}}
