---
title: 'CRS version 4.24.0 released'
date: '2026-02-28'
author: fzipi
categories:
  - Blog
tags:
  - CRS-News
  - Release
slug: 'crs-version-4-24-0-released'
---

The OWASP CRS team is pleased to announce the release of CRS [v4.24.0](https://github.com/coreruleset/coreruleset/releases/tag/v4.24.0).

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/docs/deployment/install/) page.

This is a regular minor release with no breaking changes or security fixes. It includes new detection capabilities, important bug fixes, false positive reductions, and a significant modernization effort converting rules to regex-assembly format.

#### New detections

- **Smarty template PHP tag detection** (rule 933100): Added detection for Smarty template engine PHP tags, expanding protection against Server-Side Template Injection (SSTI) attacks targeting PHP applications using the Smarty templating engine, by [@touchweb-vincent](https://github.com/touchweb-vincent) ([#4447](https://github.com/coreruleset/coreruleset/pull/4447))

#### Bug fixes

- **Lazy regex for RCE rule 932130**: Changed regex semantics from `.` (match anything) to `[^\(\)]` for better performance and specificity, preventing potential backtracking issues, by [@fzipi](https://github.com/fzipi) ([#3730](https://github.com/coreruleset/coreruleset/pull/3730))
- **Method override false blocking** (rule 920650): Fixed the rule to not block requests when the `_method` override parameter matches the actual HTTP method being used. Applications like GitLab sometimes set `_method=post` in POST request bodies that were triggering false blocks, by [@EsadCetiner](https://github.com/EsadCetiner) ([#4455](https://github.com/coreruleset/coreruleset/pull/4455))
- **Multi-byte UTF-8 handling in SQL special character detection** (rules 942420-942432): Extracted multi-byte UTF-8 characters (acute accent U+00B4, left single quote U+2018, right single quote U+2019) from regex character classes into alternations. Previously, byte-by-byte matching caused false positives with non-Latin scripts including Chinese, Japanese, Arabic, Korean, and Hebrew. This closes the longstanding issue [#3325](https://github.com/coreruleset/coreruleset/issues/3325), by [@fzipi](https://github.com/fzipi) ([#4458](https://github.com/coreruleset/coreruleset/pull/4458))

#### False positive fixes

- **Restricted files FP reduction** (rule 930130): Removed `.pac` from the restricted files dataset because it was also matching legitimate files containing `.pack` in the name (e.g., `jquery.nivo.slider.pack.js`). Also mitigated FP on `.history` pattern matching files like `jquery.history.min.js`, by [@touchweb-vincent](https://github.com/touchweb-vincent) ([#4451](https://github.com/coreruleset/coreruleset/pull/4451))
- **UNIX command FP reduction** (rule 932340): Added prefix requirements for shell evasion detection, as two-letter UNIX commands were causing FPs when users entered initials into form fields, by [@ssigwart](https://github.com/ssigwart) ([#4454](https://github.com/coreruleset/coreruleset/pull/4454))
- **XMP metadata and XSL stylesheet FP** (rule 933100): Reduced false positives caused by Adobe XMP metadata packets and XSL stylesheet declarations, which were being flagged as PHP injection attempts, by [@touchweb-vincent](https://github.com/touchweb-vincent) ([#4445](https://github.com/coreruleset/coreruleset/pull/4445))
- **JSON variable name "profile" FP**: When sending JSON data to libModSecurity3 or Coraza, a variable named `profile` becomes `ARGS_NAMES:json.profile`, which matched an entry in `lfi-os-files.data` (the `.profile` file). Added a configure-time rule exclusion to resolve this, by [@EsadCetiner](https://github.com/EsadCetiner) ([#4477](https://github.com/coreruleset/coreruleset/pull/4477))
- **French addresses FP** (rule 942200): Fixed false positives triggered by French addresses containing comma and single quote patterns like `999, rue d'Arlon`, by [@theseion](https://github.com/theseion) ([#4476](https://github.com/coreruleset/coreruleset/pull/4476))
- **Google Funding Choices cookie exclusions**: Added more exclusions for Google Funding Choices cookies that were triggering false positives, by [@azurit](https://github.com/azurit) ([#4484](https://github.com/coreruleset/coreruleset/pull/4484))

#### Regex assembly conversions

A major theme of this release is the conversion of rules to [regex-assembly](https://github.com/coreruleset/coreruleset/issues/4480) format. This enables management by the `crs-toolchain`, allows optimized regex generation with common prefix factoring, and makes rules easier to maintain. In this release, **12 rules** were converted:

- Session Fixation rule 943110 ([#4431](https://github.com/coreruleset/coreruleset/pull/4431))
- RCE commands rule 932190, by [@theseion](https://github.com/theseion) ([#4475](https://github.com/coreruleset/coreruleset/pull/4475))
- Microsoft Access leakage rule 951110 ([#4463](https://github.com/coreruleset/coreruleset/pull/4463))
- DB2 leakage rule 951130 ([#4462](https://github.com/coreruleset/coreruleset/pull/4462))
- EMC leakage rule 951140 ([#4464](https://github.com/coreruleset/coreruleset/pull/4464))
- Informix leakage rule 951180 ([#4465](https://github.com/coreruleset/coreruleset/pull/4465))
- Ingres leakage rule 951190 ([#4466](https://github.com/coreruleset/coreruleset/pull/4466))
- Interbase leakage rule 951200 ([#4467](https://github.com/coreruleset/coreruleset/pull/4467))
- maxDB leakage rule 951210 ([#4468](https://github.com/coreruleset/coreruleset/pull/4468))
- MSSQL leakage rule 951220 ([#4459](https://github.com/coreruleset/coreruleset/pull/4459))
- SQLite leakage rule 951250 ([#4460](https://github.com/coreruleset/coreruleset/pull/4460))
- Sybase leakage rule 951260 ([#4461](https://github.com/coreruleset/coreruleset/pull/4461))

#### Looking ahead: CRS 4.25.0 - the first LTS release

As [previously announced]({{< ref "blog/2025-12-25-the-future-lts-release-cycle.md" >}}), the next release, CRS 4.25.0, will be the first Long-Term Support (LTS) release for the CRS 4 line. Changes in that release will be mostly cosmetic: completing the [migration to regex-assembly](https://github.com/coreruleset/coreruleset/issues/4480) across the remaining rules, along with small changes and false positive fixes. The focus is on stability and maintainability as we prepare for long-term support.

The full list of changes included in v4.24.0 can be found on the [GitHub release page](https://github.com/coreruleset/coreruleset/releases/tag/v4.24.0).

