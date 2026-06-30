---
title: 'CRS version 4.25.1 LTS released'
date: '2026-06-30'
author: fzipi
categories:
    - Blog
tags:
    - CRS-News
    - Release
draft: true
---

The OWASP CRS team is pleased to announce the release of **CRS v4.25.1**, the first patch release on our LTS-4.25 branch. This release fixes two high-severity security vulnerabilities alongside a set of false-positive reductions and regex hardening backports. All users on the CRS 4.25.x LTS line are strongly encouraged to update.

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/docs/deployment/install/) page.

## Security fixes

### XML attribute value bypass (GHSA-6jp8-c2w2-x7wr)

**Severity:** HIGH — CVSS 3.1 score 7.2 (`AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)  
**CWE:** CWE-138 — Improper Neutralization of Special Elements

#### Impact

CRS rules in the 921 (protocol-attack), 930 (LFI), 931 (RFI), 932 (RCE), 933 (PHP), 934 (generic), 941 (XSS), 942 (SQLi), and 943 (session-fixation) families inspect XML request bodies using the XPath expression `XML:/*`. That expression matches element text nodes only — it does **not** match XML attribute values. An attacker who places an attack payload inside an XML attribute (e.g. `<a href="javascript:alert(1)=window.name"></a>` or `<a value="' OR 1=1 --"></a>`) bypasses CRS detection entirely.

The bypass affects approximately 159 rules across nine rule files and applies at **every paranoia level (PL1 through PL4)**. The 944 (Java) family already correctly includes `XML://@*` and is therefore unaffected.

**Who is impacted:** Deployments that protect applications which parse XML request bodies (SOAP, REST/XML, ATOM, XML-RPC, XML config endpoints, etc.) where ModSecurity's XML body processing is enabled. Deployments that do not accept XML bodies, or that block XML content types upstream, are not impacted.

#### Workaround for users unable to update immediately

Until you can deploy v4.25.1, you can mitigate by adding the following directives to your local configuration (e.g. a file loaded after CRS):

```apache
SecRuleUpdateTargetByTag "attack-protocol"  "XML://@*"
SecRuleUpdateTargetByTag "attack-lfi"       "XML://@*"
SecRuleUpdateTargetByTag "attack-rfi"       "XML://@*"
SecRuleUpdateTargetByTag "attack-rce"       "XML://@*"
SecRuleUpdateTargetByTag "attack-php"       "XML://@*"
SecRuleUpdateTargetByTag "attack-generic"   "XML://@*"
SecRuleUpdateTargetByTag "attack-xss"       "XML://@*"
SecRuleUpdateTargetByTag "attack-sqli"      "XML://@*"
SecRuleUpdateTargetByTag "attack-fixation"  "XML://@*"
```

This change is purely additive — it inspects an additional XPath axis without altering existing matches or transformations.

#### Full advisory

The full advisory will be published at [GHSA-6jp8-c2w2-x7wr](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-6jp8-c2w2-x7wr) once the associated CVE has been assigned and published. We will update this post with the CVE number at that time.

Credit goes to [@HackingRepo](https://github.com/HackingRepo) for reporting this issue and to [@theseion](https://github.com/theseion) for the fix.

### Unix RCE ReDoS in shared regex-assembly include (GHSA-f5qm-3h4p-8qhg)

**Severity:** HIGH — CVSS score pending  
**CWE:** CWE-1333 — Inefficient Regular Expression Complexity

#### Impact

A regular-expression denial of service (ReDoS) affects the shared include file `regex-assembly/include/unix-shell-evasion-prefix.ra`, which is used to build **12 Unix RCE detection rules**: 932220, 932230, 932231, 932232, 932235, 932236, 932238, 932239, 932250, 932260, 932340, and 932350.

A single unauthenticated crafted request drives PCRE2 past its backtracking limit on the generated pattern. When PCRE2 exceeds that limit, the `@rx` operator returns an error rather than a match result, which has two consequences:

- **Detection bypass** — the affected rule fails to evaluate for that request, so the RCE payload is not inspected.
- **CPU denial of service** — the engine burns CPU exploring the ambiguous pattern on every such request.

**Root cause:** The commands-prefix group in the shared include has an ambiguous whitespace-handling alternation inside a `*` quantifier. A whitespace run between prefix tokens can be consumed by more than one quantifier (the trailing `\s*` of one iteration and the leading `\s*` of the next), so the number of parse paths grows combinatorially with the length of the run. This has been confirmed reproducible with `pcre2test` 10.47.

**Who is affected:** Deployments running CRS on **ModSecurity v2 or v3** (both link against PCRE2). **Coraza (RE2) is not affected** — RE2 does not backtrack.

#### Workaround for users unable to update immediately

There is no workaround that fully preserves detection without applying the patch:

- **Run CRS on a RE2-based engine (Coraza).** RE2 is not affected.
- **Constrain request size.** Tighter `SecRequestBodyLimit` and argument-length limits reduce exploitability but do not eliminate it.
- Lowering `SecPcreMatchLimit` / `SecPcreMatchLimitRecursion` makes the engine error sooner (less CPU per request) but does **not** remove the detection bypass — the rule still fails to evaluate when the limit is hit.
- Disabling the affected rules removes the DoS exposure but also removes the RCE detection they provide, and is not recommended.

#### Full advisory

The full advisory will be published at [GHSA-f5qm-3h4p-8qhg](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-f5qm-3h4p-8qhg) once the associated CVE has been assigned and published. We will update this post with the CVE number at that time.

## Regex hardening: exponential backtracking removed

Three rules carrying structurally ambiguous alternations that could lead to catastrophic backtracking on non-PCRE2 engines have been corrected. PCRE2 users (ModSecurity) were already protected by auto-possessification and required-literal optimizations, but engines using Oniguruma, Python `re`, or other backtracking engines were exposed. The fixes are purely additive in detection terms — all existing positive tests continue to pass.

- **Rules 933160 and 933161** — PHP function-call detection: the optional whitespace/comment suffix between the function name and the opening `(` now uses unrolled comment forms and newline-anchored line-comment branches, removing the overlap between the whitespace and comment branches under the `*` quantifier. ([#4666](https://github.com/coreruleset/coreruleset/pull/4666))
- **Rule 933180** — PHP variable function calls: the "noise" group between the variable name and call `(...)` now uses bounded bracket/brace forms and the unrolled block-comment pattern instead of free `.+`/`.*`, eliminating the shared-character ambiguity under the outer `*` quantifier. ([#4669](https://github.com/coreruleset/coreruleset/pull/4669))
- **Rule 941140** — CSS `url(javascript:...)` XSS detection: the declaration-list loop value changed from free `.+` to `[^;]+`, bounding it at the declaration separator and removing the ambiguity with the adjacent key pattern. The rule has been migrated from an inline pattern to `regex-assembly/941140.ra`. ([#4670](https://github.com/coreruleset/coreruleset/pull/4670))

## False-positive reductions

- **Rules 920240 and 920400** — These rules validate URL-encoded request bodies and enforce file-size limits. They previously relied solely on the `Content-Type` header to determine if a request body is URL-encoded, which could fail for applications that send URL-encoded data with non-standard content types such as `text/plain`. They now use the `REQBODY_PROCESSOR` variable, which is set by the engine based on the actual body processor in use, making them more robust in non-standard configurations. ([#4639](https://github.com/coreruleset/coreruleset/pull/4639))
- **Rule 942200** — SQL injection detection: a regression introduced by an earlier false-positive fix caused user-agent strings containing a comma but no surrounding whitespace to be blocked incorrectly. The rule's comment-handling logic has been refined to cover these cases. ([#4608](https://github.com/coreruleset/coreruleset/pull/4608))
- **Parameter name `.history`** — Matching against the string `.history` was producing substring false positives, e.g. triggering on the parameter name `history.history`. A word boundary has been added to restrict the match to actual `.history` file access attempts. ([#4614](https://github.com/coreruleset/coreruleset/pull/4614))
- **Unix RCE (PL1) — `pg` command** — The `pg` command has been removed from the PL1 Unix command list. It is not installed by default on most Linux distributions and was causing false positives in application traffic. ([#4613](https://github.com/coreruleset/coreruleset/pull/4613))
- **Internal bug fix 4RI-250413** — An additional bug fix addresses an internally tracked issue. ([#4672](https://github.com/coreruleset/coreruleset/pull/4672))

## Protocol enforcement

- **Rule 920100** — Request line validation: support for HTTP/0.9 bare `GET` requests (without a protocol suffix) has been removed. HTTP/0.9 is obsolete per RFC 9110, and the earlier rule 920430 already excluded it from the allowed HTTP versions list by default. The HTTP/0.9 branch was the only alternative in rule 920100 that did not require a protocol version, creating an inconsistency that has now been resolved. ([#4621](https://github.com/coreruleset/coreruleset/pull/4621))

## Setup improvement

- **`crs-setup.conf.example`** — `SecDefaultAction` directives for phases 3, 4, and 5 are now defined in anomaly scoring mode. Without explicit default actions for these phases, some engines (notably Coraza) may fall back to engine-level defaults, leading to inconsistent logging and auditing behavior across backends. The new directives make CRS behavior consistent regardless of the WAF engine in use. ([#4675](https://github.com/coreruleset/coreruleset/pull/4675))

## Upgrading

The release is available on [GitHub](https://github.com/coreruleset/coreruleset/releases/tag/v4.25.1). Given the two high-severity security fixes included in this release, all deployments on the CRS 4.25.x LTS line should update promptly. Users on the CRS 4.x main branch will receive the same security fixes in a forthcoming release.

**nginx + libmodsecurity3 users:** update libmodsecurity3 to **v3.0.16** alongside this CRS release. v3.0.16 is required for the XML attribute bypass fix (GHSA-6jp8-c2w2-x7wr) to take full effect on that stack.

If you have questions or concerns, please reach out via the [CRS GitHub repository](https://github.com/coreruleset/coreruleset), in our Slack channel (#coreruleset on [owasp.slack.com](https://owasp.slack.com/)), or on our [mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project).

Sincerely,  
Felipe Zipitria on behalf of the CRS development team
