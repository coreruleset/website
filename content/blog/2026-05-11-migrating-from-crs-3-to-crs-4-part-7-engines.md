---
author: fzipi
categories:
  - Blog
date: '2026-05-11T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-brett-sayles-4508751.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 7: Engine-Specific Notes'
slug: 'migrating-crs-3-to-4-part-7-engines'
---

This is Part 7 — the final post — in the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). The previous six posts covered configuration, plugins, anomaly scoring, rule changes, and tuning. This post covers the engine layer: what WAF engines CRS 4 supports, how support differs across them, and the changes to Docker-based deployments.

{{< figure src="/images/2026/04/pexels-brett-sayles-4508751.jpg" caption="Choosing the right engine for CRS 4" attr="Brett Sayles on Pexels" attrlink="https://www.pexels.com" >}}

## The CRS 4 Engine Support Matrix

CRS 4 officially supports three WAF engines:

| Engine | Status | Notes |
|---|---|---|
| ModSecurity v2 (Apache) | Supported | Reference implementation for most operators; full feature support |
| ModSecurity v3 (libmodsecurity) + Nginx | Supported | Some Lua-based plugins require additional compilation steps |
| Coraza | Supported | Actively maintained; recommended for new deployments |

Two configurations that worked in some CRS 3 deployments are explicitly **not supported** in CRS 4:

- **Nginx + ModSecurity v2**: This combination never had official support and is known to behave incorrectly.
- **Apache + ModSecurity v3**: This combination has known connector issues that affect rule processing.

If you are running either of these unsupported combinations with CRS 3, the migration to CRS 4 is a good time to correct the engine setup.

## ModSecurity v2

ModSecurity v2 is the most mature engine and the one where CRS has historically been developed and tested. If you are running CRS 3.3.x on Apache + ModSecurity v2, the CRS 4 migration path is the most straightforward.

### What Changed

The core behaviour is unchanged. The same `SecRule`, `SecAction`, `SecRuleRemoveById`, and related directives work identically. The main operational differences are:

**Plugin Include ordering.** As covered in Part 3, you must add three new `Include` lines to your Apache configuration for the plugin `*-config.conf`, `*-before.conf`, and `*-after.conf` files. Apache's `mod_security2.so` processes these without any modification.

**Lua plugins.** Some CRS 4 plugins — notably the fake-bot plugin — require Lua support. ModSecurity v2 supports Lua via the `SecRuleScript` directive, but it must be compiled with Lua support. Verify with:

```bash
apachectl -M | grep security
# Then check ModSecurity build flags:
grep -r LUA /path/to/modsecurity.conf
```

If Lua is not compiled in and you want to use a Lua-dependent plugin, you will need to recompile or use an alternative package. DigitalWave ([modsecurity.digitalwave.hu](https://modsecurity.digitalwave.hu)) maintains updated ModSecurity v2 packages for Debian/Ubuntu that include Lua support.

**`SecCollectionTimeout` removal.** As noted in Part 2, this directive was removed from `crs-setup.conf` in CRS 4. If you have it in your global `modsecurity.conf` (not in `crs-setup.conf`), it continues to work. If you had it in `crs-setup.conf`, move it to your global ModSecurity configuration.

### Version Requirements

CRS 4 requires ModSecurity v2.9.x. Versions earlier than 2.9 are not supported. Most distribution packages and the DigitalWave builds are at 2.9.x — verify before proceeding:

```bash
apachectl -M 2>&1 | grep -i modsec
```

## ModSecurity v3 (libmodsecurity)

ModSecurity v3 is the rewritten C++ library implementation. CRS 4 supports it for Nginx (using the `ngx_http_modsecurity_module` connector). The Apache + ModSecurity v3 combination is not supported.

### Key Differences from v2

**Connector quality matters.** The ModSecurity v3 connector for Nginx has historically had gaps in SecLang support. Before deploying CRS 4 on ModSecurity v3, run the CRS test suite ([go-ftw](https://github.com/coreruleset/go-ftw)) against your deployment to verify that the connector correctly processes the rules.

**Some v2-specific directives are absent.** Directives that are Apache-specific (like `SecUploadDir`) behave differently or do not apply. Review the [ModSecurity v3 compatibility notes](https://github.com/owasp-modsecurity/ModSecurity/wiki/Reference-Manual-(v3.x)) for your connector version.

**`WebAppID` support.** ModSecurity v3's Nginx connector supports `SecWebAppID`, which is used for per-virtual-host plugin scoping (described in Part 3). Verify your connector version supports it before relying on it.

**Lua.** Lua support in ModSecurity v3 is available but requires the library to be compiled with Lua. If you use Lua-dependent plugins, verify your build:

```bash
nginx -V 2>&1 | grep modsec
```

## Coraza

Coraza is a modern, full-featured WAF engine written in Go, implementing the SecLang specification. It is the recommended engine for new CRS 4 deployments.

### Why Consider Coraza for Migration

If you are already planning the migration from CRS 3 to CRS 4, it is worth evaluating whether this is also the right time to migrate from ModSecurity to Coraza. Coraza's advantages include:

- **Active development**: The project moves faster than ModSecurity v3 and responds quickly to CRS compatibility requirements
- **Go ecosystem integration**: Coraza embeds naturally into Go-based proxy and server stacks (Caddy, custom proxies)
- **Clean SecLang implementation**: Fewer connector-specific edge cases than the ModSecurity v3 + Nginx pairing

The trade-off is operational familiarity. If your team knows ModSecurity v2 well, there will be a learning curve.

### Coraza-Specific Notes

**`WebAppID` not supported.** As of the time of writing, Coraza does not support `SecWebAppID`. For per-virtual-host plugin scoping on Coraza, use the `Host` header match pattern shown in Part 3.

**RE2/Hyperscan.** Coraza can be built with RE2 or Go's native `regexp` package. CRS 4's RE2 compatibility (covered in Part 5) means that CRS rules work correctly regardless of which regex backend Coraza uses.

**Plugin compatibility.** Lua-based plugins (fake-bot, antivirus) require Lua support in the WAF engine. Coraza's Lua support depends on the build configuration. If Lua is not available, these plugins are not compatible — consider alternatives or use detection-only mode for those use cases.

## Docker Images

CRS 4 ships official Docker images that bundle the WAF engine, the web server, and CRS 4 rules in a single container. The image tagging scheme changed significantly from the unofficial CRS 3 images.

### CRS 4.25.0 LTS Images

```bash
# ModSecurity + Apache
docker pull owasp/modsecurity-crs:4.25-lts-apache

# ModSecurity + Nginx
docker pull owasp/modsecurity-crs:4.25-lts-nginx

# Coraza + Caddy
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-caddy

# Coraza + Nginx (experimental)
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-nginx

# Coraza + Apache (experimental)
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-apache
```

The `4.25-lts` floating tag always points to the latest LTS point release. The pinned form `4.25.N-lts` locks to a specific release.

### Configuring CRS in Docker

The Docker images accept `crs-setup.conf` variables as environment variables. For example:

```bash
docker run \
  -e PARANOIA=2 \
  -e INBOUND_ANOMALY_SCORE_THRESHOLD=5 \
  -e BLOCKING_EARLY=0 \
  owasp/modsecurity-crs:4.25-lts-nginx
```

The environment variable names correspond directly to the `crs-setup.conf` variable names, uppercased. Check the image's README on Docker Hub or GitHub for the full list.

For plugin installation in Docker, the recommended approach is to build a derived image that adds plugin files into the container's `plugins/` directory:

```dockerfile
FROM owasp/modsecurity-crs:4.25-lts-nginx

# Add WordPress exclusions plugin
COPY wordpress-rule-exclusions-plugin/plugins/ /etc/modsecurity.d/owasp-crs/plugins/
```

## Summary of the Series

This series has covered every major dimension of the CRS 3.3.9 → 4.25.0 LTS migration:

1. **Overview** — why migrate, what changed at a glance, and what to expect
2. **Configuration** — `crs-setup.conf` renamed and new variables, migration checklist
3. **Plugin architecture** — application exclusion mapping, installation methods, new capability plugins
4. **Anomaly scoring** — per-PL accumulators, new reporting model, early blocking, PL redistribution
5. **Rule changes** — new categories, removed and modified rules, auditing existing exclusions
6. **Tuning** — two migration strategies, safe production cut-over, common false positive areas
7. **Engine notes** — ModSecurity v2/v3, Coraza, Docker images *(this post)*

CRS v4.25.0 LTS is supported until Q3 2027. If you start the migration now, you have the full LTS support window ahead of you. The CRS project team will continue publishing blog posts on specific migration scenarios and edge cases — subscribe to the blog or follow [@coreruleset](https://twitter.com/coreruleset) for updates.

If you run into issues during your migration, the best places to get help are the [CRS mailing list](https://groups.google.com/a/owasp.org/forum/#!forum/modsecurity-core-rule-set-project) and the [OWASP Slack #coreruleset channel](https://owasp.slack.com/archives/CBKGH8A5P).

{{< related-pages "Migration" "CRS-v4" >}}
