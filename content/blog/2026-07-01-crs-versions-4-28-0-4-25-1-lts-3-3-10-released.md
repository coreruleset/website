---
title: 'CRS versions 4.28.0, 4.25.1 LTS, and 3.3.10 released'
date: '2026-07-02'
author: fzipi
categories:
    - Blog
tags:
    - CRS-News
    - Release
---

The OWASP CRS team is pleased to announce three coordinated releases today: **v4.28.0** (main branch), **v4.25.1** (v4 LTS), and **v3.3.10** (v3 LTS). All three fix the same two high-severity security vulnerabilities that affect all previous CRS releases. Users on any supported branch are strongly encouraged to update.

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/docs/deployment/install/) page.

## Security fixes

Both vulnerabilities affect all three release lines.

### XML attribute value bypass ([GHSA-6jp8-c2w2-x7wr](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-6jp8-c2w2-x7wr))

**Severity:** HIGH — CVSS 3.1 score 7.2 (`AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)  
**CWE:** CWE-138 — Improper Neutralization of Special Elements

#### Impact

CRS rules in the 921 (attacks targeting HTTP protocol), 930 (LFI - Local File Inclusion), 931 (RFI - Remote File Inclusion), 932 (RCE), 933 (PHP), 934 (generic), 941 (XSS), 942 (SQLi), and 943 (session-fixation) families inspect XML request bodies using the XPath expression `XML:/*`. That expression matches element text nodes only — it does **not** match XML attribute values. An attacker who places an attack payload inside an XML attribute (e.g. `<a href="javascript:alert(1)=window.name"></a>` or `<a value="' OR 1=1 --"></a>`) bypasses CRS detection entirely.

The bypass affects approximately 159 rules across nine rule files and applies at **every paranoia level (PL1 through PL4)**. The 944 (Java) family already correctly includes `XML://@*` and is therefore unaffected.

**Who is impacted:** Deployments that protect applications which parse XML request bodies (SOAP, REST/XML, ATOM, XML-RPC, XML config endpoints, etc.) where ModSecurity's XML body processing is enabled. Deployments that do not accept XML bodies, or that block XML content types upstream, are not impacted.

#### Opt-in gate on LTS branches (v4.25.1 and v3.3.10)

On the LTS branches the fix ships behind a runtime gate (`tx.crs_xml_attr_inspect`) so operators can stage the rollout. It is **enabled by default** — no action is needed to get the protection. Operators who need to temporarily disable it can add the following to their local configuration:

```apache
SecAction "id:900130,phase:1,nolog,pass,\
    setvar:tx.crs_xml_attr_inspect=0"
```

**v4.28.0** ships the fix unconditionally with no gate.

#### ModSecurity v2 (Apache) — LTS branches

**ModSecurity 2.9.14** (released 2026-07-02) fixes the `ctl:ruleRemoveTargetByTag` bug that prevented the opt-out gate from working on that engine ([owasp-modsecurity/ModSecurity#3592](https://github.com/owasp-modsecurity/ModSecurity/issues/3592)). ModSecurity v2/Apache users on 2.9.14 or later can use the `tx.crs_xml_attr_inspect` gate normally.

Users on **ModSecurity v2 older than 2.9.14** should update ModSecurity alongside this CRS release. If that is not immediately possible, the gate's opt-out will not take effect; use config-load-time directives instead to suppress attribute inspection:

```apache
SecRuleUpdateTargetByTag "attack-protocol"  "!XML://@*"
SecRuleUpdateTargetByTag "attack-lfi"       "!XML://@*"
SecRuleUpdateTargetByTag "attack-rfi"       "!XML://@*"
SecRuleUpdateTargetByTag "attack-rce"       "!XML://@*"
SecRuleUpdateTargetByTag "attack-php"       "!XML://@*"
SecRuleUpdateTargetByTag "attack-generic"   "!XML://@*"
SecRuleUpdateTargetByTag "attack-xss"       "!XML://@*"
SecRuleUpdateTargetByTag "attack-sqli"      "!XML://@*"
SecRuleUpdateTargetByTag "attack-fixation"  "!XML://@*"
```

Credit goes to [@HackingRepo](https://github.com/HackingRepo) for reporting this issue and to [@theseion](https://github.com/theseion) for the fix.

### Unix RCE ReDoS in shared regex-assembly include ([GHSA-f5qm-3h4p-8qhg](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-f5qm-3h4p-8qhg))

**Severity:** HIGH — CVSS score pending  
**CWE:** CWE-1333 — Inefficient Regular Expression Complexity

#### Impact

A regular-expression denial of service (ReDoS) affects the shared include `regex-assembly/include/unix-shell-evasion-prefix.ra`, used to build **12 Unix RCE detection rules**: 932220, 932230, 932231, 932232, 932235, 932236, 932238, 932239, 932250, 932260, 932340, and 932350.

A single unauthenticated crafted request drives PCRE2 past its backtracking limit. When PCRE2 exceeds that limit, the `@rx` operator returns an error rather than a match result, which has two consequences:

- **Detection bypass** — the affected rule fails to evaluate for the given parameter, so the RCE payload is not inspected.
- **CPU denial of service** — the engine burns CPU exploring the ambiguous pattern on every such request.

**Root cause:** The commands-prefix group contained an ambiguous whitespace-handling alternation inside a `*` quantifier. A whitespace run between prefix tokens could be consumed by more than one quantifier, so the number of parse paths grew combinatorially with the length of the run. This has been confirmed reproducible with `pcre2test` 10.47.

**Who is affected:** Deployments running CRS on **ModSecurity v2 or v3** (both link against PCRE2). **Coraza (RE2) is not affected** — RE2 does not backtrack.

#### Workaround for users unable to update immediately

There is no workaround that fully preserves detection without applying the patch:

- **Run CRS on a RE2-based engine (Coraza).** RE2 is not affected.
- **Constrain request size.** Tighter `SecRequestBodyLimit` and argument-length limits reduce exploitability but do not eliminate it.
- Lowering `SecPcreMatchLimit` / `SecPcreMatchLimitRecursion` makes the engine error sooner (less CPU per request) but does **not** remove the detection bypass.
- Disabling the affected rules removes the DoS exposure but also removes the RCE detection they provide, and is not recommended.

#### Full advisory

The full advisory is available at [GHSA-f5qm-3h4p-8qhg](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-f5qm-3h4p-8qhg).

## Changes in v4.28.0

### New features and detections

- **UTF-8 validation enabled by default** — Rule 920250 (`@validateUtf8Encoding` on `REQUEST_FILENAME|ARGS|ARGS_NAMES`) is now active at PL1 without additional configuration. Sites that genuinely use a non-UTF-8 parameter encoding can opt out via the `900950` `SecAction` in `crs-setup.conf.example`. ([#4647](https://github.com/coreruleset/coreruleset/pull/4647))

- **Shell quote evasion detection** — New detection for shell quote evasion techniques used to bypass command-detection rules. ([#3813](https://github.com/coreruleset/coreruleset/pull/3813))

- **ORM lookup operator injection** — Two new rules detect Django-style ORM lookup-operator injection in request parameter names, a class of attack that can lead to data leakage or authentication-filter bypass when unsanitized parameter keys are passed directly into a query builder:
  - **Rule 934220** (PL2): nested relationship traversal — two or more `__` separators — followed by an operator suffix (e.g. `created_by__departments__user__username__startswith`). Multi-hop traversal exposed to clients is rarely legitimate.
  - **Rule 934210** (PL3): any operator suffix on a parameter name (e.g. `username__startswith`). Sits at PL3 as single-field operator syntax is documented and legitimate in some APIs.

  Both rules inspect `ARGS_NAMES` and `REQUEST_BODY`. ([#4659](https://github.com/coreruleset/coreruleset/pull/4659))

- **Uninitialized variable spacer in RCE evasion** — The unix-shell evasion prefix now recognises an uninitialised shell variable used as a spacer (e.g. `$a`), which expands to the empty string at runtime. Payloads such as `;$a cat test.txt` previously bypassed PL1–PL3 detection; they now trigger at PL2 (rule 932236) or PL1 (rule 932235). This change regenerates all 12 rules sharing the `unix-shell-evasion-prefix.ra` include. ([#4652](https://github.com/coreruleset/coreruleset/pull/4652))

### Other changes

- **NPM subdirectories in restricted files** — `restricted-files.data` now covers common `node_modules/` subdirectories (`.bin`, `.cache`, `package.json`, `package-lock.json`) in a way that avoids the false positives the bare `node_modules/` entry caused on static sites. ([#4653](https://github.com/coreruleset/coreruleset/pull/4653))

- **Regex hardening** — In addition to the ReDoS security fix above, four further rules had ambiguous patterns corrected:
  - Rules 933160/933161 — PHP function-call comment suffix de-ambiguated. ([#4666](https://github.com/coreruleset/coreruleset/pull/4666))
  - Rule 933180 — PHP variable-function noise suffix de-ambiguated. ([#4669](https://github.com/coreruleset/coreruleset/pull/4669))
  - Rule 941140 — CSS `url(javascript:...)` XSS detection, declaration-list loop bounded. ([#4670](https://github.com/coreruleset/coreruleset/pull/4670))
  - Rule 942522 — Removed a redundant `^.*?` prefix that negated the benefit of anchoring the regex to the start of the string. ([#4676](https://github.com/coreruleset/coreruleset/pull/4676))

- **Rules 932171 and 942361** — Restored a `(?:json\.)?` prefix fix on the `ARGS_NAMES` check that had been silently lost during conflict resolution. These two rules carry hand-written regexes with no `.ra` source file and were therefore missed when regenerating other rules from source. ([#4672](https://github.com/coreruleset/coreruleset/pull/4672))

- **Rule 942390** — Migrated from an inline regex to `regex-assembly/942390.ra`. ([#4011](https://github.com/coreruleset/coreruleset/pull/4011))

- **`crs-setup.conf.example`** — `SecDefaultAction` directives for phases 3, 4, and 5 are now defined in anomaly scoring mode, ensuring consistent logging and auditing behavior across WAF engines. ([#4675](https://github.com/coreruleset/coreruleset/pull/4675))

- **RESPONSE_BODY false positives** — Several overly broad phrases in response-body error-detection rules have been replaced with more specific alternatives. ([#4684](https://github.com/coreruleset/coreruleset/pull/4684))

## Changes in v4.25.1 LTS

This release backports security and false-positive fixes onto the v4.25.x LTS branch. The two security fixes above apply in full; the `tx.crs_xml_attr_inspect` opt-in gate and the libmodsecurity v3.0.16 requirement described in the security section are specific to this branch.

### Regex hardening backports

- Rules 933160/933161 — PHP function-call comment suffix. ([#4666](https://github.com/coreruleset/coreruleset/pull/4666))
- Rule 933180 — PHP variable-function noise suffix. ([#4669](https://github.com/coreruleset/coreruleset/pull/4669))
- Rule 941140 — CSS `url(javascript:...)` XSS detection. ([#4670](https://github.com/coreruleset/coreruleset/pull/4670))

### False-positive reductions

- **Rules 920240 and 920400** — Now use `REQBODY_PROCESSOR` instead of the `Content-Type` header to determine whether a request body is URL-encoded, making them more robust for applications that send URL-encoded data with non-standard content types. ([#4639](https://github.com/coreruleset/coreruleset/pull/4639))
- **Rule 942200** — Refined comment-handling logic to fix a regression that blocked user-agent strings containing a comma but no surrounding whitespace. ([#4608](https://github.com/coreruleset/coreruleset/pull/4608))
- **Parameter name `.history`** — Added a word boundary to prevent substring false positives (e.g. `history.history`). ([#4614](https://github.com/coreruleset/coreruleset/pull/4614))
- **Unix RCE (PL1) — `pg` command** — Removed from the PL1 Unix command list; not installed by default on most Linux distributions. ([#4613](https://github.com/coreruleset/coreruleset/pull/4613))
- **Rules 932171 and 942361** — Restored the `(?:json\.)?` ARGS_NAMES-prefix fix that was silently dropped during conflict resolution, as these rules have hand-written regexes with no `.ra` source file. ([#4672](https://github.com/coreruleset/coreruleset/pull/4672))

### Protocol enforcement

- **Rule 920100** — Removed support for bare HTTP/0.9 `GET` requests (obsolete per RFC 9110), resolving an inconsistency with rule 920430 which already excluded HTTP/0.9 from the allowed HTTP versions list. ([#4621](https://github.com/coreruleset/coreruleset/pull/4621))

### Setup improvement

- **`crs-setup.conf.example`** — `SecDefaultAction` for phases 3, 4, and 5 in anomaly scoring mode. ([#4675](https://github.com/coreruleset/coreruleset/pull/4675))

## Changes in v3.3.10

This is a **security-only** release on the v3.3 LTS line. It contains both security fixes described above and no other functional changes.

The `tx.crs_xml_attr_inspect` opt-in gate (rules 901180 and 901181 in `REQUEST-901-INITIALIZATION.conf`) is present on this branch, with the same default-on behavior and the same ModSecurity v2 opt-out limitation described above.

## Upgrading

All three releases are available on the [CRS GitHub releases page](https://github.com/coreruleset/coreruleset/releases).

**ModSecurity v2/Apache users on v4.25.1 or v3.3.10:** update ModSecurity to **v2.9.14** alongside this CRS release to ensure the `tx.crs_xml_attr_inspect` opt-out gate works correctly.

**nginx + libmodsecurity3 users on v4.25.1 or v3.3.10:** update libmodsecurity3 to **v3.0.16** alongside this CRS release. The opt-in gate on these branches uses `ctl:ruleRemoveTargetByTag` with an `XML://@*` target; versions of libmodsecurity3 prior to 3.0.16 reject the `@` character in that position at parse time, preventing the configuration from loading at all ([ModSecurity#3589](https://github.com/owasp-modsecurity/ModSecurity/pull/3589)). v4.28.0 does not use this syntax and has no additional engine version requirement.

If you have questions or concerns, please reach out via the [CRS GitHub repository](https://github.com/coreruleset/coreruleset), in our Slack channel (#coreruleset on [owasp.slack.com](https://owasp.slack.com/)), or on our [mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project).


