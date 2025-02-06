---
author: dune73
categories:
  - Blog
date: '2017-08-15T13:48:36+02:00'
title: CRS Project News August 2017
---


This is the CRS newsletter covering the period from July until today.

**What has happened during the last few weeks:**

We held our community chat last Monday. There were eight people including Manuel Spartan who participated on the development of the paranoia mode.
The big topic was disassembly of the optimized regular expressions that are very hard to read. See below for details.
The next community chats will be held on the following dates:
- Sep 4, 2017, 20:30 CEST (14:30 EST, 19:30 GMT)
- Oct 2, 2017, 20:30 CEST
- Nov 6, 2017, 20:30 CET
- Dec 4, 2017, 20:30 CET

    - The OWASP ModSecurity Core Rule Set 3.0.2 is still the latest stable version. We talked about an eventual 3.1 version in the chat, but we agreed that we are far from that and that we want to add a substantial set of new features to make transition worthwhile for users.
    - ModSecurity 2.9.2 came out on July 19. Among several bugfixes, it brings an updated libinjection support that helped CRS close a few holes. See this CRS issue for an example:
        [https://github.com/coreruleset/coreruleset/issues/797](https://github.com/coreruleset/coreruleset/issues/797)
        We recommend all users to update to 2.9.2. AFAICS there are no backported packages for the major distros yet, so this is only viable for those users who are doing their own compilation.
    - Summer holidays are taking their toll and we are quite behind with the inclusion of pull requests. This brings us to a very high number of 10 open pull requests. Most of them have been reviewed, but they have not yet been incorporated.
    - A PR that is still in preparation, but almost done is a big disassembly of over 2 dozens of the complex regular expressions that are so hard to read in the CRS. [Look at this beauty for example](https://github.com/coreruleset/coreruleset/blob/v3.0/master/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf#L589)
        The point is these rules are very old, they are machine generated with the help of an ancient perl module optimizing regular expressions for performance and the sources / original regular expressions are long gone. To add to the problem, some of the rules have been edited by hand afterwards so there is just no telling what they really do. It takes a rule archaeologist to reconstruct the original sources. Franziska Bühler took over this task and it seems she got to the bottom of all the complex SQLi regexes within a couple of weeks.
        The idea is now a PR to add the sources to util/regexp-assemble. This would then allow us to consolidate / optimize the regular expressions.
    - Believe it or not: We got the new logo for the project. As we kind of expected it took longer than expected, but it's done now and it sure looks cool. Expect a separate announcement very soon.
        This also holds true for the website which is ready and only waits for the logo for the real announcement.
    - OWASP London invited me to present my CRS3 intro presentation that I held in Belfast for AppSecEU. This took place on July 27 and according to the audience it was a big success. Here are a few photos taken after the presentation when I signed the new ModSecurity Handbook and then in the pub nearby:[![](/images/2017/08/crs_news_2017-08-photo-1.jpeg)](https://twitter.com/ChrFolini/status/892686195133739009)[![](/images/2017/08/crs_news_2017-08-photo-2.jpeg)](https://twitter.com/OWASPLondon/status/890693408683163648)

## Upcoming Stuff

- OWASP Switzerland is also hosting CRS introduction talk. This is happening on Wednesday, August 16 in Zurich at 6pm. [Here are the details](https://www.meetup.com/de-DE/OWASPSwitzerland/events/241771446/)
- There are still a few seats available for the Apache / ModSecurity / CRS courses in October. One in London, one in Zurich. https://www.feistyduck.com/training/modsecurity-training-course
- There is now a plan to run a real poll where CRS users can vote on feature requests. There are a ton of feature requests recorded on github, but we really are a bit at a loss on what people are really interested in. Stay tuned to learn more about this.

I have been on a holiday for two weeks, and it is likely I overlooked things on the mailinglists and on github. Feel free to speak up and respond to this message highlighting the omissions.
