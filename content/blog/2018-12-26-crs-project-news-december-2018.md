---
author: dune73
categories:
  - Blog
date: '2018-12-26T13:13:28+01:00'
permalink: /20181226/crs-project-news-december-2018/
tags:
  - CRS-News
title: CRS Project News December 2018
url: /2018/12/26/crs-project-news-december-2018/
---


I hope everybody has a few calm days to finish the year. CRS is finishing the year enjoying the 3.1 release and an adjustment to the PHP rules that closes a nasty hole in the detection.

### **What has happened in recent weeks**

- CRS 3.1 has been released bringing new rules to detect Java injections and an easier way to deal with paranoia levels. More changes in the announcement.  
    Link: {{< ref "blog/2018-11-28-announcement-owasp-modsecurity-core-rule-set-version-3-1-0.md" >}}
- CRS Co-Lead Christian Folini taught two CRS crash courses together with David Jardin from Siwecos in Bern and Zurich, Switzerland. The course was sponsored by Switch (The Swiss NIC) and addressed internet hosters. One result was a new initiative to run a workshop at the Cloudfest conference in late March to come up with a CRS profile that works for internet hosters. There will be a separate announcement, when we know more.
- CRS committer Franziska Bühler pubished a blog post introducing the extensions for the official CRS docker container that she developed. The extensions allow you to configure a CRS container including the backend connection from the command line.  
    Link: {{< ref "blog/2018-12-12-core-rule-set-docker-image.md" >}}
- CRS Co-Lead Christian published an asciinema demo video illustrating Franziska's work.  
    Link: <https://asciinema.org/a/0JDnaO1Wi42sIYpgJzoYbCdtn>
- The American company Gridvision published a success story how they secured their WordPress setup with CRS.  
    Link: <https://gridvision.net/projects/nginx-modsecurity-and-project-honeypot/>
- CRS contributor TheMiddle published a blog post with WAF bypasses aiming for PHP. As usual, CRS was doing better than many other WAFs, but there is a particularly sinister bypass we did not detect in lower paranoia levels (more news about this below).  
    Link: <https://www.secjuice.com/php-rce-bypass-filters-sanitization-waf/>

### Significant pull requests that were merged

With the 3.1 release out the door, the development for 3.2 was immediately revived. Pull requests are coming in nicely now.

- CRS committer Federico Schwindt continued his work to drop unneeded capture groups, which results in better performance and better readability.all around.  
    Link: [https://github.com/coreruleset/coreruleset/pulls?utf8=%E2%9C%93&amp;q=is%3Apr+%22capture+groups%22](https://github.com/coreruleset/coreruleset/pulls?utf8=%E2%9C%93&q=is%3Apr+%22capture+groups%22)
- CRS Co-Lead Walter Hop reacted to the publication by TheMiddle (see above) very quickly and provided a pull request to get rid of a particularly nasty bypass where an attacker would use the PHP `get_defined_functions()` functionality to enumerate dangerous calls without naming them explicitly.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1268>
- CRS contributor TheMiddle wrote a pull request to add the "application/xss-auditor-report" content type to the list of permitted content types.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1243>

### Things that are meant to happen in the coming weeks or thereafter

- Details for the CRS internet hoster workshop at Cloudfest in Germany at the end of March.
- CRS Co-Lead Christian Folini is teaching a CRS / ModSecurity course on 28th/29th March 2019 in Zurich, Switzerland. 2 early bird tickets are still available.  
    Link: <https://www.eventbrite.com/e/modsecurity-owasp-core-rule-set-masterclass-tickets-53678669345>
- CRS committer Franziska is planning to work with Co-Lead Chaim Sanders to get her work into the official CRS docker container that is distributed together with the project.
- The next Monthly Community Chat will be held on January 7, 2019, at 20:30 CET in the #coreruleset channel in the OWASP Slack. A link to a slack invite can be found in the agenda linked below. Please use this agenda issue on github to schedule topics for discussion.  
    Link: <https://owasp.slack.com>  
    Link: <https://github.com/coreruleset/coreruleset/issues/1272>

### Important pull requests in the queue

- New rule 941360 to detect JSFuck and Hieroglyphy at PL1  
    Link: <https://github.com/coreruleset/coreruleset/pull/1261>
- CRS committer Federico Schwindt submitted the final pull request to drop unneeded capture groups.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1270>
