---
author: Chaim Sanders
categories:
  - Blog
date: '2018-02-11T05:10:03+01:00'
guid: https://coreruleset.org/?p=649
id: 649
permalink: /20180211/crs-project-news-february-208/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: CRS Project News February 2018
url: /2018/02/11/crs-project-news-february-208/
---


This is the CRS newsletter covering the period from Early January until today.

We held our monthly community chat. We had quite a few people stop by.

- <span style="font-weight: 400;">csanders</span>
- <span style="font-weight: 400;">airween</span>
- <span style="font-weight: 400;">franbuehler</span>
- <span style="font-weight: 400;">lifeforms</span>
- <span style="font-weight: 400;">spartantri</span>
- <span style="font-weight: 400;">dune73</span>
- <span style="font-weight: 400;">allanbo</span>

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/1003). During the chat we discussed the following:

Issue <span style="font-weight: 400;">\#[989](https://github.com/coreruleset/coreruleset/issues/989) status: Currently waiting on canders to fix Dockerfile before it can merged. The Dockerfile’s point to csanders-git’s personal repository instead of CRS repo. This is done in error. csanders will change config default for docker to build on ubuntu and not fedora.</span>

Issue <span style="font-weight: 400;">\#[990](https://github.com/coreruleset/coreruleset/issues/990) status : This ticket is a requisite for OWASP CRS 3.1 release. This is currently under review by Lifeforms and Dune73 after changes made during the week before the meeting.</span>

Issue #[994](https://github.com/coreruleset/coreruleset/issues/994) status: This pull requests <span style="font-weight: 400;">detects certain file types by looking into the request body no matter the content-type or extension. The discussion centered around potential performance issues that would be incurred by requiring body access. The decision was that body access should left to the WAF (such as ModSecurity) to control. The rule be will be in PL2. The current decision is to enable it via CRS seutp.conf. This will also need tests before merged.</span>

Issue <span style="font-weight: 400;">\#[1004](https://github.com/coreruleset/coreruleset/issues/1004) replaces the #[1000](https://github.com/coreruleset/coreruleset/issues/1000), merging to the correct branch. Contains a fix for performance issues. Looking for more detail on the use of xml:\* which was added by Dune. He was working in conjunction with Achim Hoffmann back in 2015. He’ll message Achim and get an answer.</span>

<span style="font-weight: 400;">Issue #[1008](https://github.com/coreruleset/coreruleset/issues/1008) status: csanders has been working on fixing many of the FP tests in FTW that </span><span style="font-weight: 400;">azhao155 noticed. These have all been merged into one PR.</span>

Issue #[1009](https://github.com/coreruleset/coreruleset/issues/1009) status: <span style="font-weight: 400;">Franbueler was volunteered to review this.</span>

Issue #[1011](https://github.com/coreruleset/coreruleset/issues/1011) status: I<span style="font-weight: 400;">s a rather striaght forward PR that can simply be merged when reviewed.</span>

<span style="font-weight: 400;">Issue #[731](https://github.com/coreruleset/coreruleset/issues/731) status: emphazer was unable to finish last month but is looking to finish this month.</span>

There is an acceptable task that's been opened for a new volunteer dealing with rule cleanup. This was opened as #[1015](https://github.com/coreruleset/coreruleset/issues/1015).

Dune73 and csanders will work offline to determine the best way to minimize the amount of issues. This may include combining labels and adding won't fix tags in KNOWN\_BUGS or TODO files.

**Announcements:**

- <span style="font-weight: 400;">New draft of the poster </span>[<span style="font-weight: 400;">https://www.christian-folini.ch/poster1.jpg</span>](https://www.christian-folini.ch/poster1.jpg)<span style="font-weight: 400;">. It’ll be sold through a poster store.</span>
- <span style="font-weight: 400;">Dune has a ModSec talk in Geneva in February 22 </span>[<span style="font-weight: 400;">https://swiss-cybersecurity.ch/upcoming-events</span>](https://swiss-cybersecurity.ch/upcoming-events)
- <span style="font-weight: 400;">Netnea has an open position as posted on the ML, contact Dune73 for more information.</span>

**The next community chats will be held on the following dates:**

March 5, 2018 20:30 CET

April 2, 2018 20:30 CET

May 7, 2018 20:30 CET