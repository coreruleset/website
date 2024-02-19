---
author: Chaim Sanders
categories:
  - Blog
date: '2017-12-12T16:20:35+01:00'
guid: https://coreruleset.org/?p=613
id: 613
permalink: /20171212/crs-project-news-december-2017/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: CRS Project News December 2017
url: /2017/12/12/crs-project-news-december-2017/
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

- @dune73 will be attending [German Open Source Business Awards](http://award.osb-alliance.de). Chances look good that CRS will a top performer. More information can be found [here](http://award.osb-alliance.de/2017/12/01/unsere-osbar-kandidaten-teil-1/)
- Using t:lowercase versus (?i) performance and best practice. 
    - There is currently no definitive answer
    - A benchmark can be done using ModSecurity debug logs
    - @<span aria-controls="memberContextMenu" aria-haspopup="true" class="buffer bufferLink author c8 user hasUserParent link" role="button" title="spartantri (~spartantr@cio13-4-78-227-109-215.fbx.proxad.net)">spartantri will reach out to contacts to determine best approach for measuring and update us next meeting.</span>
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
- <div class="row messageRow sameAuthor chat type_buffer_msg userParent" data-bid="8485418" data-cid="358098" data-eid="1512423322605864" data-msgid="1512423322605864" data-name="lifeforms_" data-time="1512423324544.864" data-usermask="~walter@nagorno.karabakh.nl" id="e8485418_1512423322605864"><span class="message"><span class="content">PR #896 awaiting</span></span><span class="g"> </span><span class="message"><span class="content">fgs update on the PR we</span></span><span class="message"><span class="content"> think if the comments were taken into account it would be a quick and nice merge,</span></span><span class="g"> </span><span class="message"><span class="content">but for now it's stalled</span></span></div>
- Fizipi resolved the conflict <span class="message"><span class="content">896 </span></span>resolving the conflict on this one

The next community chats will be held on the following dates:

- January 8, 2018 20:30 CET **(Note: The change from our normal schedule)**
- February 5, 2018 20:30 CET
- March 5, 2018 20:30 CET

Some nice new blog posts have come out on coreruleset.org

- [Core Rule Set Project Won a German OSBAR Award!](https://coreruleset.org/wp-admin/post.php?post=604&action=edit)
- [How You Can Help the CRS Project](https://coreruleset.org/wp-admin/post.php?post=601&action=edit)
- [The Top 5 Ways CRS Can Help You Fight the OWASP Top 10](https://coreruleset.org/wp-admin/post.php?post=586&action=edit)
- [Disassembling SQLi Rules](https://coreruleset.org/wp-admin/post.php?post=563&action=edit)