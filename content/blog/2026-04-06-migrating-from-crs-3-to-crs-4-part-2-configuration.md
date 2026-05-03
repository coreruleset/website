---
author: fzipi
categories:
  - Blog
date: '2026-04-06T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-antonio-batinic-2573434-4164418.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 2: Configuration'
slug: 'migrating-crs-3-to-4-part-2-configuration'
---

This is Part 2 of the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). Part 1 provided an overview of the migration. This post covers the `crs-setup.conf` changes — the most immediately breaking part of the upgrade for most operators.

If you take one thing from this post: **do not reuse your CRS 3 `crs-setup.conf` with CRS 4 without reviewing every variable in it.** Some variables were renamed, some were removed, and several new ones are required for features that did not exist in CRS 3.

{{< figure src="/images/2026/04/pexels-antonio-batinic-2573434-4164418.jpg" caption="Every configuration variable matters" attr="Antonio Batinić on Pexels" attrlink="https://www.pexels.com" >}}

## The Migration Approach for Configuration

The recommended approach is to start with the CRS 4 `crs-setup.conf.example` as your new base and re-apply your customizations from your CRS 3 file. Copying your old file and patching it is possible but more error-prone — the structure and default values of several sections changed.

Open both files side by side. Work section by section.

## Renamed Variables: Paranoia Level

The paranoia level variable was renamed in CRS 4. In CRS 3 you set `tx.paranoia_level`. In CRS 4 the same setting is `tx.blocking_paranoia_level`:

```apache
# CRS 3 (id:900000):
#   setvar:tx.paranoia_level=1

# CRS 4 (id:900000):
#   setvar:tx.blocking_paranoia_level=1
```

CRS 4 also introduces a companion variable, `tx.detection_paranoia_level`, that did not exist in CRS 3. It lets you execute rules from a higher paranoia level than `tx.blocking_paranoia_level` without having those rules contribute to the anomaly score. This is useful for exploring the impact of moving to a higher PL before committing to it:

```apache
#SecAction \
#    "id:900001,\
#    phase:1,\
#    pass,\
#    t:none,\
#    nolog,\
#    setvar:tx.detection_paranoia_level=2"
```

If you do not set it, `tx.detection_paranoia_level` defaults to the value of `tx.blocking_paranoia_level`. For migration, we recommend you do not set it and let it.

## Anomaly Scoring Variables

The threshold variable names are **unchanged**:

| Variable | CRS 3 | CRS 4 |
|---|---|---|
| Inbound block threshold | `tx.inbound_anomaly_score_threshold` | `tx.inbound_anomaly_score_threshold` |
| Outbound block threshold | `tx.outbound_anomaly_score_threshold` | `tx.outbound_anomaly_score_threshold` |

The per-severity scoring increment variables (`tx.critical_anomaly_score`, `tx.error_anomaly_score`, `tx.warning_anomaly_score`, `tx.notice_anomaly_score`) also existed in CRS 3 and carry over unchanged at their default values (5, 4, 3, 2).

What changed is the internal score accumulation model and how scores are reported — this is covered in detail in Part 4.

## New Variable: Reporting Level

CRS 4 introduces `tx.reporting_level` (rule id:900115), which controls how much detail the phase 5 reporting rules log beyond the blocking rule itself. There is no CRS 3 equivalent.

The six levels are:

| Level | Behaviour |
|---|---|
| `0` | Reporting disabled — only the blocking rule logs |
| `1` | Report requests where the blocking anomaly score ≥ threshold |
| `2` | Report requests where the detection anomaly score ≥ threshold |
| `3` | Report requests where the blocking anomaly score > 0 |
| `4` | Report requests where the detection anomaly score > 0 (default) |
| `5` | Report all requests |

The default is `4`. This is more verbose than CRS 3, where only blocked requests were reported. If your SIEM or log aggregation infrastructure is sensitive to log volume, consider starting with level `1` or `2` during the migration and raising it once you have confirmed your log pipeline can handle the volume.

## New Variable: Early Blocking

CRS 4 introduces `tx.early_blocking` (rule 900120), which controls whether the anomaly score is evaluated at the end of phase 1 (before the request body is processed) and at the end of phase 3 (before the response body is processed).

The purpose of early blocking is to reduce the amount of work the web server and WAF have to do when traffic will be rejected anyway.

```apache
#SecAction \
#    "id:900120,\
#    phase:1,\
#    pass,\
#    t:none,\
#    nolog,\
#    setvar:tx.early_blocking=1"
```

When commented out (the default), early blocking is disabled and behaviour matches CRS 3 exactly — evaluation happens only at the end of phase 2 and phase 4.

For migration, leave this commented out. Enable it only after the rest of the migration is stable.

## New Variable: Default Collections

CRS 4 introduces the `tx.enable_default_collections` flag. In CRS 3, the GLOBAL and IP collections were initialized by the core rule set for every request. In CRS 4, the core rules themselves no longer use these collections — but plugins may.

```apache
# Default: off — collections not initialized unless needed
SecAction \
    "id:900130,\
    phase:1,\
    nolog,\
    pass,\
    t:none,\
    setvar:tx.enable_default_collections=0"
```

If you install any plugin that uses IP or GLOBAL collections (such as the fake-bot plugin or the auto-decoding plugin), set this to `1`. If you run only the core rules with no plugins that require collections, leave it at `0`.

## Restricted Headers: Restructured Into Two Variables

CRS 3 managed restricted headers through a single `tx.restricted_headers` variable. CRS 4 splits this into two variables with different enforcement behaviour:

- **`tx.restricted_headers_basic`** (id:900250) — headers that are always forbidden, regardless of paranoia level
- **`tx.restricted_headers_extended`** (id:900255) — headers that are forbidden at higher paranoia levels

This split is itself a breaking change: if you customised `tx.restricted_headers` in CRS 3, you need to decide which of the two new variables your customisation belongs in.

### New additions to the basic list

Several headers were added to the basic list that were not restricted in CRS 3:

| Header | Reason |
|---|---|
| `content-encoding` | WAF engines cannot inspect compressed bodies; blocking removes the bypass vector |
| `x-http-method-override`, `x-http-method`, `x-method-override` | Prevents HTTP method override attacks |
| `x-middleware-subrequest` | CVE-2025-29927 (Next.js middleware bypass) |
| `expect` | Prevents Expect-based HTTP desync attacks |

All of these are blocked at PL1. If your application or any client sending requests to it uses these headers legitimately, you will see blocks immediately after the migration.

### The extended list

The default extended list contains `/accept-charset/`. This header is deprecated and can be used to bypass the WAF on response rules, but it still appears in some legitimate clients, so it is restricted at higher paranoia levels rather than universally. If you run at PL2 or above, check whether any of your clients send `Accept-Charset`.

### Adding exclusions

```apache
# Example: allow content-encoding on a specific upload endpoint
SecRule REQUEST_URI "@beginsWith /api/upload" \
    "id:1000,phase:1,pass,nolog,\
    ctl:ruleRemoveTargetById=920450;REQUEST_HEADERS:Content-Encoding"
```

`X-HTTP-Method-Override` in particular is used by JavaScript frameworks (Laravel, Rails, Symfony) — check your frontend if you use any of these.

## New Variable: Method Override Parameter

CRS 4 adds `tx.allow_method_override_parameter` (rule 900210), which controls whether the `_method` query parameter used by many web frameworks for HTML form method override is allowed. By default this is blocked at PL2 and higher.

If your application uses a framework that relies on `_method=DELETE` or `_method=PATCH` in form submissions, set this to `1` or add a targeted exclusion. If you run at PL1 only, this is not triggered.

## New Variable: Skip Response Analysis

CRS 4 adds `tx.crs_skip_response_analysis` (rule 900500). Response body analysis is enabled by default in CRS 4 (when `SecResponseBodyAccess On` is set in your engine config). A newly documented attack class — Request Filter Denial of Service (RFDoS) — can abuse response body inspection to exhaust WAF resources. Setting `tx.crs_skip_response_analysis=1` disables response inspection entirely.

For migration, leave this at the default (response analysis enabled). Be aware of the trade-off if you are deploying in an environment where RFDoS is a concern.

## HTTP Version Defaults

CRS 3 tolerated HTTP/0.9 requests. CRS 4 does not — rule 920430 blocks HTTP/0.9 requests outright. If your infrastructure passes HTTP/0.9 internally (rare, but seen in legacy load balancers), you will see blocks. The fix is to add back HTTP/0.9 in rule 900230.

## The SecCollectionTimeout Removal

CRS 3 defined `SecCollectionTimeout` in `crs-setup.conf`. CRS 4 removed this setting from the core rule set because the core rules no longer work with collections directly. If you need a custom collection timeout, set it in your WAF's main configuration or in a plugin's configuration file.


## Migration Checklist

Work through this list before reloading your WAF with CRS 4:

- [ ] Start from `crs-setup.conf.example`, not from your CRS 3 file
- [ ] Re-apply paranoia level: `tx.paranoia_level` → `tx.blocking_paranoia_level`
- [ ] Consider `tx.detection_paranoia_level` if you want to trial a higher PL without scoring
- [ ] Re-apply `tx.inbound_anomaly_score_threshold` and `tx.outbound_anomaly_score_threshold` (names unchanged)
- [ ] Set `tx.reporting_level` appropriate for your log volume (default `4`)
- [ ] Leave `tx.early_blocking` commented out for initial migration (disabled by default)
- [ ] Decide on `tx.enable_default_collections` based on which plugins you will install
- [ ] Migrate `tx.restricted_headers` customisations to `tx.restricted_headers_basic` and/or `tx.restricted_headers_extended`
- [ ] Check for newly restricted basic headers in your application's requests (`content-encoding`, `x-http-method-override`, `expect`, etc.)
- [ ] Check for `accept-charset` in client requests if running at PL2+
- [ ] Decide on `tx.allow_method_override_parameter` if your app uses `_method` form parameter at PL2+
- [ ] Decide on `tx.crs_skip_response_analysis` if RFDoS is a concern in your environment
- [ ] Remove or migrate any `SecCollectionTimeout` directive from your old config
- [ ] Review the full `crs-setup.conf.example` for any new options not present in CRS 3

## Interactive Migration Tool

Paste your CRS 3 `crs-setup.conf` into the tool below and click **Migrate to CRS 4**. It will generate a CRS 4 config with all renamed variables applied, new variables pre-populated with their defaults, and a colour-coded notes panel explaining every change.

{{< crs-config-migrator >}}

## What's Next

[Part 3]({{< ref "blog/2026-04-13-migrating-from-crs-3-to-crs-4-part-3-plugins.md" >}}) covers the plugin architecture in depth — including the full mapping from CRS 3 application exclusion packages to CRS 4 plugins, and how to install them.

{{< related-pages "Migration" "CRS-v4" >}}
