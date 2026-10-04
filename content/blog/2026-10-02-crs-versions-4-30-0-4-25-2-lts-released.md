---
title: 'CRS versions 4.30.0 and 4.25.2 LTS released'
date: '2026-10-02'
author: fzipi
categories:
    - Blog
tags:
    - CRS-News
    - Release
---

The OWASP CRS team is pleased to announce two coordinated releases today: **v4.30.0** (main branch) and **v4.25.2** (v4 LTS). Both fix the same three security vulnerabilities, published today as GitHub security advisories, along with a file upload bypass in the PHP and Java upload checks. Users on either supported v4 line are strongly encouraged to update.

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/docs/deployment/install/) page.

## Security fixes

All three vulnerabilities affect both release lines. CVE identifiers have been requested and will be added to the advisories once assigned.

### Path-based command injection bypass of the RCE rules ([GHSA-575j-qr6p-9763](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-575j-qr6p-9763))

**Severity:** MEDIUM — CVSS 3.1 score 5.4 (`AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:L/A:N`)  
**CWE:** CWE-693 — Protection Mechanism Failure

#### Impact

The 932 (Remote Command Execution) rule family did not include `REQUEST_FILENAME` in its targets. A command injection payload that CRS detects in a query or body argument was not inspected when the same payload was placed in the URL path instead, even at paranoia level 4. For example, `GET /files?f=x%3Bid` triggers rule 932350, while `GET /files/x%3Bid` triggered no 932 rule at all.

**Who is impacted:** applications that pass a URL path segment to a shell (for example `os.popen`, or `child_process.exec` with `shell: true`). Calls that don't go through a shell, such as `execFile`, are not affected.

#### Fix

`REQUEST_FILENAME` is now a target of the RCE rules 932125–932390, with one exception: rule 932200 does not inspect the path, because it requires a `/` and every URL path contains one, so it would fire on ordinary filenames like `John's report.pdf`.

#### Workaround

If you can't update right away, add the target to the rules that close the reported bypass:

```apache
SecRuleUpdateTargetById 932130 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932235 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932236 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932240 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932260 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932281 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932340 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932350 "REQUEST_FILENAME"
SecRuleUpdateTargetById 932380 "REQUEST_FILENAME"
```

CRS 3.x is also affected and will not receive a fix. In 3.x, `SecRuleUpdateTargetById 932130 "REQUEST_FILENAME"` covers the only rule from this list that exists there.

Credit goes to [@SoraMoko](https://github.com/SoraMoko) for reporting this issue and to [@theseion](https://github.com/theseion) for the fix.

### Charset allow-list bypass via mixed-case `CHARSET` ([GHSA-89h9-2j8h-9gp2](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-89h9-2j8h-9gp2))

**Severity:** HIGH — CVSS 3.1 score 7.2 (`AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)  
**CWE:** CWE-178 — Improper Handling of Case Sensitivity; CWE-436 — Interpretation Conflict

#### Impact

Rule 920480 enforces the allow-list of charsets a client may declare in the `Content-Type` header (`tx.allowed_request_content_type_charset`). Its anchor regex matched only the lowercase parameter name `charset`. Media-type parameter names are case-insensitive (RFC 9110 §8.3.1), so `Content-Type: application/x-www-form-urlencoded; CHARSET=utf-7` never matched, and the allow-list check never ran. This reopens the encoding-based evasion class the rule exists to block, such as UTF-7 XSS, whenever the backend honors the declared charset.

**Who is impacted:** every CRS v4 release up to and including 4.29.0 and 4.25.1, at the default paranoia levels. CRS 3.3.x is not affected, because its equivalent rule already lowercases the header.

#### Workaround

```apache
SecRuleUpdateActionById 920480 "t:lowercase"
```

Credit goes to [@HackingRepo](https://github.com/HackingRepo) for reporting this issue and to [@fzipi](https://github.com/fzipi) for the fix.

### Multipart `_charset_` shadowing bypass ([GHSA-qmx4-jfcv-fgww](https://github.com/coreruleset/coreruleset/security/advisories/GHSA-qmx4-jfcv-fgww))

**Severity:** MEDIUM — CVSS 3.1 score 5.8 (`AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:N`)  
**CWE:** CWE-235 — Improper Handling of Extra Parameters; CWE-436 — Interpretation Conflict

#### Impact

Rule 922100 blocks multipart requests whose global `_charset_` field declares a charset that isn't allowed by policy. It only checked one `_charset_` value. An attacker could add a second, allowed `_charset_`, either in the query string or in another multipart part, and the disallowed one went unchecked. That let the attacker inject multipart parts in any encoding. Which value was checked depended on the engine: ModSecurity v2 expands `%{ARGS._charset_}` to the first value, libmodsecurity3 to the last.

#### Fix

Every `_charset_` value is now collected and checked individually, so no value can shadow another on either engine.

Credit goes to [@airween](https://github.com/airween) for reporting this issue, and to [@airween](https://github.com/airween) and [@fzipi](https://github.com/fzipi) for the fix.

### Trailing-slash bypass of the upload extension checks

Rules 933110 (PHP) and 944140 (Java) block uploads of script files by extension. They tolerated trailing dots after the extension (`shell.php.`) but not a trailing slash, so `shell.php/` was not blocked. That matters for frameworks that strip a trailing path separator before saving the file. Both rules now tolerate any mix of trailing dots and slashes. ([#4815](https://github.com/coreruleset/coreruleset/pull/4815))

## Changes in v4.30.0

### Important changes

- **Skipping response analysis now skips response bodies too** — Setting `tx.crs_skip_response_analysis` (rule 900500 in `crs-setup.conf`) was meant to skip all response rules, but it only skipped the phase 3 response header rules; the phase 4 body rules kept running. New rule 950022 skips the phase 4 rules as well. ([#4807](https://github.com/coreruleset/coreruleset/pull/4807))

### New features and detections

- **JSON content types allowed by default** — Any `application/*+json` content type (rule 901370) and the AWS `application/x-amz-json-1.0` and `1.1` types (rule 901360) are now allowed by default, and their bodies are parsed as JSON. Previously these requests were either blocked by rule 920420 or reached the rules without their JSON body being parsed. Subtypes that themselves contain a `+`, such as `application/vc+ld+json`, are covered too. ([#4775](https://github.com/coreruleset/coreruleset/pull/4775), [#4828](https://github.com/coreruleset/coreruleset/pull/4828))
- **Active Directory command-line tools** — Rule 932380 now detects `dsquery`, `dsadd`, `dsmod`, `ntdsutil`, `csvde`, `ldifde` and the rest of the AD directory-service tool family. ([#4768](https://github.com/coreruleset/coreruleset/pull/4768))
- **Velocity and FreeMarker template injection** — Rule 934200 now detects Apache Velocity (`#set`, `#foreach`) and FreeMarker (`<#assign>`, `<@macro>`) directive syntax when it contains a function or method call, a multiplication, or a double underscore (as in `__class__`). ([#4774](https://github.com/coreruleset/coreruleset/pull/4774))
- **SELinux administration commands** — Common SELinux commands are now detected as Unix command injection. ([#4724](https://github.com/coreruleset/coreruleset/pull/4724))
- **Scanner user agent `Mozilla/6.0`** — Added to the scanner user-agent list; it has no legitimate use. ([#4784](https://github.com/coreruleset/coreruleset/pull/4784))
- **Restricted files** — `.claude` configuration and credential files and a further batch of sensitive paths are now restricted. ([#4809](https://github.com/coreruleset/coreruleset/pull/4809), [#4816](https://github.com/coreruleset/coreruleset/pull/4816))

### Rule removals

- **Response compression checks consolidated** — Each response rule file (950–956) used to carry its own check that skips body inspection for compressed responses (rules 950010, 951010, 952010, 953010, 954010, 955010 and 956010). They are replaced by a single rule, 950020, which skips to the new `BEGIN-RESPONSE-959-BLOCKING-EVALUATION` marker so that response blocking evaluation still runs. **If your exclusions reference any of the removed rule IDs, update them.** ([#4806](https://github.com/coreruleset/coreruleset/pull/4806))

### Other changes

- **Rule 932180** — Now uses a regular expression with word boundaries for entries prone to substring matches, fixing false positives such as `asound` matching `asoundmind.jpg`. ([#4632](https://github.com/coreruleset/coreruleset/pull/4632))
- **Rule 932270** — Tilde expansion patterns (`~+`, `~-`) now require a shell boundary in front, so values like `cookie=abc~+1` no longer match. ([#4596](https://github.com/coreruleset/coreruleset/pull/4596))
- **Rule 913100** — The `vega` scanner entry no longer matches the `veganism.social` user agent. ([#4777](https://github.com/coreruleset/coreruleset/pull/4777))
- **Response body false positives** — Rule 951230 drops an overly broad MySQL error pattern, and rule 956100 no longer matches the keyword `EOFError`. ([#4747](https://github.com/coreruleset/coreruleset/pull/4747), [#4752](https://github.com/coreruleset/coreruleset/pull/4752))
- **libmodsecurity3 and Coraza** — A configure-time exclusion fixes a substring false positive on JSON keys named `profiledata`. ([#4812](https://github.com/coreruleset/coreruleset/pull/4812))

## Changes in v4.25.2 LTS

This release backports security and selected bug fixes onto the v4.25.x LTS branch.

### Security fixes

All three advisories and the upload extension fix described above, plus:

- **Rule 942390** — Removed a length bound in the SQL `(X)OR` injection detection that could be bypassed with long quoted or unary literals. ([#4713](https://github.com/coreruleset/coreruleset/pull/4713))

### Bug fixes

- **Skipping response analysis now skips response bodies too** (new rule 950022), as in v4.30.0. ([#4807](https://github.com/coreruleset/coreruleset/pull/4807))
- **Rule 913100** — `veganism.social` false positive, as in v4.30.0. ([#4777](https://github.com/coreruleset/coreruleset/pull/4777))

### Other changes

- **JSON content types allowed by default** (new rules 901360 and 901370), as in v4.30.0. Note that this changes default behavior on the LTS line: `application/*+json` and AWS JSON requests that were previously blocked by rule 920420 are now accepted and inspected as JSON. ([#4775](https://github.com/coreruleset/coreruleset/pull/4775), [#4828](https://github.com/coreruleset/coreruleset/pull/4828))
- **Rule 932171** — Moved to a regex-assembly source with the standard whitespace class. This is a maintainability change with no change in detection. ([#4703](https://github.com/coreruleset/coreruleset/pull/4703))

The response compression consolidation (#4806) is **not** part of v4.25.2, so the per-file compression rules (950010–956010) remain on the LTS line.

## Upgrading

Both releases are available on the [CRS GitHub releases page](https://github.com/coreruleset/coreruleset/releases).

Because the RCE rules now inspect the URL path, review your false-positive logs for 932xxx alerts on `REQUEST_FILENAME` after updating, especially if your application uses shell-like characters in path segments.

If you have questions or concerns, please reach out via the [CRS GitHub repository](https://github.com/coreruleset/coreruleset), in our Slack channel (#coreruleset on [owasp.slack.com](https://owasp.slack.com/)), or on our [mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project).
