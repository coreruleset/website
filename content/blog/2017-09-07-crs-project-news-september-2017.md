---
author: Christian Folini
categories:
  - Blog
date: '2017-09-07T16:18:20+02:00'
permalink: /20170907/crs-project-news-september-2017/
tags:
  - CRS-News
title: CRS Project News September 2017
url: /2017/09/07/crs-project-news-september-2017/
---


This is the CRS newsletter covering the period from mid August until today.

**What has happened during the last few weeks:**

- We held our community chat last Monday. Chaim was high in the air so we were only six of us, but Manuel was back so I get the feeling we are slowly growing the project. The big project administration and governance discussions seem to be over for the moment. So we spent a lot of time talking about development, possible roadblocks and code policies.  
    The next community chats will be held on the following dates:  
    - Oct 2, 2017, 20:30 CEST (14:30 EST, 19:30 GMT)  
    - Nov 6, 2017, 20:30 CET  
    - Dec 4, 2017, 20:30 CET

- On August 22, we announced our new website at https://coreruleset.org and our  
     new project logo. The launch was combined with several blog post published:  
     <https://coreruleset.org/20170821/running-crs-rules-only-on-certain-parameters/>  
     [https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released/](https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released)  
     
If you have not read them so far, you are missing something.  
We also tried to get the website and logo into the OWASP connector newsletter, but no luck so far. We might make another attempt next time around.   
Also, we still do not have the SVG version of the logo. However, there are plenty of PNG versions in various sizes available to use for your presentations.  

Administrative detail for transparency: Walter Hop has registered the domain to "Core Rule Set Project" p/a Lifeforms Holding BV in the Netherlands. Project lead Chaim Sanders is also authorized to change the registration.

- One of the policy outcomes from the chat is, that new PRs are supposed to go against the development tree (which is now 3.1/dev). Then they can also be considered for backporting to the stable tree. There will be exceptions, but that's the general rule of thumb.
- Me (Christian) and Walter have mostly been active from the development in August for private / business reasons. But development actually accelerated with new contributors; yet we see that not all issues / PRs get answered in a timely manner.
- There is a remarkable code cleanup happening. See  
<https://github.com/coreruleset/coreruleset/issues/808>  
It is likely the code will be converted to spaces and many small issues will be solved along the way. Parts of the cleanup, namely whitespace stuff, will also be happening on the 3.0 codebase. Emphazer volunteered to support that effort by github users fgsch and fzipi and we will make sure that the PRs coming out of this important project are merged swiftly so that other PRs are not harmed by the big code changes in the code cleanup. This includes this PR which is almost done:  
<https://github.com/coreruleset/coreruleset/pull/838>
- Franbuehler reports good progress on the sqli regex disassembly. She faces problems with certain manual or mixed regexes where the code is not purely machine generated. The idea with this project is still to go for a single PR and then edit the PR together until it is ready. Walter / lifeforms is volunteering to review this.
- We have talked about the idea to change the behaviour of the ruleset depending on the backend employed. You could thus use a config setting to tell CRS if you are running a Windows application server or a GNU/Linux based service on the backend. Namely the Remote Command Execution rules would profit as we now have to make sure evasions targeting cmd.exe and bash do not cause too many false positives. We discussed this again and we think it might be possible to get this working with the rule exclusion mechanism introduced for WordPress and Drupal so far.
- Felipe and Victor / Trustwave Spiderlabs have release the first release candidate for [ModSecurity / libModSecurity 3.0.0](https://www.trustwave.com/Resources/SpiderLabs-Blog/ModSecurity-version-3-0-0-first-release-candidate)

**Upcoming Stuff**

- Robert Whitley and Tin Zaw will present a talk with the title ["Core Rule Set for the Masses"](https://appsecusa2017.sched.com/event/BN29/core-rule-set-for-the-masses) at AppSec USA on Friday, September 22.  
     From the abstract: "We will share our experience in fine-tuning the CRS for a large number of customers, adjusting to their taste in risk and attitude toward false positives. We will discuss lesser used features of ModSecurity to cut down noise levels in alerts, sometimes as much as 90%. We will also discuss our experience in moving from CRS 2.2.9 to 3.0 which was released in late 2016."  
    [![](/images/2017/09/DIsqT0-VAAANHVl.jpg)](https://appsecusa2017.sched.com/event/BN29/core-rule-set-for-the-masses)
- During the trainings at AppSec USA, the SpiderLabs team will run a one-day training with ModSecurity, focusing on the new libmodsecurity 3.0.0 release candidate.  
    <https://appsecusa2017.sched.com/event/B2VV>  
    From the abstract: "The training is tailored for web application defenders who are charged with protecting live web applications. It will cover significant updates, improvements and new features which have been added to this bleeding edge version of the open source libModSecurity (aka v3) WAF. We've created this training for anyone who's interested in sharpening their web security defensive skills to detect and stop web attacks as well as mastering the latest version ModSecurity."
- Walter / lifeforms is working on a CRS troubleshooting page for the new website. I have contributed with a list of frequently encountered issues and Walter promised to put up initial documentation which will then be expanded as we move along.
- The idea to run a poll to decide on 3.1 features got stuck on the question if a github / forms survey would work. We agreed that it does not and that Victor / squared, who volunteered to run this, will rather go with google forms or surveymonkey. You should see this poll in a few weeks.
- My "Introduction to CRS 3" talk is touring to Geneva, Switzerland, this month. I will speak at OWASP Geneva on Monday, September 11. Inscription:  
     <https://www.eventbrite.com/e/inscription-owasp-geneva-meeting-september-11th-2017-37606169064>
- The sales on the two Apache / ModSecurity / CRS courses in October are doing well. There are 3-4 seats free for London (October 4-5) and a single seat for Zurich (October 11-12).  
     <https://www.feistyduck.com/training/modsecurity-training-course>

{{< figure src="images/2017/08/christian-folini-2017-450x450.png" width="100px" caption="Christian Folini / [@ChrFolini](https://twitter.com/ChrFolini)" >}}
