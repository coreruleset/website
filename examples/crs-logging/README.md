# OWASP CRS logging series: companion stacks

Everything referenced by the "Logging with OWASP CRS" blog series on
[coreruleset.org](https://coreruleset.org/blog/):

| Part | What it is | Files |
|------|------------|-------|
| 1 | What CRS logs, what to look for, and what to add | `waf/` |
| 2 | ModSecurity + CRS logs in the Elastic Stack (Logstash, Elasticsearch, Kibana) | `elk/` |
| 3 | Coraza + CRS logs in Grafana + Loki (shipped with Grafana Alloy) | `grafana-loki/` |

Both stacks run CRS 4.30.0 from the CRS project's own images, in front of a
tiny echo backend, blocking at paranoia level 1 and logging at paranoia
level 2. The engine differs:

- `elk/` runs ModSecurity v3 on NGINX (`owasp/modsecurity-crs`).
- `grafana-loki/` runs Coraza on Caddy (`ghcr.io/coreruleset/coraza-crs`).

## Quick start

Each blog post has a zip with the files it uses, which unpacks to a
`crs-logging/` folder with the layout shown below. Run everything from
that folder (or from this directory, if you are in the repository):

```bash
# Pick one:
cd elk            # ModSecurity + Elastic Stack, needs ~4 GB RAM
cd grafana-loki   # Coraza + Grafana + Loki, needs ~1 GB RAM

docker compose up -d
../generate-traffic.sh 300
```

Then open the dashboard:

- Elastic Stack: <http://localhost:5601/app/dashboards> (dashboard "OWASP CRS - ModSecurity overview")
- Grafana: <http://localhost:3000/d/crs-coraza-overview>

The WAF itself listens on <http://localhost:8080> (set `WAF_PORT` to change
it, for example if you want both stacks running at the same time).

Every port is published on `127.0.0.1` only. To open the dashboards from
another machine, for example over Tailscale or your LAN, set `BIND_ADDR` to
that interface's address and point the traffic generator at it:

```bash
BIND_ADDR=100.64.0.10 docker compose up -d
TARGET=http://100.64.0.10:8080 ../generate-traffic.sh 300
```

To start over with empty logs and an empty log store:

```bash
docker compose down -v
```

## Layout

```
crs-logging/
├── build-archives.py            # builds the per-post zip downloads
├── generate-traffic.sh          # mix of legitimate and malicious requests
├── waf/
│   ├── RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf   # phase 5 score summary rule (both engines)
│   └── nginx-realip.conf        # client address from X-Forwarded-For (NGINX)
├── elk/
│   ├── compose.yaml
│   ├── logstash/
│   │   ├── pipeline/modsec-audit.conf   # file input -> flatten -> Elasticsearch
│   │   ├── scripts/modsec_flatten.rb    # the flattening logic
│   │   └── templates/modsec-audit.json  # index template (field types)
│   └── kibana/
│       ├── crs-dashboard.ndjson     # data view + Discover session + dashboard
│       └── build-dashboard.py       # regenerates the file above
└── grafana-loki/
    ├── compose.yaml
    ├── coraza/
    │   ├── Caddyfile                # log to a file, trust X-Forwarded-For
    │   └── audit-relevant.conf      # audit log every transaction that scored
    ├── loki/loki-config.yaml
    ├── alloy/config.alloy           # tails the logs, parses, pushes to Loki
    └── grafana/
        ├── provisioning/            # Loki data source + dashboard provider
        └── dashboards/crs-overview.json
```

## Notes

- These are labs. Authentication is disabled on Kibana, Elasticsearch and
  Grafana, Elasticsearch ignores the disk watermark and Loki runs without a
  write-ahead log. Keep the default loopback bindings unless you need remote
  access. If you set `BIND_ADDR` to a non-loopback address, limit access to a
  controlled network with firewall rules; do not expose the stacks to the
  public internet. Do not copy these settings into production.
- The traffic generator sends textbook payloads; it is not a scanner and
  does not try to evade anything. Every request is sent with a fake
  `X-Forwarded-For`, which the stacks trust from broad lab-only address ranges
  (`waf/nginx-realip.conf`), so the "top clients" panels have something to
  show. A peer in those ranges can spoof client addresses. Do not use this
  trust list in production; trust only controlled load balancers.
  It runs on bash 3.2 or later, so the macOS default works.
- Tested with the image tags pinned in the compose files. Newer tags should
  work; if Kibana refuses the dashboard import after an upgrade, update the
  migration versions at the end of `elk/kibana/build-dashboard.py` and
  regenerate the NDJSON file.
- The blog posts publish these files as page resources: `config/_default/hugo.yaml`
  mounts parts of this directory into each post's page bundle, and the
  `resources` shortcode lists them. If you move or rename files here, update
  those mounts (and the shortcode patterns in the posts) to match.
- Each post also has a zip of its files, built by `build-archives.py` into
  the post's page bundle. Hugo cannot create zips, so after changing any
  file here, run `python3 examples/crs-logging/build-archives.py` from the
  repository root and commit the result. CI fails the pull request if an
  archive is out of date.
