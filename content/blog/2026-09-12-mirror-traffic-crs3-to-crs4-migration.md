---
author: fzipi
categories:
  - Blog
date: '2026-09-12T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
title: 'A Safety Net for the CRS 3 to CRS 4 Migration: Mirror Your Traffic First'
slug: 'mirror-traffic-crs3-to-crs4-migration'
---

Our [seven-part CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}) covers what changes and how to prepare. But reading about the changes and trusting them in production are two different things. If you are still running CRS 3 and hesitant to cut over, this post gives you a way to see CRS 4's behavior against your own real traffic, live, before you change anything in production.

## The idea: mirror, don't switch

Docker Compose has no built-in way to send one request to two backends — that is not a networking feature, it is an application-layer concern. The standard tool for it is nginx's [`mirror`](https://nginx.org/en/docs/http/ngx_http_mirror_module.html) directive: it sends an async copy of every request to a shadow backend while the client only ever sees the response from the primary. If the shadow request fails, times out, or returns a 500, the client never knows.

That gives you a setup where:

- **CRS 3** stays in front, in production, answering real clients exactly as it does today.
- **CRS 4** sits in the shadows, receiving a copy of every request, so you can diff its ModSecurity audit log against CRS 3's for real traffic — no synthetic test suite, no guessing which of your users' edge cases might trip a new rule.

Apache has no equivalent to nginx's `mirror` module, so the front door here is a small, plain nginx container — regardless of whether your CRS containers run Apache or Nginx underneath.

## The compose file

CRS 4 is pulled straight from the published, stable `4.25-apache-lts` tag — no build needed. CRS 3 has no equivalent: Docker Hub only carries dated snapshot tags for it (e.g. `3-apache-202609111209`) that rotate every few days, so it's built from the [modsecurity-crs-docker](https://github.com/coreruleset/modsecurity-crs-docker) sources with `CRS_RELEASE` pinned to `3.3.10` — reproducible indefinitely, since it fetches that CRS release directly rather than depending on a tag that will eventually point somewhere else. Both front the same backend (swap `BACKEND` for your real application):

```yaml
# Mirrors live traffic to CRS3 (primary, answers the client) and CRS4 (shadow,
# fire-and-forget) against the same backend, so you can diff ModSecurity audit
# logs between versions before upgrading.
#
# CRS4 is pulled from the published, stable "lts" tag. CRS3 has no equivalent
# stable tag on Docker Hub (only dated snapshots that rotate every few days),
# so it's built from source pinned to CRS_RELEASE instead - reproducible
# forever, since it fetches the CRS release directly rather than a rotating tag.
#
# Usage:
#   docker compose up --build
#   curl "http://localhost:8080/anything?id=1' OR '1'='1"
#   docker compose logs crs-apache-v4   # what CRS4 would have done with the same request
#
# Point BACKEND at your own application to mirror real traffic instead of the
# httpbin placeholder.
services:
  backend:
    image: mccutchen/go-httpbin:v2.15.0
    expose:
      - "8080"

  crs-apache-v3:
    build:
      context: ../..
      dockerfile: apache/Dockerfile
      additional_contexts:
        image: docker-image://httpd:2.4.68
      args:
        MODSEC2_VERSION: "2.9.14"
        MODSEC2_FLAGS: "--with-yajl --with-ssdeep --with-pcre2"
        LUA_VERSION: "5.3"
        LUA_MODULES: "lua-zlib lua-socket"
        CRS_RELEASE: "3.3.10"
    environment:
      BACKEND: http://backend:8080
    expose:
      - "8080"

  crs-apache-v4:
    image: owasp/modsecurity-crs:4.25-apache-lts
    environment:
      BACKEND: http://backend:8080
    expose:
      - "8080"

  mirror:
    image: nginx:1.27-alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "8080:8080"
    depends_on:
      - crs-apache-v3
      - crs-apache-v4
```

## The nginx mirror config

```nginx
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    upstream primary {
        server crs-apache-v3:8080;
    }

    upstream shadow {
        server crs-apache-v4:8080;
    }

    server {
        listen 8080;

        location / {
            mirror /mirror;
            mirror_request_body on;
            proxy_pass http://primary;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Shadow copy: response is discarded, client never sees it or its errors.
        location = /mirror {
            internal;
            proxy_pass http://shadow$request_uri;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

`mirror_request_body on` copies the request body as well as headers, so CRS 4's body-inspection rules see the same payload CRS 3 saw.

## Trying it

```bash
docker compose up --build
curl "http://localhost:8080/anything?id=1' OR '1'='1"
docker compose logs crs-apache-v4   # what CRS4 would have done with the same request
```

The client gets CRS 3's response (a `403` for the payload above, against `crs-setup.conf` defaults). `docker compose logs crs-apache-v4` shows the same request went through CRS 4 as well — same anomaly score, same matched rules, same blocking decision, or a difference worth investigating before you touch production.

## What this does and does not tell you

This surfaces **rule-behavior differences** — a request CRS 3 allowed that CRS 4 blocks, or vice versa — against your actual traffic shape, which is far more representative than any static test payload set. It does not validate performance under your production load (the shadow container adds real CPU and network cost proportional to your traffic volume, so size it and keep an eye on it) and it does not replace the configuration and plugin-migration steps covered in the rest of the series — read [Part 2]({{< ref "blog/2026-04-06-migrating-from-crs-3-to-crs-4-part-2-configuration.md" >}}) through [Part 7]({{< ref "blog/2026-05-11-migrating-from-crs-3-to-crs-4-part-7-engines.md" >}}) for those. Think of mirroring as the empirical check that complements the reading, not a substitute for it.

{{< related-pages "Migration" "CRS-v4" >}}
