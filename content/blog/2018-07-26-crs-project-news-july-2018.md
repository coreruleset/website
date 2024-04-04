---
author: dune73
categories:
  - Blog
date: '2018-07-26T07:43:50+02:00'
tags:
  - CommunitySummit
  - CRS-News
title: CRS Project News July 2018
url: /2018/07/26/crs-project-news-july-2018/
---


We are launching the monthly news anew. The idea is to look beyond the pure CRS development again and to bring you additional information that touch on our project. As the editor, I (-&gt; Christian Folini) am planning to release this in the first half of the month. This did not work in July, though, but I have a very cute excuse: She's called Giovanna and she is only a couple of days old. We're going to be a bit earlier in August, but also less news apparently.

So here we go for the CRS project newsletter for July 2018:

## What has happened in recent weeks

- We met for the first CRS community summit in London on July 4, 2018 and then for an on-site developer meeting on Friday July 6. There is a blog post covering the Summit (and a photo below).  
    Link: <https://coreruleset.org/20180712/reporting-from-the-first-crs-community-summit-in-london/>
- The dev meeting (replacing the monthly chat for July) was very productive. Below is a list of decisions taken.
- Chaim Sanders has been named release manager for 3.1. We are aiming for CRS 3.1 in September with a release candidate in August. CRS 3.2 should be ready in early Summer 2019.
- We're launching the monthly newsletter anew. It's going to be edited by Christian Folini. This is going to be published via the website.
- AviNetworks presented their proposal for a rules Meta-Language during the summit. It was welcomed with open arms. A committee working on this idea was formed out of attending CRS developers and other people.  
    Link: [https://github.com/avinetworks/owasp-crs-technical-discussion/raw/master/documentation/OWASP\_AppSec\_EU\_2018-Core\_Ruleset.pdf](https://github.com/avinetworks/owasp-crs-technical-discussion/raw/master/documentation/OWASP_AppSec_EU_2018-Core_Ruleset.pdf)
- Adrian Winckles and Mark Graham from Cambridge are reviving the OWASP Honeypot project that aims to examine HTTP attacks in the wild. It is based on ModSecurity and CRS. If you are interested to join, please get in touch with Adrian.  
    Link: [https://www.owasp.org/index.php/OWASP\_Honeypot\_Project](https://www.owasp.org/index.php/OWASP_Honeypot_Project) (Website to be)
- Tin Zaw from Verizon attended the CRS Summit and presented WAFLZ, an alternative open source implementation of the ModSecurity rules language aimed at running CRS. The focus of the engine is on multitenancy and effective use of resources.  
    Link: <https://github.com/VerizonDigital/waflz>
- Rodrigo Martinez from the University of Uruguay presented their work on Machine Learning with ModSecurity and the CRS at the summit. His presentation was based on a paper published earlier this year:  
    Link: <https://arxiv.org/pdf/1803.05529.pdf>
- We have too many issues open on github. Federico Schwindt is starting an initiative to resolve open issues and bring down this number. As an immediate remedy, we are pointing users with support questions to stackoverflow (tag questions with "owasp-crs"). The mailinglist continues to be covered too (but was deemed a bit old-fashioned).  
    Link: <https://stackoverflow.com/questions/tagged/owasp-crs>
- We created a channel named "coreruleset" on the OWASP Slack. There are no plans to move the monthly IRC community meeting just now. If you do not have access to the OWASP slack, you can get an invite from from the link below.  
    Link: <https://owasp.slack.com/>
- Soroush Dalili ([@irsdl](https://twitter.com/irsdl)) presented a series of WAF bypasses at AppSecEU. CRS is affected by a charset manipulation via the Content-Type request header. (See below for a PR closing this hole)  
    Link: <https://www.slideshare.net/SoroushDalili/waf-bypass-techniques-using-http-standard-and-web-servers-behaviour>
- Mazin Ahmed has published a blog post about WAF bypassing via argument separators. He also pointed out that CRS is not affected by this problem.  
    Link: <https://blog.mazinahmed.net/2018/07/html-attribute-separators.html>

## Significant pull requests that were merged

- We merged a patch to v3.1/dev that brings the ability to execute rules in a higher paranoia level without them adding to the scoring. This allows to run PL1, but execute rules from PL2 in order to tune false positives, so you can later raise the PL to PL2 without the risk to block legitimate users. The PR was contributed by Christian Folini.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1076>
- We merged several PRs by Chaim Sanders to improve the docker container and travis integration.
- We merged a PR bringing in a new rule (920340) that improves handling of content length header. The PR was contributed by Walter Hop.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1118>

## Things that are meant to happen in the coming weeks

- We are going to see a 3.1 RC in August
- We're creating an issue template on github that guides the creation of issues (asking for correct description of the problem, log files etc.)
- We've decided to start a list on the website with services / products that come with Core Rule Set integration.
- The next project chat is going to be on August 6, 20:30 CET, as usual in the channel #modsecurity on the freenode (IRC). There is a chance we are going to move to slack for the future, but August is still meant to be on IRC.

## Important pull requests in the queue

- - There is a PR to close a hole with the charset manipulation bypass mentioned above.  
        Link: <https://github.com/coreruleset/coreruleset/pull/1143>
    - GitHub user theMiddleBlue contributed a PR that prevents a bypass of the RCE rules. It is based on a new rule to be executed at PL3.  
        Link: <https://github.com/coreruleset/coreruleset/pull/1136>
    - Federico Schwindt continues his rule cleanup efforts with dropping a series of unneeded capture groups:  
        Link: <https://github.com/coreruleset/coreruleset/pull/1124>
    - Walter Hop contributed additional Content-Type checks in a PR  
        Link: <https://github.com/coreruleset/coreruleset/pull/1103>
    - Manuel Leos Rivas created an advanced PR to check malicious file uploads. Testing is ongoing and it looks like the PR would be split with a non-disputed part being integrated into 3.1 and the rest pushed to a future 3.2.  
        Link: <https://github.com/coreruleset/coreruleset/pull/1045>

If you have news that should be covered in this newsletter, then please submit to me directly via christian dot folini at netnea dot com.

And here is the group photo from the community summit.

{{< figure src="images/2018/07/Group-Photo-1-small.jpg" caption="Group Photo from the CRS Community Summit 2018 in London" >}}

