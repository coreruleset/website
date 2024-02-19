---
adv-header-id-meta:
  - ''
ast-site-content-layout:
  - default
astra-migrate-meta-layouts:
  - set
author: Alessandro Monachesi
categories:
  - Blog
date: '2022-11-22T22:03:47+01:00'
footnotes:
  - ''
guid: https://coreruleset.org/?p=1932
id: 1932
permalink: /20221122/meet-the-crs-team-ervin-the-gardening-radio-amateur-in-the-background/
stick-header-meta:
  - ''
tags:
  - developer portrait
theme-transparent-header-meta:
  - ''
title: 'Meet the CRS team: Ervin, the gardening radio amateur in the background'
url: /2022/11/22/meet-the-crs-team-ervin-the-gardening-radio-amateur-in-the-background/
---


#### *Astronaut? Garbage truck driver? Electrical engineer? Metalsmith? In the end, Hungarian Ervin Hegedüs became a software developer. Within the Core Rule Set project, he contributes primarily to tool development and packaging. “New team members should above all be team players,” says Ervin.*

<figure class="wp-block-image size-large is-resized">![](/images/2022/11/airween_jump_1-857x1024.png)<figcaption class="wp-element-caption">*A man of many talents and names: Ervin Hegedüs aka AirWeen aka HA2OS*</figcaption></figure>Ervin Hegedüs has had no shortage of interesting career ideas in his 51-year life. While the usual childhood dreams of becoming an astronaut or a garbage truck driver vanished as he grew older, Ervin still today sometimes wonders what would have become of him if he hadn’t found his way to IT. He thinks he might have become an electrical engineer since he is a HAM radio operator in his spare time (callsign: HA2OS). More about that later.

Ervin's professional career eventually developed in a different direction. He studied at the Eötvös Loránd University (ELTE), a renowned natural science university in the Hungarian capital Budapest, where he graduated with a bachelor's degree in Computer Science. Today, he still lives in Budapest working as a systems and software engineer and developer at Digitalwave, a Hungarian digital marketing and advertising agency.

> “I learned a lot on the job.”

Ervin had his first contact with ModSecurity and the Core Rule Set in 2017, around the time of the ModSecurity v3 release. “A year later, I started getting serious about the software and CRS, and immediately a lot of questions popped up. A lot of things weren’t working properly,” Ervin recalls. So, he set out to fix them – although he’s no C++ expert, as he admits. “But I learned a lot on the job.”

Within two or three months, Ervin managed – with many workarounds – to get libmodsecurity3 and CRS up and running satisfactorily. Invaluable help came from the CRS project's Slack channel. “I bombarded the CRS team with questions about ModSecurity, and they were always helpful.” During these exchanges, Ervin eventually turned his attention to rulemaking. To that end, he developed a “pretty much working” (his words) parser, which he initially mentioned in passing in his contacts with the team.

The CRS team noticed Ervin’s talent and dedication. He was asked if he would like to demonstrate his parser to the team members present at an upcoming OWASP conference. When the core team eventually invited him to officially work as a developer on the Core Rule Set, Ervin didn’t hesitate: “I felt honored by the request. Moreover, I knew that I wanted to work with ModSecurity and CRS in the next few years. So, I accepted and joined the team.”

<figure class="wp-block-image size-full is-resized">![](/images/2022/11/Ervin_Antenna.jpeg)<figcaption class="wp-element-caption">*He has the high ground. After all, he calls himself AirWeen.*</figcaption></figure>Today, Ervin is an indispensable member of the CRS core team. In the Slack channel, he figures under “AirWeen” – a nickname he got from his friends when he did the triathlon: there were shoes called Nike Air Hurachi and Nike Air Pegasus ... so, why not Nike Air Ween? With his knowledge of the inner workings of the engines (mod\_security2 and libmodsecurity3) Ervin sees his role above all in providing important support in the background. Based on his parser, the CRS team has since developed a number of important utilities (e.g. regexp-assemble) and testing tools. “Tools that support the work of the ‘real’ CRS developers,” Ervin says with a wink. As a Debian maintainer, he also takes care of packaging for Debian and Ubuntu and brings this perspective to the work of the CRS team. This goes to show that all talents can be of use in the project. “Of course, a project like the Core Rule Set can always use web security analysts,” Ervin says. “But most importantly, you should be a team player.”

> "I knew that I wanted to work with ModSecurity and CRS in the next few years. So, I joined the team.”

How much time Ervin is able to work on the CRS project depends on his other tasks. “It’s been a while since I haven’t put at least a couple of hours a week into the Core Rule Set.” Fortunately, his employer supports him in his commitment. At Digitalwave, they’ve realized that Ervin’s expertise could certainly be used to add relevant services to their own portfolio.

Inevitably, Ervin also developed software for his favorite hobby, HAM radio. As a member of a local radio club, he participates in contests, preferably HF bands with Morse code at high speed. When a contest is coming up, he puts work, chores, and everything else aside to focus on preparation. In addition, Ervin is involved with his club’s radio station: building circuits, maintaining antennas and other equipment – and gardening. “I wouldn’t call it a hobby,” Ervin explains, “but I like working in the garden.” And that work goes way byond mowing lawns and trimming hedges: He’s already built two tree houses in the garden. “I love working with my hands and making things,” he explains with a shrug, finally adding, “If I hadn’t become an IT specialist, I think I'd like to be a metalsmith.”

Ervin Hegedüs is certainly not short of job ideas.

<div aria-hidden="true" class="wp-block-spacer" style="height:27px"></div>*How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*

<div aria-hidden="true" class="wp-block-spacer" style="height:27px"></div>### Three more questions for the nerds ...

**What is your favorite part of CRS. Why is that?**

If I have such a thing as a favorite at all, it’s the protocol enforcement. I don’t know why, maybe because those are always true.

**What is your favorite rule and why?**

I don’t think I have a favorite rule.

**Can you share the biggest f\*\*up that happened on your ModSecurity setup?**

I think it was a common mistake and I’m sure that everyone runs into this problem at some point: I had created a few exceptions (note: not “few” exceptions, but many exceptions) for several virtual hosts. I had to look at the host header because the exceptions were valid depending on it. So, I had to use chained rules, and to the first rule I added 'ctl:ruleRemoveById=...' and 'ctl:ruleEngine=Off' – that turned WAF off completely for many vhosts, and the WAF was running for weeks before I noticed. This happened years ago, and I don’t think I’ve done anything like that since. But, of course, this taught me a lesson.

*Text: Alessandro Monachesi, science communications*

<div aria-hidden="true" class="wp-block-spacer" style="height:27px"></div>#### Meet the CRS team:

- [Andrea, the musical man-in-the-middle](https://coreruleset.org/20221018/meet-the-crs-team-andrea-the-musical-man-in-the-middle/)
- [Fränzi, the puzzle-loving hard worker with a mission](https://coreruleset.org/20230117/meet-the-crs-team-franzi-the-puzzle-loving-hard-worker-with-a-mission/)
- [Andrew, the technical writer who loves Eurovision and Doom II](https://coreruleset.org/20231109/meet-the-crs-team-andrew-the-technical-writer-who-loves-eurovision-and-doom-ii/)