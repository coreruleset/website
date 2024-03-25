---
author: lifeforms
categories:
  - Blog
date: '2019-09-03T13:51:47+02:00'
tags:
  - '3.2'
  - Release
title: 'Announcement: OWASP ModSecurity Core Rule Set Version 3.2.0-RC2'
url: /2019/09/03/announcement-owasp-modsecurity-core-rule-set-version-3-2-0-rc2/
---


The OWASP ModSecurity Core Rule Set team is proud to announce the general availability of release candidate 2 for the upcoming CRS v3.2.0. The new release is available at

- [https://github.com/coreruleset/coreruleset/archive/v3.2.0-rc2.zip](https://slack-redir.net/link?url=https%3A%2F%2Fgithub.com%2FSpiderLabs%2Fowasp-modsecurity-crs%2Farchive%2Fv3.2.0-rc2.zip&v=3)
- [https://github.com/coreruleset/coreruleset/archive/v3.2.0-rc2.tar.gz](https://slack-redir.net/link?url=https%3A%2F%2Fgithub.com%2FSpiderLabs%2Fowasp-modsecurity-crs%2Farchive%2Fv3.2.0-rc2.tar.gz&v=3)

This release represents a very big step forward in terms of both capabilities and protections including:

- Improved compatibility with ModSecurity 3.x
- Improved CRS docker container that is fully configureable at creation
- Expanded Java RCE blacklist
- Expanded unix shell RCE blacklist
- Improved PHP RCE detection
- New javascript/Node.js RCE detection
- Expanded LFI blacklists
- Added XenForo rule exclusion profile
- Fixes for many false positives and bypasses
- Detection of more security scanners
- Regexp performance improvements preventing ReDoS in most cases

Please see the CHANGES document with around 150 entries for a detailed list of new features and improvements.  
[https://github.com/coreruleset/coreruleset/blob/v3.2.0-rc2/CHANGES](https://slack-redir.net/link?url=https%3A%2F%2Fgithub.com%2FSpiderLabs%2Fowasp-modsecurity-crs%2Fblob%2Fv3.2.0-rc2%2FCHANGES&v=3)  
  
Note how this RC2 is the first public release candidate for 3.2.0. RC1 was not formally released.  
  
Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP TOP 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install. This RC2 therefore offers an opportunity for individuals to provide feedback and to report any issue they face with this release. We will then try and fix them for the upcoming full release.

Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel ([\#coreruleset](https://owasp.slack.com/archives/CBKGH8A5P) on [owasp.slack.com](http://owasp.slack.com)), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release candidate.

Our current timeline is to seek public feedback on RC2 for the next two weeks, followed by an RC3 (if needed) and subsequently a release on September 24. We look forward to hearing your feedback!  
  
Sincerely,   
Walter Hop, release manager, on behalf of the Core Rule Set development team
