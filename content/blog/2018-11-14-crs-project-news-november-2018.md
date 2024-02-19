---
author: Christian Folini
categories:
  - Blog
date: '2018-11-14T22:04:29+01:00'
guid: https://coreruleset.org/?p=835
id: 835
permalink: /20181114/crs-project-news-november-2018/
site-content-layout:
  - default
site-sidebar-layout:
  - default
tags:
  - CRS-News
theme-transparent-header-meta:
  - default
title: CRS Project News November 2018
url: /2018/11/14/crs-project-news-november-2018/
---


The plan is to do this newsletter every month, but it's already November. The reason is the pending 3.1 release, so I waited for the release to happen and then it did not and suddenly October was over. But now we have a 3.1-RC2 and a strong belief that 3.1 will come out for good on Sunday November 24.

**What has happened in recent weeks**

- CRS 3.1 RC2 has been released.  
    It brings few bugfixes over 3.1 RC1 and we think it will be very close to the eventual stable 3.1 release.  
    Download: <https://github.com/coreruleset/coreruleset/releases/tag/v3.1.0-rc2>
- The CRS project has decided to prioritize 3.1 and abandon the 3.0 release line. So there won't be a 3.0.3 release.
- The development has been slow with picking up again. We're working on the 3.2/dev branch but it feels like the pending 3.1 is keeping the project back.  
    Link: <https://github.com/coreruleset/coreruleset>
- libModSecurity 3.0.3 has been released. This is a release focues on code readability, resilience and performance. This is an important move as ModSecurity 3.0.2 has been breaking CRS 3.1 and we worked very hard on the ModSecurity developers to have them release 3.0.3 before we do our 3.1. (The delay with our 3.1 release is entirely our fault, though.)  
    Link: <https://github.com/SpiderLabs/ModSecurity/releases/tag/v3.0.3>  
    Link: <https://github.com/SpiderLabs/ModSecurity/releases/tag/v3.0.3/CHANGES>
- We shifted the monthly community chat from IRC to the #coreruleset channel on the OWASP Slack.
- CRS developer Christoph Hansen has published a script to convert the modern GeoIP database into the legacy format that ModSecurity 2.x supports. This solves a major problem for many users.  
    [https://github.com/emphazer/GeoIP\_convert-v2-v1](https://github.com/emphazer/GeoIP_convert-v2-v1)
- Linux Journal article on ModSec / CRS on NGINX  
    Link: <https://www.linuxjournal.com/content/modsecurity-and-nginx>
- Mikhail Golovanov has published an article about ModSecurity rule verification. Among many interesting ideas, he also demonstrates a way to create payloads from a regular expression in a rule.  
    Link: <https://waf.ninja/modsecurity-rules-verification/>
- The Company Approach from Belgium has released the source code for an Apache module that brings a new transformation to ModSecurity: t:bash. Ideally, this source code will be integrated into ModSecurity, and ultimately be supported by CRS, but we are quite far from that. You can use it immediately for your own rules, though.  
    Link: <https://www.approach.be/en/modsecurity.html>

### Significant pull requests that were merged

- Java rules bug that the last news reported about has been fixed.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1198>  
    Link: <https://github.com/coreruleset/coreruleset/issues/1185>
- Several typos in variable names have been spotted and fixed (Victor Hora)  
    Link: <https://github.com/coreruleset/coreruleset/pull/1187>
- Dropped the keyword "exit" from both, Unix and Windows RCE rules (Federico Schwindt)  
    Link: <https://github.com/coreruleset/coreruleset/pull/1204/files>
- Bugfix with new paranoia level counters (Federico Schwindt)  
    Link: <https://github.com/coreruleset/coreruleset/pull/1196>

### Things that are meant to happen in the coming weeks

- We plan to release CRS 3.1 on Sunday November 24.
- There are going to be two separate one-day ModSecurity / CRS courses for ISPs / Hosters focusing on CMS. Christian Folini and David Jardin from SIWECOS will teach both courses on invitation by SWITCH.  
    The first course will be on December 5 in Bern, Switzerland and the second course will be on December 6 in Zurich, Switzerland.  
    Link: [<span class="js-display-url">https://swit.ch/CMS\_Bern</span>](https://t.co/fhUaCE5rD2 "https://swit.ch/CMS_Bern")  
    Link: [https://swit.ch/CMS\_Zurich](https://swit.ch/CMS_Zurich)
- CRS developer Franziska Bühler is working on her docker container. She is adding CLI support for all the CRS variables during "docker create". This means you will be able to create and configure a CRS WAF container on the fly with a one-liner. This is meant to be merged into the official CRS docker container eventually.  
    Link: <https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/>
- The next Monthly Community Chat will be held on December 3, 2018, at 20:30 CET in the #coreruleset channel in the OWASP Slack. A link to a slack invite can be found in the agenda linked below. Please use this agenda issue on github to schedule topics for discussion.  
    Link: <https://owasp.slack.com>  
    Link: <https://github.com/coreruleset/coreruleset/issues/1238>
- CRS developer Felipe Zipitria has volunteered to come up with a proposal to have CRS swag produced via an online print-on-demand shop. Desired items include posters, stickers, buttons, T-Shirts, ideally the full program.  
    Link: <https://github.com/OWASP/owasp-swag>

### Important pull requests in the queue

- TheMiddleBlue suggests to add additional PHP wrappers to our data file. Still not merged.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1172>
- Manuel Spartan suggests to add missing Java Classes.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1156>