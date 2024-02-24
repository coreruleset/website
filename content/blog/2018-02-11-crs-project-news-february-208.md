---
author: csanders-git
categories:
  - Blog
date: '2018-02-11T05:10:03+01:00'
permalink: /20180211/crs-project-news-february-208/
title: CRS Project News February 2018
url: /2018/02/11/crs-project-news-february-208/
---


This is the CRS newsletter covering the period from Early January until today.

We held our monthly community chat. We had quite a few people stop by.

- csanders
- airween
- franbuehler
- lifeforms
- spartantri
- dune73
- allanbo

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/1003). During the chat we discussed the following:

Issue \#[989](https://github.com/coreruleset/coreruleset/issues/989) status: Currently waiting on canders to fix Dockerfile before it can merged. The Dockerfile’s point to csanders-git’s personal repository instead of CRS repo. This is done in error. csanders will change config default for docker to build on ubuntu and not fedora.

Issue \#[990](https://github.com/coreruleset/coreruleset/issues/990) status : This ticket is a requisite for OWASP CRS 3.1 release. This is currently under review by Lifeforms and Dune73 after changes made during the week before the meeting.

Issue #[994](https://github.com/coreruleset/coreruleset/issues/994) status: This pull requests detects certain file types by looking into the request body no matter the content-type or extension. The discussion centered around potential performance issues that would be incurred by requiring body access. The decision was that body access should left to the WAF (such as ModSecurity) to control. The rule be will be in PL2. The current decision is to enable it via CRS seutp.conf. This will also need tests before merged.

Issue \#[1004](https://github.com/coreruleset/coreruleset/issues/1004) replaces the #[1000](https://github.com/coreruleset/coreruleset/issues/1000), merging to the correct branch. Contains a fix for performance issues. Looking for more detail on the use of xml:\* which was added by Dune. He was working in conjunction with Achim Hoffmann back in 2015. He’ll message Achim and get an answer.

Issue #[1008](https://github.com/coreruleset/coreruleset/issues/1008) status: csanders has been working on fixing many of the FP tests in FTW that azhao155 noticed. These have all been merged into one PR.

Issue #[1009](https://github.com/coreruleset/coreruleset/issues/1009) status: Franbueler was volunteered to review this.

Issue #[1011](https://github.com/coreruleset/coreruleset/issues/1011) status: Is a rather striaght forward PR that can simply be merged when reviewed.

Issue #[731](https://github.com/coreruleset/coreruleset/issues/731) status: emphazer was unable to finish last month but is looking to finish this month.

There is an acceptable task that's been opened for a new volunteer dealing with rule cleanup. This was opened as #[1015](https://github.com/coreruleset/coreruleset/issues/1015).

Dune73 and csanders will work offline to determine the best way to minimize the amount of issues. This may include combining labels and adding won't fix tags in KNOWN\_BUGS or TODO files.

**Announcements:**

- New draft of the poster [https://www.christian-folini.ch/poster1.jpg](https://www.christian-folini.ch/poster1.jpg). It’ll be sold through a poster store.
- Dune has a ModSec talk in Geneva in February 22 [https://swiss-cybersecurity.ch/upcoming-events](https://swiss-cybersecurity.ch/upcoming-events)
- Netnea has an open position as posted on the ML, contact Dune73 for more information.

**The next community chats will be held on the following dates:**

March 5, 2018 20:30 CET

April 2, 2018 20:30 CET

May 7, 2018 20:30 CET
