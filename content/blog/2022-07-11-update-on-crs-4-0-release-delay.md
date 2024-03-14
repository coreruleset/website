---
author: Walter Hop
categories:
  - Blog
date: '2022-07-11T12:40:38+02:00'
title: Update on CRS 4.0 release delay
url: /2022/07/11/update-on-crs-4-0-release-delay/
---


Dear all,

A few months ago we happily [announced](https://coreruleset.org/20220428/coreruleset-v4-rc1-available/) the first Release Candidate for Core Rule Set 4.0.

Our original plan was to finish the 4.0 release as fast as possible. However, we found ourselves in a unique situation for our project.

After the Release Candidate, a large CRS user organized a CRS Bug Bounty event, where advanced WAF hackers were tasked to bypass our ruleset to earn prizes. Since a similar earlier event did not uncover any findings, we were expecting to only get a small number of bug reports. But the hackers turned out to be amazing and created more than 100 malicious payloads that bypassed our detection!

As you can imagine, the large number of findings from the Bug Bounty threw a big wrench in our CRS 4.0 release planning... There is suddenly a lot of work for us to do. We have discussed various strategies and settled on the following.

Our plan at this time is to resolve as many of the findings as possible before releasing 4.0. This will unfortunately delay the CRS 4.0 release for quite some time, but at the same time, it will make 4.0 the most battle-tested CRS release ever, and it will be worth the wait!

We decided not to do a 'partial fix' for 4.0 (and continue fixing bugs in 4.1, 4.2 etc.), since it feels bad to do a release with a large number of known bypasses. Instead, 4.0 seems the best time to introduce a large volume of new protections together with the [plugin mechanism](https://coreruleset.org/docs/concepts/plugins/), even if it means we will have a serious delay.

Since we depend on the work of our volunteer developers to write rules to block these payloads, we cannot really predict when we will be finished processing all the bug bounty findings.

We will be working hard to make it as fast as possible, though! First, the Bug Bounty sponsor helped us by giving extra prizes to hackers who created patches, which are now being code-reviewed and integrated by our developers. We also started a program to periodically review our blocklists to improve our coverage of new SQL dialect functions, Javascript snippets, Java classes, Unix commands, and so on. Next, we will hold a virtual hackathon with our developers in August to solve issues as a team. We have also sponsored a developer to create regression tests for the discovered payloads, which will help us in resolving the issues — but it's hard to tell how our velocity will be. It might take us several months before we are ready for a release. In any case we should have a clearer picture in late August.

If you feel like you want to have bleeding edge rules with the latest fixes, then we suggest you follow the v4/dev tree closely or run the [nightly builds](https://github.com/coreruleset/coreruleset/releases/tag/nightly), since we add the fixes in our main development tree to the widest extent.

I can imagine this delay is unwelcome for those who were waiting for CRS 4.0. I thank everybody for your understanding of our situation. We will keep you informed after we have resolved more of the issues; then we will be in a better position to plan and restart the CRS 4.0 release process.

Kind regards,  
Walter Hop  
Core Rule Set Co-Lead
