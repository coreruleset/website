---
author: lifeforms
categories:
  - Blog
date: '2019-09-24T11:13:43+02:00'
title: 'Announcement: OWASP ModSecurity Core Rule Set Version 3.2.0'
url: /2019/09/24/owasp-modsecurity-core-rule-set-version-3-2-0/
---


**The OWASP ModSecurity Core Rule Set team is proud to announce the general availability of the OWASP ModSecurity Core Rule Set Version 3.2.0.**

The new release is available for download at [](https://coreruleset.org/installation/)<https://coreruleset.org/installation/>

This release represents a very big step forward in terms of both capabilities and protections including:

- Improved compatibility with ModSecurity 3.x
- Improved CRS docker container that is fully configurable at creation
- Expanded Java RCE blacklist
- Expanded unix shell RCE blacklist
- Improved PHP RCE detection
- New javascript/Node.js RCE detection
- Expanded LFI blacklists
- Added XenForo rule exclusion profile
- Fixes for many false positives and bypasses
- Detection of more security scanners
- Regexp performance improvements preventing ReDoS in most cases

Please see the CHANGES document with around 150 entries for a detailed list of new features and improvements:  
[](https://github.com/coreruleset/coreruleset/blob/v3.2.0/CHANGES)<https://github.com/coreruleset/coreruleset/blob/v3.2.0/CHANGES>  
  
Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP TOP 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install.

Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel ([\#coreruleset](https://owasp.slack.com/archives/CBKGH8A5P) on [owasp.slack.com](http://owasp.slack.com)), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release candidate.

Sincerely,
Walter Hop, release manager, on behalf of the Core Rule Set development team
