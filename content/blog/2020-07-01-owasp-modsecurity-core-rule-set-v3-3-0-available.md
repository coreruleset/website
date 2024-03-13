---
author: Walter Hop
categories:
  - Blog
date: '2020-07-01T20:26:37+02:00'
tags:
  - Release
title: OWASP ModSecurity Core Rule Set v3.3.0 available
url: /2020/07/01/owasp-modsecurity-core-rule-set-v3-3-0-available/
---


The OWASP ModSecurity Core Rule Set team is proud to announce the final release for CRS v3.3.0.

For downloads and installation instructions, please see the [Installation](/installation/) page.

This release packages many changes, such as:

- Block backup files ending with ~ in filename (Andrea Menin)
- Detect ffuf vuln scanner (Will Woodson)
- Detect Nuclei vuln scanner (azurit)
- Detect SemrushBot crawler (Christian Folini)
- Detect WFuzz vuln scanner (azurit)
- New LDAP injection rule (Christian Folini)
- New HTTP Splitting rule (Andrea Menin)
- Add .swp to restricted extensions (Andrea Menin)
- Allow CloudEvents content types (Bobby Earl)
- Add CAPEC tags for attack classification (Fernando Outeda, Christian Folini)
- Detect Unix RCE bypass techniques via uninitialized variables, string concatenations and globbing patterns (Andrea Menin)
- Many improvements to lower the number of false positives and improve attack detections

Important upgrade notes:

- The format of configuration setting `allowed_request_content_type` has been changed to be more in line with other variables. If you had manually changed this setting, then you need to update it. Please see the example rule 900220 in the file crs-setup.conf.example. If you **didn’t** change this setting, you don’t need to do anything.
- We removed rule tags WASCTC, OWASP\_TOP\_10, OWASP\_AppSensor/RE1, and OWASP\_CRS/FOO/BAR since our tags were mostly out-of-date and incomplete, and therefore less useful; note that tags 'OWASP\_CRS' and 'attack-type' were kept. So, for instance, if you had a exclusion rule `ctl:ruleRemoveTargetByTag=XSS`, you should change it to `ctl:ruleRemoveTargetByTag=attack-xss`.

Please see the CHANGES document with around 160 entries for the complete list of new features and improvements: [https://github.com/coreruleset/coreruleset/blob/v3.3.0/CHANGES](https://github.com/coreruleset/coreruleset/blob/v3.3.0-rc2/CHANGES)

Finally, we have done a lot of infrastructure work during this release, such as the move from TrustWave to our own GitHub organization and the conversion of our CI to GitHub Actions. We are very grateful to our developers who have invested much time in this process, with a special nod to developer Felipe Zipitria who created a GitHub bot to preserve all the project's issue history.

Our desire is to see the Core Rule Set project used as a baseline security feature, effectively protecting from OWASP TOP 10 risks with few side effects. As such we attempt to cut down on false positives as much as possible in the default install. Please use the CRS GitHub (<https://github.com/coreruleset/coreruleset>), our slack channel ([\#coreruleset](https://owasp.slack.com/archives/CBKGH8A5P) on [owasp.slack.com](https://owasp.slack.com)), or the Core Rule Set mailing list to tell us about your experiences, including false positives or other issues with this release!

Sincerely,  
Walter Hop, release manager, on behalf of the Core Rule Set development team
