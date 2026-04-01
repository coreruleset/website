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

### Phase 1: Parallel Detection (1-2 weeks)

Run CRS 4 in detection mode in parallel with your existing CRS 3 blocking setup. There are a few ways to achieve this:

**Dual WAF deployment.** Route a copy of your traffic (via mirroring or a dedicated logging endpoint) through CRS 4 in detection mode, while CRS 3 continues blocking for real traffic. Compare the CRS 4 detection results against known good requests in your access logs.

**Single WAF, detection mode.** If a parallel setup is not practical, swap CRS 3 for CRS 4 in pure detection mode. You lose blocking during this phase, so only do this if your threat model allows a temporary blocking gap (e.g. you have another upstream protection layer).

**WAF-engine anomaly logging.** Some WAF engine setups allow you to log anomaly score results without blocking, even when blocking is technically enabled, by setting the anomaly threshold very high (e.g. `9999`). Set your CRS 4 thresholds to `9999` during the detection phase so that nothing is blocked even if the score exceeds the normal threshold.

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

**Restricted headers — basic list.** Requests that include `Content-Encoding`, `X-HTTP-Method-Override`, or `Expect`. These are blocked at all paranoia levels. Common sources: upload clients that set `Content-Encoding`, JavaScript frameworks using `X-HTTP-Method-Override` for form method override, and .NET clients using `Expect: 100-continue`.

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
    "id:1001,phase:2,pass,nolog,\
    ctl:ruleRemoveTargetById=941100;ARGS:content"
```

Prefer path-scoped, parameter-scoped exclusions over global rule removals. A global `SecRuleRemoveById 941100` removes XSS detection from your entire application; the above removes it only for the `content` parameter on the specific path where the rich text editor needs it.

## After the Migration: Maintaining Your Exclusion Set

One benefit of migrating to CRS 4.25.0 LTS is that the rule set is stable. The LTS backport policy does not allow new rules, PL changes, or refactoring to land on the LTS branch. This means your exclusions will not be invalidated by LTS point releases — only security fixes are backported, and those are cherry-picked with care.

When a new LTS point release ships (quarterly), review the release notes before upgrading. The release notes will list every change on the LTS branch. If a security fix modifies a rule you have excluded, review your exclusion.

## What's Next

[Part 7]({{< ref "blog/2026-05-11-migrating-from-crs-3-to-crs-4-part-7-engines.md" >}}) covers engine-specific considerations — the support matrix for ModSecurity v2, ModSecurity v3, and Coraza, differences in plugin compatibility across engines, and the new Docker image tagging scheme.

*Felipe Zipitria, CRS Co-Lead*
