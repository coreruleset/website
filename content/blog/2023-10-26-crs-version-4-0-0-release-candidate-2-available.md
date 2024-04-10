---
author: RedXanadu
categories:
  - Blog
date: '2023-10-26T22:42:38+02:00'
title: CRS version 4.0.0 release candidate 2 available
---


The OWASP ModSecurity Core Rule Set (CRS) team is proud to announce the availability of release candidate 2 (RC2) of the upcoming CRS v4.0.0 release. The release candidate is available for download as a 'release' from our GitHub repository:

- <https://github.com/coreruleset/coreruleset/releases/tag/v4.0.0-rc2>

This new release candidate includes over 230 changes. Some of the important changes include:

- Add new rule 920620 to explicitly detect multiple Content-Type abuse ([CVE-2023-38199](https://coreruleset.org/20230717/cve-2023-38199-multiple-content-type-headers/)) (Andrea Menin)
- Extend definition of restricted headers to include Content-Encoding and Accept-Charset by default (Walter Hop)
- Migrate application exclusions and less-used functionality to plugins (Christian Folini, Max Leske, Jozef Sudolský, Andrew Howe)
- Add support for HTTP/3 (Jozef Sudolský)
- Add enable\_default\_collections flag to not initialize collections by default (Matteo Pace)
- Switch to using wordnet instead of spell for finding English words in spell.sh utility (Max Leske)

Refer to the CHANGES.md file in the release for the full list of changes.

It is important to note that this new release candidate is **significantly different to the first release candidate** which was [announced and made available](https://coreruleset.org/20220428/coreruleset-v4-rc1-available/) back in April 2022. Two days after the v4.0.0 RC1 release, the CRS project [participated in a bug bounty program](https://coreruleset.org/20230509/what-we-learnt-from-our-bug-bounty-program-its-not-for-the-faint-of-heart/) in April-May 2022 which resulted in *175 security findings* being reported. The decision was made to fix the findings in full for the v4.0.0 release, rather than release a half-baked version 4.0 with many newly discovered holes.

The fixes required a *significant* amount of work over many months. It was sometimes the case that adding the required new detection would cause unforeseen problems, such as introducing new false positives which then needed to be addressed. Fixing all of the security findings in full required the development of new tooling, new rules, new tests, and new approaches. This all took a lot of time to complete to the high standard expected from the CRS project, resulting in an unfortunate delay to v4.0.0.

As a result of fixing the security findings, the RC2 release features **a lot of new detection capability**. It is highly likely that **new false positives will continue to appear** as a result, so it is very important for this new release candidate to be tested as widely as possible. **Please test this new release candidate** and [report any false positives encountered](https://github.com/coreruleset/coreruleset/issues/new?assignees=&labels=%3Aheavy_plus_sign%3A+False+Positive&projects=&template=01_false-positive.md&title=). All feedback and reports are gratefully received and will help to make the final v4.0.0 release the best and most comprehensive CRS release ever!

Sincerely,  
Andrew Howe on behalf of the Core Rule Set development team
