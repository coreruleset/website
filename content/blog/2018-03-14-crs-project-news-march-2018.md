---
author: csanders-git
categories:
  - Blog
date: '2018-03-14T06:37:37+01:00'
title: CRS Project News March 2018
---


This is the CRS newsletter covering the period from Early February until today.

We held our monthly community chat. We had quite a few people stop by.

- csanders
- lifeforms
- franbuehler
- emphazer
- dune73
- agi
- squared
- fzipi
- spartantri

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/1026). During the chat we discussed the following:

We added support for ModSecurity-v3/Apache and Modsecurity-v2/Nginx to the [CRS Support ModSecurity Docker Repos](https://github.com/CRS-support/modsecurity-docker). These will be used when testing before a release. Additionally, we will be adding testing with Nginx+FTW in addition to Apache+FTW.

A blog about the current CI process will be created for next month.

Issue #[990](https://github.com/coreruleset/coreruleset/issues/990) status : Only issue was with FTW failing tests, this has since been fixed. This was merged.

CRS Summit at AppSec EU: 

Dune73, Tin Zaw, and csanders-git submitted CFPs to AppSec EU.

\#1013 FP resolution status: was merged.

\#994 File detection: was built against ubuntu with ModSecurity on Apache. This was causing conflicts. We decided as an organization to switch our CI testing env to Ubuntu (instead of fedora).

\#989 Fix Regression Tests: For some reasons even though tests were fixed, these still failed, we'll be rebasing and that should fix the issue.

remaining @azhao155 issues represent actual issues with how the rules are written.

CRS 3.1 release date shooting for May 2018

csanders-git put forth a number of options for increasing project management capabilities within the project. A further email will be sent out.

**Announcements:**

- Posted a blog post from Karl Stoney - Creating an OpenWAF solution with Nginx, ElasticSearch and ModSecurity
- Posted a blog post from Christian Peron - Building a WAF test harness
- Posted a blog post from Christian Folini - How to tune your WAF installation to reduce false positives

**The next community chats will be held on the following dates:**

April 2, 2018 20:30 CET

May 7, 2018 20:30 CET

June 4, 2018 20:30 CET
