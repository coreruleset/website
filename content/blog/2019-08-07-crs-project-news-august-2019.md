---
author: Christian Folini
categories:
  - Blog
date: '2019-08-07T22:45:43+02:00'
permalink: /20190807/crs-project-news-august-2019/
tags:
  - CRS-News
title: CRS Project News August 2019
url: /2019/08/07/crs-project-news-august-2019/
---


Life is interfering and the rhythm of the CRS news is not what I would like it to be. Three months since the last edition. But the advantage is of course, that there are more news to talk about once I get to write it all up.

#### What has happened in recent weeks

- The OWASP Honeypot project that is based on CRS is running a Google Summer of Code  
    project, that aims for an up do date containerization of the honeypot.  
    Link:  
    <https://docs.google.com/document/d/1nyXuuS90TAy-UyeCE3vsoR7V5fUQ2adbxguEWdKjbiQ/edit>
- O'Reilly is distributing a free 40 pages brochure about "Defense in Depth" by Stephen Gates.  
    CRS is featured prominently on page 22: "Today, most WAF vendors have implemented the OWASP ModSecurity Core Rule Set (CRS), which contains generic attack detection rules for use with ModSecurity or compatible WAFs."  
    Link:  
    <https://www.oreilly.com/library/view/modern-defense-in/9781492050360/>
- Zevenet has patched the traditional - but rather exotic - reverse proxy Pound to work with ModSecurity 3 and thus with CRS.  
    Link:  
    <https://github.com/zevenet/pound>
- The pressing ReDoS problems that resulted in 5 (!) CVEs issued against CRS could be solved with the release of 3.1.1 that is functionally equivalent to 3.1.0 and does not suffer from the problems. We also found out, that 4 of the 5 CVEs were bogus and the 5th is only exploitable in few installations. We are talking to Mitre, but they have not really be very forthcoming so far.  
    A word of caution: This does not mean that there are no more ReDoS problems in CRS. We are working through the rules and we think we have identified most problematic rules, but ReDoS is nasty as long as you run on PCRE and we are not quite ready to support an alternative engine like RE2 (but we are working on it; see below).  
    Link:  
    <{{< ref "blog/2019-06-27-announcement-owasp-modsecurity-core-rule-set-version-3-1-1.md" >}}>.
- There is a new, bi-monthly CRS / ModSecurity Meetup in Bern, Switzerland. The first edition ran on June 26 2019 and we got 14 people together in the room.  
    Link:  
    <https://www.meetup.com/CRS-ModSecurity-Meetup-Bern/>  
    <https://www.puzzle.ch/de/blog/articles/2019/07/02/erstes-treffen-der-crs-community-in-bern>
- Brian Krebs blogged about the CapitalOne breach and blamed it on an SSRF (server-side request forgery) on the ModSecurity WAF running CRS. However, this is likely wrong as a more detailed blog post at AppSecco explained. It's rather a SSRF that CRS did not block. Either because it was not detected (that is quite likely, as SSRF is really hard to detect with generic rules) or because the WAF was in monitoring mode.  
    Link:  
    <https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/>  
    <https://blog.appsecco.com/an-ssrf-privileged-aws-keys-and-the-capital-one-breach-4c3c2cded3af?gi=97a1dfb34c64>
- We did our monthly CRS project chats. Here are the agendas and the brief protocols.  
     Link:  
     <https://github.com/coreruleset/coreruleset/issues/1402> (May)  
     <https://github.com/coreruleset/coreruleset/issues/1443> (June)  
     <https://github.com/coreruleset/coreruleset/issues/1471> (July)  
     <https://github.com/coreruleset/coreruleset/issues/1496> (August)

#### Significant pull requests that were merged

- There have been several PRs that dealt with ReDoS problems in multiple rules.
- We are cleaning CRS from PCRE-specific back-tracking, that is not supported in alternative implementations like RE2, which is a lot safer with regards to ReDoS.
- The SQLi libinjection check has been added for the last path segment  
    Link:  
    <https://github.com/coreruleset/coreruleset/pull/1492>
- A new rule exclusion profile for XenForo has been contributed:  
    Link:  
    <https://github.com/coreruleset/coreruleset/pull/1403>
- Massive Updates for the CRS docker container that bring easier integration and easy configurability via ENV variables (Think Anomaly score limits, paranoia levels, backend address).  
    Link:  
    <https://github.com/coreruleset/coreruleset/pull/1457>  
    <https://github.com/coreruleset/coreruleset/pull/1455>  
    <https://github.com/coreruleset/coreruleset/pull/1454>  
    <https://github.com/coreruleset/coreruleset/pull/1453>

#### Things that are meant to happen in the coming weeks or thereafter

- We are planning to release CRS 3.2. Release manager Walter Hop confirmed the following plan:  
    Freeze on August 19, RC1 on August 26, RC2 on September 8, release on September 24.  
    Link:   
    <https://github.com/coreruleset/coreruleset/issues/1496#issuecomment-518348210>
- The next CRS / ModSecurity meetups in Bern, Switzerland, will be on August 28 and thereafter on October 30.  
    On August 28, we'll talk about Paranoia Levels in Practice. The program for October 30 has not been fixed yet.  
    Link:  
    <https://www.meetup.com/CRS-ModSecurity-Meetup-Bern/>
- We are hosting a CRS Community Summit on September 25 at the RAI in Amsterdam. This is the last training day at the OWASP AppSec Global conference. This is meant for users of CRS, for integrators and committers or our project. Entry to the summit is free, but it makes sense to combine with the AppSec conference the next day of course if you make the trip to the Netherlands.  
    The Summit will start in the early afternoon and we are going to have a dinner together afterwards.  
    Please get in touch if you plan to attend, so we can accomodate enough seats at the RAI (and at the restaurant afterwards):  
    Link:  
    christian.folini / at / owasp.org
- Christian Folini is going to present at the OWASP AppSec Global conference in Amsterdam on September 26 / 27. His talk will be about Practical CRS in high security settings.  
    Link:  
    <https://ams.globalappsec.org/>

#### Important pull requests in the queue

- There is a PR for a new rule aiming at insecure unserialization in NodeJS. This is meant to be the first rule in a new rule group (REQUEST-934-APPLICATION-ATTACK-NODEJS.conf) that is going to be released together with CRS 3.2 if according to plan.  
    Link:  
    <https://github.com/coreruleset/coreruleset/pull/1487>
- Not much more of much importance is in the queue. We have been very active with merging those last few weeks. There are just a few bugfixes here and there plus more tests.

*News assembled by Christian Folini, CRS Co-Lead.*
