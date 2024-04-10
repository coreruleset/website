---
author: csanders-git
categories:
  - Blog
date: '2017-12-12T16:20:35+01:00'
title: CRS Project News December 2017
---


This is the CRS newsletter covering the period from Early November until today.

We held our monthly community chat. We had quite a few people stop by. Special thanks to lifeforms for leading the chat.

- - lifeforms
    - emphazer
    - franbuehler
    - spartantri
    - fzipi
    - hamlet\_

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/972). We had a short chat, during the chat we discussed the following:

- @dune73 will be attending [German Open Source Business Awards](https://award.osb-alliance.de). Chances look good that CRS will a top performer. More information can be found [here](https://osb-alliance.de/news/osbar-gewinner-2017-ausgezeichnet)
- Using t:lowercase versus (?i) performance and best practice. 
    - There is currently no definitive answer
    - A benchmark can be done using ModSecurity debug logs
    - @spartantri will reach out to contacts to determine best approach for measuring and update us next meeting.
- There are an excessive amount of open PRs and Issues 
    - All but three PRs have been assigned reviewers, we have to make a dent this month.
- The Java rules, that are a key feature of 3.1 need some attention 
    - The older versions are available here: https://github.com/coreruleset/coreruleset/blob/95e7e6b3982eca93989c7948faca4a961737eace/rules/REQUEST-944-APPLICATION-ATTACK-JAVA.conf
    - A new ticket will be opened taking into account discussions from https://github.com/coreruleset/coreruleset/pull/881/files
- Badging 
    - We may remove the gitter badge because we don't feel big enough for two chats and IRC is preferred (more discussion next chat)
    - We should investigate other functional badges using https://github.com/OWASP/github-template as an example.
- General question about determine if it is possible to determine if user is accessing via HOSTS file. 
    - It is not
- Travis and FTW PRs assigned to csanders
- \#957 rule split Move part to PL3 to prevent JSON false positives
- PR #896 awaiting fgs update on the PR we think if the comments were taken into account it would be a quick and nice merge, but for now it's stalled
- Fzipi resolved the conflict 896 resolving the conflict on this one

The next community chats will be held on the following dates:

- January 8, 2018 20:30 CET **(Note: The change from our normal schedule)**
- February 5, 2018 20:30 CET
- March 5, 2018 20:30 CET

Some nice new blog posts have come out on coreruleset.org

- [Core Rule Set Project Won a German OSBAR Award!]({{< ref "blog/2017-12-07-core-rule-set-project-winning-osbar-award.md" >}})
- [How You Can Help the CRS Project]({{< ref "blog/2017-09-13-how-you-can-help-the-crs-project.md" >}})
- [The Top 5 Ways CRS Can Help You Fight the OWASP Top 10]({{< ref "blog/2017-11-21-top-5-ways-crs-can-help-you-fight-owasp-top-10.md" >}})
- [Disassembling SQLi Rules]({{< ref "blog/2017-11-09-disassembling-sqli-rules.md" >}})
