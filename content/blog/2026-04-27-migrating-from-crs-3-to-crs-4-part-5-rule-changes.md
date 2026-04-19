---
author: fzipi
categories:
  - Blog
date: '2026-04-27T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-egorkomarov-8824026.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 5: Rule Changes'
slug: 'migrating-crs-3-to-4-part-5-rule-changes'
---

This is Part 5 of the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). Part 4 covered anomaly scoring and reporting. This post covers the rule-level changes: what is new, what is gone, what moved, and how to audit your existing exclusions against the CRS 4 rule set.

{{< figure src="/images/2026/04/pexels-egorkomarov-8824026.jpg" caption="Hundreds of rules changed under the hood" attr="Egor Komarov on Pexels" attrlink="https://www.pexels.com" >}}

## The Scale of Change

There are approximately 500 changes between CRS 3.3 and CRS 4.0. This is not a point release — it is the result of years of accumulated improvements, a bug bounty programme that produced over 180 reports, and deliberate architectural cleanup. Understanding the shape of this change helps you plan your tuning work.

The changes fall into four categories:

1. **New rules and new detection categories** — coverage that did not exist in CRS 3
2. **Modified rules** — rules that exist in both versions but with changed patterns, PL assignments, or IDs
3. **Removed rules** — rules that were dropped because they were superseded, redundant, or false-positive-prone
4. **Reorganized rules** — rules that were split, merged, or renumbered

The authoritative source for all of this is the [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md) in the CRS 4.0 release. This post walks through the most significant categories. For a full audit of your specific exclusions, you will need to cross-reference CHANGES.md with your existing configuration.

## New: Web Shell Detection in Responses

One of the most significant new detection capabilities in CRS 4 is response-phase web shell detection. CRS 3 focused almost entirely on inspecting inbound requests. CRS 4 adds a dedicated file, `RESPONSE-955-WEB-SHELLS.conf`, with rules in the `955xxx` range that inspect HTTP responses for indicators of web shell activity — command output patterns, PHP error messages triggered by shell execution, and other post-exploitation signals.

This matters for migration in two ways:

**New coverage you gain immediately.** These rules require no configuration — they fire at the default paranoia level when a response matches a known web shell indicator.

**Potential for new false positives.** Applications that return debugging output, error messages containing shell-like text, or system information in responses may trigger these rules. Run in detection mode after the migration and review response-phase rule firings before enabling blocking.

## New: HTTP/3 Support

CRS 4 adds rules that correctly handle HTTP/3 semantics. For most operators this is invisible — your WAF engine handles the protocol level, not CRS. But if you use a WAF engine that passes HTTP/3-specific headers or pseudo-headers to the rule set, CRS 4 handles them correctly where CRS 3 would have misbehaved or missed them.

## Changed: HTTP/0.9 Tolerance Dropped

HTTP/0.9 was already absent from the default `tx.allowed_http_versions` list in CRS 3.3, so the protocol enforcement rule in `REQUEST-920` has been blocking it by default in both versions. What changed in CRS 4 is narrower: response-splitting detection (rule `921110`) used to carve out an HTTP/0.9 pattern to avoid false positives on legacy clients, and that carve-out was removed. See the "drop HTTP/0.9 support" change in [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md) (PR #1966).

For most operators this is invisible at migration time. If you explicitly allowed HTTP/0.9 in CRS 3 by adding it to `tx.allowed_http_versions`, the same configuration continues to work in CRS 4, but rule `921110` will no longer tolerate HTTP/0.9 in its regex. Monitoring agents that still speak HTTP/0.9 should be updated to HTTP/1.0 or later regardless.

## Changed: Restricted Headers

CRS 4 restructured restricted headers into two categories with different enforcement behaviour (covered in detail in Part 2). From a rule-change perspective, the key additions are:

**Basic restricted headers** (blocked at all paranoia levels, new in CRS 4). The full default list in `tx.restricted_headers_basic` is:
- `content-encoding` — compressed request bodies bypass WAF inspection
- `proxy` — HTTPoxy (CVE-2016-5385) and related upstream request smuggling
- `lock-token`, `content-range`, `if` — WebDAV headers misused by uncommon clients
- `x-http-method-override`, `x-http-method`, `x-method-override` — method override attack prevention
- `x-middleware-subrequest` — CVE-2025-29927 (Next.js)
- `expect` — HTTP desync attack prevention

**Extended restricted headers** (blocked at higher paranoia levels):
- `accept-charset` — deprecated header, possible response WAF bypass; present in the extended list, not blocked at PL1

If your applications send any of the basic headers in requests, you will see blocks immediately after migration at PL1. The `accept-charset` header only triggers at higher paranoia levels.

## Changed: Regular Expression Engine Compatibility

All formerly PCRE-only regular expressions in CRS 4 are now compatible with RE2 and Hyperscan. This change has no direct impact on operators using PCRE-based engines (ModSecurity v2, most ModSecurity v3 builds). It matters if:

- You use a Coraza build that has been compiled with a non-PCRE engine
- Your WAF vendor uses RE2 or Hyperscan for performance

The practical implication is that CRS 4 is portable in ways CRS 3 was not. Some PCRE-specific features (lookaheads, lookbehinds, backreferences) were removed or refactored. If you have custom rules that rely on PCRE-specific syntax and you plan to migrate to a non-PCRE engine in the future, be aware that you will face similar constraints.

## Auditing Your Existing Exclusions

The part of rule changes that requires the most work from you is mapping your existing exclusions to CRS 4.

### Step 1: Collect Your Existing Rule IDs

Extract every rule ID you have explicitly excluded or targeted in your WAF configuration:

```bash
# Find all SecRuleRemoveById, SecRuleUpdateTargetById, etc.
grep -r 'SecRule\|ctl:ruleRemove\|ctl:ruleUpdate' /path/to/your/waf-config/ \
  | grep -oE '[0-9]{6,}' | sort -u
```

This gives you a list of rule IDs your tuning depends on.

### Step 2: Check Each ID Against CHANGES.md

For each rule ID you found in Step 1, search for it in [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md). Specifically, look for:

- **Removed**: the rule no longer exists. Your exclusion is now a no-op. If you added it to fix a false positive, that false positive may have been fixed in CRS 4 — or the rule may have been renumbered. Test and remove the exclusion if it is no longer needed.
- **Renumbered**: the rule exists under a new ID. Update your exclusion to reference the new ID.
- **Split**: the rule was broken into multiple rules with new IDs. Update your exclusion to cover the relevant new IDs.
- **Moved to plugin**: the rule is now in a plugin, not in core. You need to install the plugin and the exclusion still applies — but now against the plugin's version of the rule.

### Step 3: Verify the Remaining Exclusions in Detection Mode

After updating your exclusions for renamed and removed rules, run CRS 4 in detection mode (anomaly scoring only, no blocking) for a representative period. This reveals:

- Rules that now fire where they did not in CRS 3 (new exclusions needed)
- Exclusions that are no longer needed (the underlying false positive was fixed)
- Score changes at your paranoia level due to PL redistribution

This step cannot be skipped. The combination of rule reorganization and PL redistribution means your anomaly score baseline will be different from CRS 3, even if you carefully map every exclusion.

## Rule File Organization

CRS 4 preserves the familiar `REQUEST-9xx-*.conf` and `RESPONSE-9xx-*.conf` naming convention. The numbering within each file and some file boundaries changed, but the overall organization is similar enough that you can navigate CRS 4 files if you know CRS 3.

A notable addition: CRS 4 ships with `REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example` and `RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example` as officially supported places to add your custom exclusions. These files are the CRS-blessed approach to exclusion management. If your current exclusions are scattered across your WAF configuration, consider consolidating them into these files during the migration.

## What's Next

[Part 6]({{< ref "blog/2026-05-04-migrating-from-crs-3-to-crs-4-part-6-tuning.md" >}}) covers the practical approach to false positive tuning during the migration — two strategies for carrying over your existing tuning, how to run a production migration safely, and common false positives that changed between versions.

{{< related-pages "Migration" "CRS-v4" >}}
