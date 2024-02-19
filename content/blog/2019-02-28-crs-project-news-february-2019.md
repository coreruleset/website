---
author: Christian Folini
categories:
  - Blog
date: '2019-02-28T09:57:50+01:00'
guid: https://coreruleset.org/?p=954
id: 954
permalink: /20190228/crs-project-news-february-2019/
site-content-layout:
  - default
site-sidebar-layout:
  - default
theme-transparent-header-meta:
  - default
title: CRS Project News February 2019
url: /2019/02/28/crs-project-news-february-2019/
---


We are back with the CRS project news. The news are running very, very late in the month as I've been held up with other projects.

### **What has happened in recent weeks**

- Miyuru Sankalpa has started to publish a transformed GeoIP database in the legacy format readable by ModSecurity 2.x under a creative commons. This seems to be based on the MaxMind databases and it is not clear of MaxMind endorses this initiative.  
    Link: <https://www.miyuru.lk/geoiplegacy>
- CRS developer Andrea Menin has released a set of ModSecurity rules that complement CRS when protecting WordPress.  
    Link: <https://github.com/Rev3rseSecurity/wordpress-modsecurity-ruleset>
- Andrea Menin has also written a tutorial about DNS over HTTPS and how to protect and integrate it using ModSecurity.  
    Link: <https://www.secjuice.com/modsecurity-web-application-firewall-dns-over-https/>
- Microsoft has forked ModSecurity 2.x on github and it is (according sombody working on the project) working on patches that allow better integration with the Azure Cloud.  
    Link: <https://github.com/Microsoft/ModSecurity>
- CRS developer Franziska Bühler has integrated CRS together with the Pixie learning app into a new docker container. This allows for easy training sessions and checking out attacks against the naked Pixie and the one protected by CRS.  
    Link: <https://github.com/DevSlop/pixi-crs-demo>

### Significant pull requests that were merged

- CRS develop Andrea Menin contributed a rule to prevent PHP rule bypasses via variable functions.  
    Link:[ https://github.com/coreruleset/coreruleset/pull/1294](https://github.com/coreruleset/coreruleset/pull/1294)
- Github user siric1 contributed a rule exclusion that brings support for the WordPress Gutenberg editor.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1298>
- CRS co-lead Walter Hop added the "Jorgee" to the list of security scanners detected by CRS.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1307>
- CRS co-lead Walter Hop added the "ZGrab" to the list of security scanners detected by CRS.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1305>

### Things that are meant to happen in the coming weeks or thereafter

- The Core Rule Set project will participate at the Cloudfest Hackathon in Germany on March 23 - 25 under the direction of Walter Hop and Christoph Hansen. The idea is to develop rules, rules exclusions and documentation to allow easier integration of CRS for internet hosters. Registration is open.  
    Link: <https://www.cloudfest.com/hackathon>
- The Core Rule Set project will hold a Community Summit on Tuesday May 28, the day before the OWASP AppSecGlobal in Tel Aviv. This will follow the same format of the Community Summit we did at AppSecEU in London in 2018. Details pending.
- Swiss Post is runing a public intrusion against its Online-Voting system, that is protected by the Core Rule Set as a first layer of defense. The test runs from February 25 to March 24, 2019.  
    Link: <https://www.evoting-blog.ch/en/pages/2019/public-hacker-test-on-swiss-post-s-e-voting-system>
- The next Monthly Community Chat will be held on Monday March 4, 2019, at 20:30 CET in the #coreruleset channel in the OWASP Slack. A link to a slack invite can be found in the agenda linked below. Please use this agenda issue on github to schedule topics for discussion.  
    Link: <https://owasp.slack.com>  
    Link: <https://github.com/coreruleset/coreruleset/issues/1314>

### Important pull requests in the queue

- CRS developer Federico Schwindt contributed a rule to detect when Content-Length and Transfer-Encoding are sent in the same request.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1310>
- CRS developer Federico Schwindt wants to add the request path to the targets of rule <span class="blob-code-inner">941110</span> (XSS Filter - Category 1: Script Tag Vector).  
    Link: <https://github.com/coreruleset/coreruleset/pull/1306>
- CRS developer Federico Schwindt contributed a patch where he aims to improve the java detection rules.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1287>