---
author: Walter Hop
categories:
  - Blog
date: '2020-12-28T18:38:16+01:00'
permalink: /20201228/owasp-modsecurity-core-rule-set-v3-3-1-release-candidate-1-available/
title: OWASP ModSecurity Core Rule Set v3.3.1 Release Candidate 1 available
url: /2020/12/28/owasp-modsecurity-core-rule-set-v3-3-1-release-candidate-1-available/
---


The OWASP ModSecurity Core Rule Set team is proud to announce the release candidate 1 for the upcoming CRS v3.3.1 release. The release candidate is available at:

- <https://github.com/coreruleset/coreruleset/archive/v3.3.1-rc1.tar.gz>
- <https://github.com/coreruleset/coreruleset/archive/v3.3.1-rc1.zip>

This is a maintenance release, containing the following changes:

- Run rules as early as possible, by decreasing phase:2 to phase:1 and phase:4 to phase:3 where the variables allow it (Ervin Hegedüs)
- Add early blocking mode (tx.blocking\_early) to block at the end of phase:1 and phase:3 (Christian Folini)

There are no changes to attack detections, so this release is mostly a "drop-in" replacement for our former release 3.3.0. If you are already running v3.3.0, you can simply extract the files over your existing files.

The early blocking mode may improve performance, as it allows to block a request quickly before processing of rules in phase 2 takes place (however, most attack detections still take place in phase 2). To use this feature, enable the `tx.blocking_early` setting in crs-setup.conf. [Please see the example configuration file for more details.](https://github.com/coreruleset/coreruleset/blob/v3.3.1-rc1/crs-setup.conf.example#L320)

Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP Top 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install. This RC therefore offers an opportunity for individuals to provide feedback and to report any issue they face with this release. We will then try and fix them for the upcoming full release.

Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel (#coreruleset on owasp.slack.com), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release candidate.

We plan the release on Tuesday the 5th of January 2021.

We look forward to hearing your feedback!

Sincerely,  
Walter Hop, release manager, on behalf of the Core Rule Set development team
