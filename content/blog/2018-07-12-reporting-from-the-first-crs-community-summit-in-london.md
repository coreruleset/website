---
author: Christian Folini
categories:
  - Blog
date: '2018-07-12T14:10:35+02:00'
guid: https://coreruleset.org/?p=780
id: 780
permalink: /20180712/reporting-from-the-first-crs-community-summit-in-london/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: Reporting from the First CRS Community Summit in London
url: /2018/07/12/reporting-from-the-first-crs-community-summit-in-london/
---


This is a brief coverage of the [CRS Community Summit during](https://coreruleset.org/20180626/crs-community-summit-next-week-call-for-posters-and-the-program-is-ready/) AppSecEU in London last week.

Over 25 people followed our call for this first face to face meeting of the CRS developer team (6 of 10 developers with commit rights in the same room!) and the community. We have been very happy to have several end users, Trustwave representing the ModSecurity development, but also some of the big integrators in the room. There was AviNetworks, BitSensor, cPanel, Fastly, Kemp, Microsoft, NGINX, Verizon, etc. Finally also researchers and a representative from KISA, the Korean Internet Security Agency, and Ivan Ristić, original developer of ModSecurity for old times sake.

This was much more than what we had hoped for and this was only the beginning.

Chaim Sanders kicked it off with an overview over the upcoming [CRS 3.1 release](https://github.com/coreruleset/coreruleset/pull/1109) (RC in August!). New features include extensive coverage of Java serialization and injection attacks contributed by Manuel and Walter. We have community contributed rule exclusion packages for OwnCloud / NextCloud and DocuWiki. And we also refined the Paranoia Mode that lets you run higher Paranoia Level rules for integration purposes without affecting the scores. Federico lead a big rule cleanup and Chaim is making sure we pass all our unit tests, most of them created anew. Our build and testing process has been expanded with refined docker images; we closed many bypass holes and fixed broken rules. It's a major release.

Next up was Rodrigo Martinez from the University of Uruguay. He brought the news that Uruguay is embracing ModSecurity and CRS officially. He followed with a detailed coverage of his research into ModSec / CRS and machine learning. The two do not go together very easily, but he found to leverage lua to bring the two together. Very intriguing stuff.

Back in May, Mirko Dziadzka and Christian Treutler from AviNetworks had published the idea to [create a meta rule language](https://github.com/avinetworks/owasp-crs-technical-discussion/raw/master/documentation/OWASP_AppSec_EU_2018-Core_Ruleset.pdf). This language would be used to express CRS rules instead of ModSecurity code. This would make our project independent from a particular engine. Instead a translator script would process the meta language rules and export them into ModSecurity code. Alternative translators could aim at other WAFs. Or they could create native Java / Python / PHP code which could then be used to perform input validation. It's a bold proposal that would open the field far and wide for CRS. But it actually resonates with an idea by Ivan Ristić from ten years ago. The time was not ready back in the day, but Mirko and Christian were knocking on open doors. It looked as if the community was welcoming this initiative with open arms, constructive feedback and a frenzy discussion carrying that was hard to stop.

<figure aria-describedby="caption-attachment-788" class="wp-caption aligncenter" id="attachment_788" style="width: 1024px">[![](/images/2018/07/Group-Photo-1-small-1024x731.jpg)](/images/2018/07/Group-Photo-1-small.jpg)<figcaption class="wp-caption-text" id="caption-attachment-788">*Group Photo from the CRS Community Summit 2018 in London*</figcaption></figure>

Tin Zaw presented [WAFLZ](https://github.com/VerizonDigital/waflz), an alternative open source WAF developed by Verizon for use with their CDN. A full announcement of this project is pending, so it was more of a sneak preview for us in the audience. But a very interesting one. In fact, when talking about WAFLZ, we also touched on other implementations of the ModSecurity rule language. Robert Paprocki's Lua-Resty-WAF (used by others in the room) was mentioned and implementations by other CDNs.

So CRS will now work on a meta rules language and meanwhile alternatives for the ModSecurity engine are maturing. This brings more options for users and integrators.

Adrian Winckles told us the heartening story how is re-animating Ryan Barnett's [former](https://www.owasp.org/index.php/OWASP_WASC_Distributed_Web_Honeypots_Project) [OWASP Honeypot](https://www.owasp.org/index.php/OWASP_Honeypot_Project) [project](https://github.com/OWASP/Honeypot-Project), which has been abandoned. It's an exemplary story of system archaeology on behalf of Adrian and his partner Mark Graham. The system is slowly coming to life again and Adrian is now facing various integration problems. This includes transfer and consolidation of alerts that will ultimately feed into threat intelligence; their real research interest in this. Chaim mentioned that he thinks it's time to abandon older integration concepts and hook up on a Kafka messaging queue. And then couple this with a Kibana dashboard.

Outside of these full blown talks, we also did a poster session where Scott O'Neill presented CRS integration into cPanel. Ruben van Vreeland explained what BitSensor is doing with CRS. Additionally, Felipe Zipitría showcased the CRS DevOps integration developed by Franziska Bühler (who could not attend herself).

So this has been a most productive set of presentations. We are in touch with the presenters to see if there is interest to write a blog post about their work. That would really be worthwhile.

Outside of the presentations, we have been a very chatty crowd. The poster session got people to mix and talk among themselves and when we did the real breaks, everybody and something important to discuss. We could have went on forever, but we had to cut it down at a given moment and move to a restaurant nearby where cPanel sponsored a fantastic dinner.

I'll be back in a few days with a more detailed coverage of the decisions taken at the Summit and during a separate developer meeting. More good things are pending.

Other than that: We'll be back with another CRS Community Summit.

Best,

Christian Folini

P.S. We also did a group photo with the official OWASP event photographer. But it has not found our way so far. I'll update this post as soon as I have it.

\[Edit: Added group photo\]