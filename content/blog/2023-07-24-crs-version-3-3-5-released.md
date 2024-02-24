---
author: RedXanadu
categories:
  - Blog
date: '2023-07-24T20:11:27+02:00'
guid: https://coreruleset.org/?p=2207
id: 2207
permalink: /20230724/crs-version-3-3-5-released/
title: CRS version 3.3.5 released
url: /2023/07/24/crs-version-3-3-5-released/
---


The OWASP ModSecurity Core Rule Set (CRS) team is pleased to announce the release of CRS v3.3.5.

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/installation/) page.

This is a security release which fixes the [recently announced](https://coreruleset.org/20230717/cve-2023-38199-multiple-content-type-headers/) CVE-2023-38199, whereby it is possible to cause an impedance mismatch on some platforms running CRS v3.3.4 and earlier by submitting a request with multiple Content-Type headers.

Aside from the security fix, a few other minor, non-breaking changes and improvements are also included in this release. The full changes are as follows:

- Backport fix for CVE-2023-38199 from CRS v4 via new rule 920620 (Andrea Menin, Felipe Zipitría)
- Fix paranoia level-related scoring issue in rule 921422 (Walter Hop)
- Move auditLogParts actions to the end of chained rules where used (Ervin Hegedus)
- Clean up redundant paranoia level tags (Ervin Hegedus)
- Clean up YAML test files to support go-ftw testing framework (Felipe Zipitría)
- Move testing framework from ftw to go-ftw (Felipe Zipitría)
- Update sponsors list and copyright notices (Felipe Zipitría)

As noted above, the fix for CVE-2023-38199 has [already been merged](https://github.com/coreruleset/coreruleset/pull/3237) into the [CRS v4 branch](https://github.com/coreruleset/coreruleset/tree/v4.0/dev): our upcoming milestone release which we hope to publish in the near future.

Please feel free to contact us with any questions or concerns about this release via the usual channels: directly via the [CRS GitHub repository](https://github.com/coreruleset/coreruleset), in our Slack channel (*\#coreruleset* on [owasp.slack.com](https://owasp.slack.com/)), or on our [mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project).

Sincerely,  
Andrew Howe on behalf of the Core Rule Set development team
