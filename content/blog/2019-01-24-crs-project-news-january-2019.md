---
author: dune73
categories:
  - Blog
date: '2019-01-24T16:37:11+01:00'
permalink: /20190124/crs-project-news-january-2019/
tags:
  - CRS-News
title: CRS Project News January 2019
url: /2019/01/24/crs-project-news-january-2019/
---

We are back with the CRS project news. We're attending the Cloudfest Hackathon in March in Germany and we have plans for another CRS Community Summit at the new OWASP AppSec Global conference in Tel Aviv at the end of May (formerly OWASP AppSecEU).

### What has happened in recent weeks

- We have reached 1500 stars on GitHub and adding more every day in a nice exponential curve. This makes us one of the most popular OWASP projects on GitHub.  
    Link: [https://seladb.github.io/StarTrack-js/?u=SpiderLabs&amp;r=owasp-modsecurity-crs](https://seladb.github.io/StarTrack-js/?u=SpiderLabs&r=owasp-modsecurity-crs)
- CRS contributor Ervin Hegedüs, supported by Andrea Menin and Walter Hop, is working hard to get the CRS FTW tests to pass with ModSecurity 3 on NGINX and ModSecurity 3 on Apache. These tests are important for including Nginx with ModSecurity 3 in the next Debian release. CRS is currently using ModSecurity 2.9 on Apache as reference platform, but we need to open up for ModSecurity 3 as it is slowly maturing. Ervin and Andrea have now reached a state where over 90% of the tests pass, but they may have also discovered a bug or two in ModSecurity 3. When the work on Debian is done, we will set up our Continous Integration via Travis to run our tests against multiple platforms.
- Angelo Conforti published an interesting piece of code that allows to generate ModSecurity Whitelisting rules based on a Swagger definition. This could be very interesting for securing APIs on top of CRS. This is a work in progress, but it looks promising and I am sure testing is welcome.  
    Link: <https://github.com/angeloxx/swagger2modsec>

### Significant pull requests that were merged

When we stated development had picked up nicely after the release 3.1 the statement contained a lot of hope. But looking over the last four weeks makes it clear that we have indeed accelerated.

- We have retired the update script. We prefer people to download git releases themselves and the GeoIP support for ModSecurity has grown complicated with the database format change and ModSecurity 2.9 falling behind. Consequently we want to focus on our core project goals and GeoIP is not central enough.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1282>
- CRS 3.1 came without the script that allowed to transform CRS 2 rule IDs to CRS 3. We came to see that there are still many legacy installation that are thankful for this script when they are finally updating. So the script it back.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1278>
- CRS committer Christoph Hansen contributed a PR that made sure CRS stays compatible with the JWall Audit Console.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1276>
- CRS committer Christoph Hansen also contributed a new rule that detects misconfigured webservers delivering the source code of CGI scripts instead of running them.  
    Link:[ https://github.com/coreruleset/coreruleset/pull/1275](https://github.com/coreruleset/coreruleset/pull/1275)
- CRS committer Federic Schwindt finished his big project to drop all unneeded capture groups which brings us simpler rules and better performance.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1270>
- CRS co-lead Walter Hop shifted the PHP function get\_defined\_functions() and friends to PL1 in order to close a bypass hole documented by CRS contributer Andrea Menin.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1268>
- CRS commiter Franziska Bühler continued to add CVE information to the group of Java rules.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1268>  
    Link: <https://github.com/coreruleset/coreruleset/pull/1267>
- CRS co-lead Christian Folini contributed a rule to detect JSFuck and Hieroglyphy bypasses in CRS.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1261>

### Things that are meant to happen in the coming weeks or thereafter

- Cloudfest is a very big annual IT conference that is namely addressing hosters. The CRS project will participate at the hackathon in the days prior to the conference with the plan to come up with a rule exclusion package or a installation profile that will allow an internet hoster to run CRS on thousands of domains in parallel without too many false positives.  
    The hackathon runs from Saturday March 23 to Monday March 25. CRS will represented by co-lead Walter Hop and committer Christoph Hansen.  
    Link: <https://www.cloudfest.com/hackathon>
- The traditional European OWASP AppSecEU conference is being transformed into one of several annual AppSec Global conferences. It has just been announced that it will be held in Tel Aviv from May 26 - May 31. (3 days of training, 2 day conference). CRS will be present with the 2nd CRS Community Summit, possibly a hackathon, maybe a training and we will also participate in the call for papers for the official conference. We will keep you posted via the CRS website.
- We have lose plans for CRS 3.1.1, but it's likely to take another month. We scheduled the discussion for the next monthly chat (see below).
- The next Monthly Community Chat will be held on Monday February 4, 2019, at 20:30 CET in the #coreruleset channel in the OWASP Slack. A link to a slack invite can be found in the agenda linked below. Please use this agenda issue on github to schedule topics for discussion.  
    Link: <https://owasp.slack.com>  
    Link: <https://github.com/coreruleset/coreruleset/issues/1291>

### Important pull requests in the queue

- CRS committer Federico Schwindt proposed to add REQUEST\_URI\_RAW to the list of rule targets for the JAVA rules in 944.  
    Link: <https://github.com/coreruleset/coreruleset/issues/1287>
- CRS committer Christoph Hansen wants to make sure the % symbol is always allowed in SOAP requests. However, this might also allow for bypasses using this route.  
    Link: <https://github.com/coreruleset/coreruleset/issues/1286>
