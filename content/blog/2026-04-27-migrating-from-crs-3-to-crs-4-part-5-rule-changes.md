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

There are hundreds of rule-level changes between CRS 3.3 and CRS 4.0. This is not a point release — it is the result of years of accumulated improvements, a public bug bounty programme, and deliberate architectural cleanup. Understanding the shape of this change helps you plan your tuning work.

The changes fall into four categories:

1. **New rules and new detection categories** — coverage that did not exist in CRS 3
2. **Modified rules** — rules that exist in both versions but with changed patterns, PL assignments, or IDs
3. **Removed rules** — rules that were dropped because they were superseded, redundant, or prone to false positives
4. **Reorganized rules** — rules that were split, merged, or renumbered

The authoritative source for all of these changes is the [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/main/CHANGES.md) in the CRS 4.0 release. This post walks through the most significant categories. For a full audit of your specific exclusions, you will need to cross-reference CHANGES.md with your existing configuration.

### A Note on the CRS 4.25 LTS Cadence

CRS 4.25 is a Long-Term Support release. After the initial release, the 4.25 line receives periodic patch releases (4.25.1, 4.25.2, …) that carry targeted fixes and selected backports from main. This means "CRS 4.25 LTS" is a moving target for the better: your migration baseline is 4.25.0, and you will apply patch releases on your existing deployment over time. Throughout this post, when a change is described as "coming in 4.25.1", it will reach you on the next quarterly LTS patch — no major version upgrade required.

## Rule File Organization

CRS 4 preserves the familiar `REQUEST-9xx-*.conf` and `RESPONSE-9xx-*.conf` naming convention. The numbering within each file and some file boundaries changed, but the overall organization is similar enough that you can navigate CRS 4 files if you know CRS 3.

A notable addition: CRS 4 ships with `REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example` and `RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example` as officially supported places to add your custom exclusions. These files are the CRS-blessed approach to exclusion management. If your current exclusions are scattered across your WAF configuration, consider consolidating them into these files during the migration.

## New: Web Shell Detection in Responses

One of the most significant new detection capabilities added in CRS 4.0 (and carried forward to 4.25 LTS) is response-phase web shell detection. CRS 3 focused almost entirely on inspecting inbound requests. CRS 4 adds a dedicated file, `RESPONSE-955-WEB-SHELLS.conf`, with rules in the `955xxx` range (PL1 for 955100–955340, PL2 for 955350) that inspect HTTP responses for indicators of web shell activity — command output patterns, PHP error messages triggered by shell execution, and other post-exploitation signals.

This matters for migration in two ways:

**New coverage you gain immediately.** These rules require no configuration — they fire at the default paranoia level when a response matches a known web shell indicator.

**Potential for new false positives.** Applications that return debugging output, error messages containing shell-like text, or system information in responses may trigger these rules. Run in detection mode after the migration and review response-phase rule firings before enabling blocking.

## New: HTTP/3 Allowed by Default

CRS 4.0 added `HTTP/3` and `HTTP/3.0` to the default `tx.allowed_http_versions` list and accounts for the HTTP/2+ reality that `Transfer-Encoding` is not used (per RFC 9114 §4.1) in the protocol-enforcement rules. Most CRS detection is transport-agnostic — it inspects parsed variables such as `ARGS`, `REQUEST_URI`, and `REQUEST_HEADERS` that the WAF engine populates regardless of the underlying HTTP version — so moving clients from HTTP/1.1 to HTTP/3 does not change detection behaviour at the rule level. If you were running CRS 3 with HTTP/3 clients, you likely had to add `HTTP/3` to your `tx.allowed_http_versions` manually; in CRS 4 this is no longer necessary.

## Changed: HTTP/0.9 Tolerance Dropped

HTTP/0.9 has been progressively removed from CRS over several releases. The protocol is obsolete per [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) and is absent from the default `tx.allowed_http_versions` list — but because HTTP/0.9 requests carry no protocol string at all, the version-list check in rule `920430` only catches them when the engine populates `REQUEST_PROTOCOL` with a default. Two other rules did the real work of blocking HTTP/0.9, and both have been tightened:

- **CRS 4.0** — response-splitting detection (rule `921110`) used to carve out an HTTP/0.9 pattern to avoid false positives on legacy clients, and that carve-out was removed. See the "drop HTTP/0.9 support" change in [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/main/CHANGES.md) (PR #1966).
- **CRS 4.25.1** (first quarterly LTS backport, scheduled) — request-line validation (rule `920100`) had a dedicated alternative that accepted `GET /path` without any protocol suffix, preserving HTTP/0.9 compatibility. That alternative was removed (PR [`#4621`](https://github.com/coreruleset/coreruleset/pull/4621)) on main and will be backported to the 4.25 LTS line in the first quarterly 4.25.1 release. After this change, `GET /\r\n\r\n` style requests will trigger `920100` and will be blocked.

Once 4.25.1 ships, HTTP/0.9 is effectively blocked by CRS. Adding `HTTP/0.9` to `tx.allowed_http_versions` no longer helps — rule `920100` blocks the request at the request-line level before the protocol-version check in rule `920430` is even reached. If you have monitoring agents or legacy clients that still speak HTTP/0.9, they must be updated to HTTP/1.0 or later before you deploy 4.25.1, or they will start getting blocked.

## Changed: Restricted Headers

CRS 4.0 restructured restricted headers into two categories with different enforcement behaviour (covered in detail in Part 2). From a rule-change perspective, the key additions are:

**Basic restricted headers** (blocked at all paranoia levels, introduced in CRS 4.0). The full default list in `tx.restricted_headers_basic` is:
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

- You use Coraza (Go's `regexp` package is RE2-based, always)
- Your WAF vendor uses RE2 or Hyperscan for performance

The practical implication is that CRS 4 is portable in ways CRS 3 was not. PCRE-only features (lookaheads, lookbehinds, backreferences) were removed or refactored to RE2-compatible alternatives. If you have custom rules that rely on PCRE-specific syntax and you plan to migrate to a non-PCRE engine in the future, you will face similar constraints.

## Auditing Your Existing Exclusions

The part of rule changes that requires the most work from you is mapping your existing exclusions to CRS 4.

### Step 1: Collect Your Existing Rule IDs

Extract every rule ID you have explicitly excluded or targeted in your WAF configuration:

```bash
# Find all SecRuleRemoveById, SecRuleUpdateTargetById, ctl:ruleRemove*, ctl:ruleUpdate*
grep -rhE 'SecRuleRemoveById|SecRuleUpdate|ctl:ruleRemove|ctl:ruleUpdate' /path/to/your/waf-config/ \
  | grep -oE '\b[0-9]{6}\b' | sort -u
```

This gives you a list of rule IDs your tuning depends on.

### Step 2: Check Each ID Against CHANGES.md

For each rule ID you found in Step 1, search for it in [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/main/CHANGES.md). Specifically, look for:

- **Removed**: the rule no longer exists. Your exclusion is now a no-op. If you added it to fix a false positive, that false positive may have been fixed in CRS 4 — or the rule may have been renumbered. Test and remove the exclusion if it is no longer needed.
- **Renumbered**: the rule exists under a new ID. Update your exclusion to reference the new ID.
- **Split**: the rule was broken into multiple rules with new IDs. Update your exclusion to cover the relevant new IDs.
- **Moved to plugin**: the rule is now in a plugin, not in core. You need to install the plugin and the exclusion still applies — but now against the plugin's version of the rule.

### Step 3: Verify the Remaining Exclusions in Detection Mode

After updating your exclusions for renamed and removed rules, run CRS 4 in detection mode (anomaly scoring only, no blocking) for a representative period. This reveals:

- Rules that now fire where they did not in CRS 3 (new exclusions needed)
- Exclusions that are no longer needed (the underlying false positive was fixed)
- Score changes at your paranoia level due to PL redistribution

This step must not be skipped. The combination of rule reorganization and PL redistribution means your anomaly score baseline will be different from CRS 3, even if you carefully map every exclusion.

## What's Next

[Part 6]({{< ref "blog/2026-05-04-migrating-from-crs-3-to-crs-4-part-6-tuning.md" >}}) covers the practical approach to false positive tuning during the migration — two strategies for carrying over your existing tuning, how to run a production migration safely, and common false positives that changed between versions.

{{< related-pages "Migration" "CRS-v4" >}}
