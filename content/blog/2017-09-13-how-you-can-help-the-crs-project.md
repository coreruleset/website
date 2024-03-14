---
author: dune73
categories:
  - Blog
date: '2017-09-13T20:35:50+02:00'
tags:
  - ProjectSupport
title: How You Can Help the CRS Project
url: /2017/09/13/how-you-can-help-the-crs-project/
---


When I looked into my inbox lately, I found a very kind message where a new user asked how he could support the project. He had listened to a [clip on the OWASP 24/7 podcast](https://soundcloud.com/owasp-podcast/less-than-10-minutes-series-core-rule-set-project), got really excited and was now installing CRS3.

I responded with a fairly lengthy message covering all the areas where I think his support would be welcome if not vital. On a second thought, there might be more people who are wondering how to join us, so why not publishing my response if it is of such a general nature.

Here you go:

*CRS used to be a one man show for many years. In early 2016, Chaim Sanders took over and invited Walter Hop and me to join the project. We released CRS3 in November 2016 and currently we have like 5-6 regular contributors with 2-3 additional ones doing some really good work as I write this.*

So the project is now really growing, we have momentum and we have big plans.

The idea is to make CRS the "1st Line of Defense" that is installed by default by ISPs. We're nowhere close, but the goal is clear and we think our code / rule set has that potential.

Where do you fit? First, let me be clear that you do not need to be an expert. Contributions can take many forms. The most simple thing is joining the conversation on [github](https://github.com/coreruleset/coreruleset) and adding your opinion to existing discussions. There is currently a [code cleanup project](https://github.com/coreruleset/coreruleset/issues?q=is%3Aissue+is%3Aopen+label%3A%22Rule+Cleanup+Project%22) under way. Adding your opinion the [rule format standard question](https://github.com/coreruleset/coreruleset/issues/808) can be a valuable contribution. If you are familiar with git or want to get your feet wet, then there are simple tasks in this code cleanup that take work off the back of those contributors who would rather concentrate on other issues.

Testing [pull requests](https://github.com/coreruleset/coreruleset/pulls) and proposed changes is very valuable too. It gives everybody reassurance that the code actually works. Installing proposed rules on your (prod) servers and reporting back with your observations: priceless.

If you want to dig deeper and you want to write rules and regular expressions, there are many [open feature requests](https://github.com/coreruleset/coreruleset/issues?q=is%3Aissue+is%3Aopen+label%3A%22v3.1.0-rc1+Candidate+Issue%22) and / or [false negatives](https://github.com/coreruleset/coreruleset/issues?q=is%3Aissue+is%3Aopen+label%3A%22False+Negative+-+Evasion%22) that could do with some love. The more people we are, the faster we can put these feature requests into real rules.

We recently started with [unit testing](https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released/). Many, many rules come without unit tests that proof their correct working. Filling this gap would be a huge benefit as it would speed up the development very much.

If you are running off-the-shelf standard web applications, then helping the project by providing a set of default rule exclusions to go with that software would be most welcome.

But contribution to the project is not limited to writing rules and surfing github. We have launched our new website in August and we welcome contributions. What we really need is success stories: We need normal system engineers and sysadmins telling their fellows how they got CRS3 working on their site and how they solved the problems they faced along the way. Every company is different and sharing your personal experiences will invariably help other people.

Our documentation is generally lacking, helping newbies on the [CRS mailinglist](https://lists.owasp.org/mailman/listinfo/owasp-modsecurity-core-rule-set) find their way around is time consuming, so support is most appreciated. Using your contacts to help make CRS more popular is something that will help us all. If you are on twitter, please write about your experience. Ideally with the hashtag [\#CRS3](https://twitter.com/hashtag/CRS3) and CC [@coreruleset](https://twitter.com/coreruleset). Make other system engineers use CRS, tell the world about it and our project will grow.

An important thing for our community is the [monthly project chat on IRC](https://coreruleset.org/20170907/crs-project-news-september-2017/). This is where we talk to each other and where we decide on our plans for the next week. If you could manage to join that session, that would be great.

So that is an overview where we could use some help. I am sure there will be something that fits your interest.

**\[EDIT\]: Very useful comment below from Walter Hop. In fact I thought the same thing when I read through several github comments on the weekend.**

{{< figure src="images/2017/08/christian-folini-2017-450x450.png" width="100px" caption="Christian Folini / [@ChrFolini](https://twitter.com/ChrFolini)" >}}
