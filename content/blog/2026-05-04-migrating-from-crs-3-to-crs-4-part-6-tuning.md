---
author: fzipi
categories:
  - Blog
date: '2026-05-04T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-northern-29268627.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 6: False Positive Tuning'
slug: 'migrating-crs-3-to-4-part-6-tuning'
---

This is Part 6 of the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). Part 5 covered rule changes and how to audit your existing exclusions. This post covers the tuning phase itself — the practical work of establishing a clean CRS 4 baseline for your applications.

{{< figure src="/images/2026/04/pexels-northern-29268627.jpg" caption="Fine-tuning for production" attr="Dave H on Pexels" attrlink="https://www.pexels.com" >}}

## Two Migration Strategies

There are two approaches to handling false positive tuning during the migration. Neither is universally better — choose based on the size and complexity of your existing setup.

Both strategies describe how you build the CRS 4 exclusion set. They are independent of how you roll the new rule set out to production: you do **not** have to turn your existing WAF off to run either of them. The parallel rollout options that let you keep CRS 3 blocking while you validate CRS 4 are covered in [Running a Safe Production Migration](#running-a-safe-production-migration) below.

### Strategy A: Start Fresh

Discard your existing CRS 3 exclusions entirely and retune from scratch with CRS 4.

**When this makes sense:**
- Your application has changed significantly since you last tuned CRS
- Your CRS 3 exclusion set is large, poorly documented, or has accumulated exclusions whose original reasons are no longer clear
- You run at PL1 with a relatively small exclusion set
- You are migrating to a different WAF engine at the same time

**How to do it:**
1. Install CRS 4.25.0 with a clean `crs-setup.conf` at your target paranoia level
2. Install any required application exclusion plugins (Part 3) but do not add any custom exclusions yet
3. Set the WAF to detection mode (log but do not block)
4. Run detection mode for at least two weeks, covering all application workflows
5. Collect false positives from your WAF logs and add exclusions for legitimate traffic
6. Re-enable blocking when the false positive rate is acceptable

The advantage: you start clean, without carrying forward exclusions that may have masked other issues. The disadvantage: this requires the application traffic to actually exercise all code paths during the detection phase. If you have infrequently-used admin workflows, they must be tested manually.

### Strategy B: Carry Over Existing Exclusions

Map your CRS 3 exclusions to CRS 4 equivalents and migrate them.

**When this makes sense:**
- You run at PL2 or higher with a large, well-maintained exclusion set
- Your application is stable and complex, making a full retune expensive
- You have strong coverage of application traffic in your detection logs from CRS 3

**How to do it:**
1. Follow the exclusion audit described in [Part 5]({{< ref "blog/2026-04-27-migrating-from-crs-3-to-crs-4-part-5-rule-changes.md" >}}) to map each old rule ID to its CRS 4 equivalent
2. Remove exclusions for rules that no longer exist (and verify the underlying issue is gone)
3. Update rule IDs for renamed and renumbered rules
4. Install CRS 4 with the updated exclusion set in detection mode
5. Run detection mode for one to two weeks to catch anything the mapping missed
6. Add new exclusions for any new false positives
7. Re-enable blocking

The advantage: less manual re-testing of application workflows. The disadvantage: you may carry forward exclusions that are now unnecessary, slightly weakening your detection.

## Running a Safe Production Migration

Regardless of which strategy you choose, the migration sequence for production should be:

### Phase 1: Detection-Mode Validation (1-2 weeks)

Run CRS 4 in detection mode for one to two weeks (or until you have observed peak traffic and exercised every critical workflow at least once) so you can review what it would have blocked before any of it actually blocks. There are several ways to set this up. Options A and D are truly parallel — CRS 3 keeps blocking while CRS 4 only records — whereas the others swap CRS 3 for CRS 4 in a single engine and rely on the engine not to block.

**Option A: Dual WAF deployment (true parallel).** Route a copy of your traffic — via traffic mirroring, a sidecar engine, or a dedicated logging endpoint — through a second WAF instance running CRS 4 in detection mode, while your production WAF continues to run CRS 3 in blocking mode. CRS 3 keeps protecting real users; CRS 4 sees the same requests and records what it would have done. Compare the CRS 4 detection log against your access logs to find false positives. This is the safest option and the one to prefer when your environment supports it.

**Option B: Single WAF, detection mode.** If you cannot run a second engine, swap CRS 3 for CRS 4 on your existing WAF and put it in pure detection mode (CRS 3 is no longer active — loading both rule sets naively in one engine collides on rule IDs and anomaly scores; option D below resolves that). You lose blocking for this phase, so only choose this if your threat model allows a temporary gap, for example because you have another upstream protection layer (CDN WAF, edge proxy, application-level controls).

**Option C: Single WAF, anomaly-threshold override.** Some engines do not have a clean detection-only switch, or you want CRS 4 fully wired into the production engine (alerting, audit logs, plugin loading) without it actually blocking. Swap CRS 3 for CRS 4 as in option B, but instead of toggling detection mode, raise the inbound and outbound anomaly score thresholds to a value the score will never reach in practice (for example `9999`). Blocking is technically enabled but functionally disabled — the engine evaluates every rule, you get the score breakdown in your logs, and nothing is rejected. Restore the normal thresholds when you cut over.

**Option D: Single WAF, both rule sets in parallel.** To get truly parallel evaluation without a second engine, the [netnea CRS Upgrading Plugin](https://www.netnea.com/cms/2025/12/18/the-netnea-crs-upgrading-plugin-technical-implementation-details/) renumbers CRS 4's rule IDs and renames its anomaly score variables so both rule sets run side by side in the same engine: CRS 3 keeps blocking real traffic while CRS 4 records what it would have done, and a logging rule tags each request with the ruleset that handled it so you can diff the two verdicts. The plugin can also drive the cut-over, shifting traffic to CRS 4 by path or by percentage sampling until it handles everything, after which you remove CRS 3 and the plugin.

### Phase 2: Validation

After the detection phase, review your CRS 4 detection logs:

- Count distinct rule IDs that fired
- For each firing rule, determine whether the trigger was a legitimate request or actual attack traffic
- For legitimate requests that triggered rules, add targeted exclusions
- Check that known attack traffic you tested is still detected

The CRS 4 per-PL score breakdown in logs (covered in Part 4) makes this easier than it was in CRS 3 — you can see at a glance which paranoia level is responsible for each detection.

### Phase 3: Cut Over

Switch CRS 4 from detection mode to blocking mode by restoring your normal anomaly thresholds. Keep enhanced logging enabled for the first week after cut-over to catch anything the detection phase missed.

## Common False Positive Areas to Check

Based on the changes covered in earlier posts in this series, these are the areas most likely to produce new false positives after the CRS 3 → 4 migration:

**Response-phase web shell rules.** Applications that return debugging output or verbose error messages containing shell-like text. Check your application's error pages, debug endpoints, and admin panels.

**Restricted headers — basic list.** Requests that include `Content-Encoding`, `X-HTTP-Method-Override`, or `Expect`. These are blocked at all paranoia levels. Common sources: upload clients that set `Content-Encoding`, JavaScript frameworks using `X-HTTP-Method-Override` for form method override, and .NET clients using `Expect: 100-continue`. Before adding a WAF exclusion, check whether the client itself can be configured not to send the header — `Expect: 100-continue` from .NET, for example, is controlled by `ServicePointManager.Expect100Continue` (or `HttpClientHandler` in newer code), and adjusting the application is usually preferable to weakening the rule.

**Restricted headers — extended list.** Requests that include `Accept-Charset`. This is only blocked at higher paranoia levels (PL2+) since it still appears in some legitimate clients. If you run at PL1, this will not trigger.

**PL redistribution.** If you run at PL2, some rules that were PL3 in CRS 3 are now PL2 in CRS 4 and will fire where they did not before. The new firings are most common in SQL injection and XSS detection rules.

**Plugin exclusions.** If you use application exclusion plugins (Part 3), the plugin rule IDs are different from the CRS 3 exclusion rule IDs. The plugins may have broader or narrower coverage than the original CRS 3 exclusion files.

## Using the New Reporting Model for Tuning

CRS 4's per-PL score breakdown makes tuning more systematic. For each false positive in your logs:

1. Note the rule ID and the PL it belongs to
2. Note the request URI, method, and the specific parameter that triggered the rule
3. Decide: is this a real false positive (legitimate application behaviour), or is the application doing something it should not?

For real false positives, write the exclusion as narrowly as possible. The CRS-recommended pattern is:

```apache
# In REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
# Exclude rule 941100 (XSS via libinjection) for the /editor/save path
SecRule REQUEST_URI "@beginsWith /editor/save" \
    "id:1001,phase:1,pass,nolog,\
    ctl:ruleRemoveTargetById=941100;ARGS:content"
```

Prefer path-scoped, parameter-scoped exclusions over global rule removals. A global `SecRuleRemoveById 941100` removes XSS detection from your entire application; the above removes it only for the `content` parameter on the specific path where the rich text editor needs it.

## After the Migration: Maintaining Your Exclusion Set

One benefit of migrating to CRS 4.25.0 LTS is that the rule set is stable. The LTS backport policy does not allow new rules, PL changes, or refactoring to land on the LTS branch. This means your exclusions will not be invalidated by LTS point releases — only security fixes are backported, and those are cherry-picked with care.

When a new LTS point release ships (quarterly), review the release notes before upgrading. The release notes will list every change on the LTS branch. If a security fix modifies a rule you have excluded, review your exclusion.

## What's Next

[Part 7]({{< ref "blog/2026-05-11-migrating-from-crs-3-to-crs-4-part-7-engines.md" >}}) covers engine-specific considerations — the support matrix for ModSecurity v2, ModSecurity v3, and Coraza, differences in plugin compatibility across engines, and the new container image tagging scheme.

{{< related-pages "Migration" "CRS-v4" >}}
