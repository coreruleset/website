---
author: Chaim Sanders
categories:
  - Blog
date: '2018-03-14T06:37:37+01:00'
guid: https://coreruleset.org/?p=671
id: 671
permalink: /20180314/crs-project-news-march-2018/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: CRS Project News March 2018
url: /2018/03/14/crs-project-news-march-2018/
---


This is the CRS newsletter covering the period from Early February until today.

We held our monthly community chat. We had quite a few people stop by.

- csanders
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c19 user hasUserParent link" role="button" title="lifeforms (~walter@nagorno.karabakh.nl)">lifeforms</span>
- franbuehler
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c2 user hasUserParent link" role="button" title="emphazer (3e8fef11@gateway/web/freenode/ip.62.143.239.17)">emphazer</span>
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c0 user hasUserParent link" role="button" title="dune73 (~dune73@93-94-243-179.static.monzoon.net)">dune73</span>
- agi
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c4 user hasUserParent link" role="button" title="squared (~squared@24.114.221.218)">squared</span>
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c4 user hasUserParent link" role="button" title="fzipi_ (~fzipi@190.64.49.27)">fzipi\_</span>
- <span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c8 user hasUserParent link" role="button" title="spartantri (~spartan@37.171.48.140)">spartantri</span>

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/1026). During the chat we discussed the following:

We added support for ModSecurity-v3/Apache and Modsecurity-v2/Nginx to the [CRS Support ModSecurity Docker Repos](https://github.com/CRS-support/modsecurity-docker). These will be used when testing before a release. Additionally, we will be adding testing with Nginx+FTW in addition to Apache+FTW.

A blog about the current CI process will be created for next month.

Issue #[990](https://github.com/coreruleset/coreruleset/issues/990) status : Only issue was with FTW failing tests, this has since been fixed. This was merged.

CRS Summit at AppSec EU: <span class="message"><span class="content"> The proposed CRS Summit will be on July 4, 4pm in London, the closing day of the trainings, the night before the real conference starts.</span></span>

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