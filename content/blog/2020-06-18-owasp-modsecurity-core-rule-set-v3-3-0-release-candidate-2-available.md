---
author: lifeforms
categories:
  - Blog
date: '2020-06-18T20:39:56+02:00'
title: OWASP ModSecurity Core Rule Set v3.3.0 Release Candidate 2 available
url: /2020/06/18/owasp-modsecurity-core-rule-set-v3-3-0-release-candidate-2-available/
---


The OWASP ModSecurity Core Rule Set team is proud to announce the release candidate 2 for the upcoming CRS v3.3.0 release. The release candidate is available at:

- <https://github.com/coreruleset/coreruleset/archive/v3.3.0-rc2.tar.gz>
- <https://github.com/coreruleset/coreruleset/archive/v3.3.0-rc2.zip>

This release packages many changes, such as:

- Block backup files ending with ~ in filename (Andrea Menin)
- Detect ffuf vuln scanner (Will Woodson)
- Detect SemrushBot crawler (Christian Folini)
- Detect WFuzz vuln scanner (azurit)
- New LDAP injection rule (Christian Folini)
- New HTTP Splitting rule (Andrea Menin)
- Add .swp to restricted extensions (Andrea Menin)
- Allow CloudEvents content types (Bobby Earl)
- Add CAPEC tags for attack classification (Fernando Outeda, Christian Folini)
- Detect Unix RCE bypass techniques via uninitialized variables, string concatenations and globbing patterns (Andrea Menin)

Important note: The format of configuration setting `allowed_request_content_type` has been changed to be more in line with other variables. If you had manually changed this setting, then you need to update this configuration setting. Please see the example rule 900220 in crs-setup.conf.example. If you **didn’t** change this setting, you don’t need to do anything.

If you had tested RC1, the list of changes between RC1 and RC2 are as follows:

New functionality:

- Add CloudEvents content types (Bobby Earl)
- Add CAPEC tags for attack classification (Fernando Outeda, Christian Folini)
- Detect RCE bypass techniques via uninitialized variables, string concatenations and globbing patterns (Andrea Menin)

Removed functionality:

- Removed rule tags WASCTC, OWASP\_TOP\_10, OWASP\_AppSensor/RE1, and OWASP\_CRS/FOO/BAR; note that tags 'OWASP\_CRS' and 'attack-type' are kept. (Christian Folini)

Fixes and improvements:

- Prevent bypass of rule 921110 (Amit Klein, Franziska Bühler)
- fix CVE msg in rules 944120 944240 (Fernando Outeda)
- Remove broken or no longer used files (Federico G. Schwindt)
- Make content-type case insensitive (franbuehler)
- Move /util/docker folder from v3.3/dev branch to dedicated repo (Peter Bittner)
- feat(lint): split actions in linting and regression (Felipe Zipitria)
- Fix FP in 921120 (Amit Klein, Franziska Bühler)
- Add missing OWASP\_CRS tags (Christian Folini)
- Fix GHA badges (Federico G. Schwindt)
- feat(badge): add apache license badge
- fix typos found by fossies codespell (Tim Herren)
- Decrease processing time of rules (Ervin Hegedüs)
- handle multiple directives in 920510 (themiddleblue)

Please see the CHANGES document with around 160 entries for the complete list of new features and improvements: <https://github.com/coreruleset/coreruleset/blob/v3.3.0-rc2/CHANGES>

Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP Top 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install. This RC therefore offers an opportunity for individuals to provide feedback and to report any issue they face with this release. We will then try and fix them for the upcoming full release.

Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel (#coreruleset on owasp.slack.com), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release candidate.

Our current timeline is to seek public feedback for the next 1.5 weeks, followed by a release on June 29th. We look forward to hearing your feedback!

Sincerely,
Walter Hop, release manager, on behalf of the Core Rule Set development team
