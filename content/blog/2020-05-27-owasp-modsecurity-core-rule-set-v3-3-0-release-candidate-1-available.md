---
author: lifeforms
categories:
  - Blog
date: '2020-05-27T16:05:24+02:00'
tags:
  - Release
title: OWASP ModSecurity Core Rule Set v3.3.0 Release Candidate 1 available
---


The OWASP ModSecurity Core Rule Set team is proud to announce the release candidate 1 for the upcoming CRS v3.3.0 release. The release candidate is available at:

- <https://github.com/coreruleset/coreruleset/archive/v3.3.0-rc1.tar.gz>
- <https://github.com/coreruleset/coreruleset/archive/v3.3.0-rc1.zip>

This release packages many changes, such as:

- New rule to detect LDAP injection
- New HTTP Splitting rule
- Block backup files ending with ~ in filename
- Detect ffuf, Semrush and WFuzz scanners
- Updated exclusion profiles for Nextcloud, WordPress and XenForo
- Improvements to many patterns to improve detection and lower false alarms

Important note: The format of configuration setting `allowed_request_content_type` has been changed to be more in line with other variables. If you had manually changed this setting, then you need to update this configuration setting. Please see the example rule 900220 in `crs-setup.conf.example`. If you didn't change this setting, you don't need to do anything.

Please see the CHANGES document with around 150 entries for a detailed list of new features and improvements.  
<https://github.com/coreruleset/coreruleset/blob/v3.3.0-rc1/CHANGES>

Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP Top 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install. This RC therefore offers an opportunity for individuals to provide feedback and to report any issue they face with this release. We will then try and fix them for the upcoming full release.

Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel ([\#coreruleset](https://owasp.slack.com/archives/CBKGH8A5P) on [owasp.slack.com](https://owasp.slack.com)), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release candidate.

Our current timeline is to seek public feedback for the next two weeks, followed by an RC2 (if needed) and subsequently a release on June 16th. We look forward to hearing your feedback!  
  
Sincerely,
Walter Hop, release manager, on behalf of the Core Rule Set development team
