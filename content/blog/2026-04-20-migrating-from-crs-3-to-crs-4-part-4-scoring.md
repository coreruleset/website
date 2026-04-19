---
author: fzipi
categories:
  - Blog
date: '2026-04-20T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-thisisengineering-3861957.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 4: Anomaly Scoring and Reporting'
slug: 'migrating-crs-3-to-4-part-4-scoring'
---

This is Part 4 of the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). Part 3 covered the plugin architecture. This post covers anomaly scoring, the reporting model, and paranoia level changes — the areas most likely to affect your baseline after a migration.

{{< figure src="/images/2026/04/pexels-thisisengineering-3861957.jpg" caption="Measuring and scoring every request" attr="ThisIsEngineering on Pexels" attrlink="https://www.pexels.com" >}}

## How Anomaly Scoring Changed

### The CRS 3 Model

In CRS 3, every rule that fires adds to a single transaction variable `tx.anomaly_score`. At the end of phase 2 (for inbound) and phase 4 (for outbound), the total accumulated score is compared against `tx.inbound_anomaly_score_threshold` and `tx.outbound_anomaly_score_threshold`. If the score exceeds the threshold, the request is blocked.

This model is simple but has one significant weakness: you cannot tell from the final score alone which paranoia levels contributed to it. A score of `15` at PL2 might come from three PL1 rules or one PL2 rule, and the log entry for the blocking action does not distinguish between them.

### The CRS 4 Model

CRS 4 refactored the anomaly scoring variables for consistency. The **threshold** variable names are unchanged — you still configure `tx.inbound_anomaly_score_threshold` and `tx.outbound_anomaly_score_threshold` in `crs-setup.conf` exactly as in CRS 3.

What changed is the internal score accumulation and how the per-severity increments are named. The per-severity scoring variables are:

```apache
# These existed in CRS 3 and carry over to CRS 4 unchanged:
tx.critical_anomaly_score = 5
tx.error_anomaly_score    = 4
tx.warning_anomaly_score  = 3
tx.notice_anomaly_score   = 2
```

In CRS 3, the running total was accumulated in `tx.anomaly_score`. In CRS 4 the internal accumulation was refactored so that scores are tracked in a way that correlates with the paranoia level of the firing rule. The details are inside the engine rules — the operator-facing variables you configure (`tx.inbound_anomaly_score_threshold`, the severity scores) are unchanged.

The visible change is in what gets reported. CRS 4 reporting rules (see the Reporting Model section below) include more structured context about which paranoia level and rule category contributed to the score, making it significantly easier to understand what drove a blocking action.

### Impact on Custom Rules

If you have custom rules or Lua scripts that read `tx.anomaly_score` directly — for example, to make a routing decision mid-request — those rules need to be verified against CRS 4. Check your WAF configuration for any `@eq`/`@gt` checks against `tx.anomaly_score` and test that they behave as expected after upgrading.

## The Reporting Model

### CRS 3 Reporting: 980xxx Rules

CRS 3 had a set of `980xxx` reporting rules that fired when a request exceeded the anomaly threshold. These rules were redundant — one for each combination of inbound/outbound and paranoia level — and produced noisy, repetitive log entries. The reporting model was widely criticised as difficult to parse and easy to misconfigure.

### CRS 4 Reporting: Granular Control

CRS 4 replaces the `980xxx` rules with a new, more structured reporting system controlled by `tx.reporting_level`. There is a single reporting action per direction in phase 5, governed by logic that decides *when* it fires based on the level you configure. The result is cleaner logs and operator control over verbosity.

The six reporting levels (configured via rule 900115) are:

| Level | Behaviour |
|---|---|
| `0` | Reporting disabled |
| `1` | Report when blocking anomaly score ≥ threshold |
| `2` | Report when detection anomaly score ≥ threshold |
| `3` | Report when blocking anomaly score > 0 |
| `4` | Report when detection anomaly score > 0 (default) |
| `5` | Report all requests |

The default is `4`, which is more verbose than CRS 3. This is intentional — the extra log output at level 4 is the mechanism that shows you near-miss requests (requests that scored above zero but did not hit the blocking threshold), which is essential for tuning.

The practical migration impact: if you have SIEM rules, alerting logic, or log parsers that match on `980xxx` rule IDs, update them to the new CRS 4 reporting rule IDs. Also, the log message format changed — run your log parser against a sample of CRS 4 output before cutting over.

## Early Blocking

The `tx.early_blocking` option (covered in detail in Part 2) changes the phase at which anomaly score evaluation can occur:

| Mode | Inbound evaluation | Outbound evaluation |
|---|---|---|
| `tx.early_blocking` unset (default) | End of phase 2 | End of phase 4 |
| `tx.early_blocking=1` | End of phase 1 *and* phase 2 | End of phase 3 *and* phase 4 |

With early blocking enabled, a request that trips a phase-1 rule (primarily header-based rules) can be blocked before the WAF processes the request body. This reduces latency for clearly malicious requests and reduces WAF load for attack traffic that signals itself early in the connection.

The trade-off: if a request's score does not exceed the threshold based on headers alone but would have exceeded it after body inspection, early blocking will not block it in phase 1 — it will still be blocked in phase 2 as usual. Early blocking is additive, not a replacement.

For migration, leave `tx.early_blocking` commented out (disabled). This matches CRS 3 behaviour exactly. After your initial migration is stable and your false positive rate is under control, consider enabling it.

## Paranoia Level Redistribution

CRS 4 made a broad effort to better distribute rules across paranoia levels. In CRS 3, PL1 carried a disproportionately large fraction of the total rule count. Many rules that were quite specialised or had higher false positive rates were at PL1 simply because PL2–PL4 were underused.

In CRS 4, a significant number of rules were moved from lower to higher paranoia levels. The direction was almost always toward higher PLs — rules moved up, not down.

### What This Means for You

**If you run at PL1:** Your anomaly score baseline will likely *decrease* after migration. Rules that previously fired at PL1 in CRS 3 may now only fire at PL2 or higher. This is generally good — fewer false positives at PL1 — but it also means some attacks you were detecting at PL1 in CRS 3 may now only be detected at PL2 in CRS 4. Review your threat model.

**If you run at PL2 or higher:** Your baseline may increase. Rules that were at PL1 in CRS 3 are now at PL2, so at PL2 you are covering more detection than before. This is the intended direction, but it means more tuning may be needed after the migration.

**If you have PL-specific exclusions:** Some of your exclusions may no longer be necessary if the rules they targeted moved to a higher PL than the one you run at. Conversely, new rules may fire at your PL that were not present in CRS 3. After the migration, run in detection mode for at least a week before enabling blocking to establish a new baseline.

## Verifying Your Scoring Setup

After installing CRS 4 with your migrated configuration, verify that scoring is working as expected by sending a test request that should trigger detection. The CRS documentation and the [go-ftw](https://github.com/coreruleset/go-ftw) testing framework provide test cases for this purpose.

A simple check: send a request containing a known attack pattern at your configured paranoia level and confirm that:

1. The rule fires (visible in access or audit logs)
2. The anomaly score variables are populated correctly
3. The reporting rule fires and logs the expected block action

If you have an anomaly score below the threshold but a rule fired, the per-PL breakdown in the CRS 4 logs will show you exactly which paranoia level bucket the score landed in.

## What's Next

[Part 5]({{< ref "blog/2026-04-27-migrating-from-crs-3-to-crs-4-part-5-rule-changes.md" >}}) covers the rule-level changes — new detection categories, removed and reorganized rules, RE2/Hyperscan compatibility, and how to audit your existing `SecRuleRemoveById` exclusions against the CRS 4 rule set.

{{< related-pages "Migration" "CRS-v4" >}}
