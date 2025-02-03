---
author: amonachesi
categories:
  - Blog
date: '2023-11-28T07:00:00+01:00'
title: Discussions, excursions and hard work – CRS Developer Retreat 2023, days 2–7
slug: 'discussions-excursions-and-hard-work-crs-developer-retreat-2023-days-2-7'
---


After the lofty ideas of Sunday (keyword: [universe domination](https://coreruleset.org/20231105/universe-domination-plans-in-budapest-the-crs-developer-retreat-2023-day-1/)), things got a little more down-to-earth on Monday. After the participants had split up into the four projects, work began on them. Things got more exciting again in the afternoon when the next steps and the project roadmap were discussed.

Two results from the intensive discussion about the long-term development of the project should be mentioned here in particular: Firstly, in order to not being restricted by the SecRule language the project decided to slowly start preparing an alternative structured format for a rule language. Secondly, as a lesson from the delayed release of version 4 as a result of the bug bunty program, we agreed on a new and faster serial release – without getting rid of the LTS releases. There were many other points to discuss, which we will report on in due course when things are ready.

{{< figure src="images/2023/11/CRS_Budapest-1-3-scaled.jpeg" caption="During the guided tour through the Buda Castle district" >}}
On Tuesday, after the morning's project work, a trip to Budapest was finally on the agenda. We reached the historic center of the Hungarian capital by minibus, metro and bus (some were still expecting to fly on by helicopter). As a local, Ervin had organized a guided tour through the [castle district of Buda](https://budacastlebudapest.com/).

We walked past [Viktor Orbán](https://en.wikipedia.org/wiki/Viktor_Orb%C3%A1n)'s presidential residence (including soldiers marching at the changing of the guard) and 19^th^ century buildings (re)constructed in concrete in the 21^st^ century (a fact that was met with a frown from certain historians among us) to the castle courtyard. After a brief visit to the [Castle Museum and St Stephen's Hall](https://szentistvanterem.hu/en) – and an "impressive" coffee (according to the overwhelming opinion of the Italians in our group) in the museum’s café, we were definitely ready for dinner. We walked past [Matthias Church](https://matyas-templom.hu/home) to restaurant [Aranybásta](https://en.aranybastya.com/) – an excellent choice by Ervin.

#### The House of Terror, medieval times, and a pinball extravaganza

Our second excursion to Budapest, starting on Friday after lunch, took us first to the Heroes' Square in the city center, then down the Andrássy Boulevard along some embassies and consulates to the [House of Terror Museum](https://www.terrorhaza.hu/en) where we learnt a lot about Hungarian history from German to Soviet occupation. From a pedagogical standpoint, it was an especially well-crafted exhibition with many impressive exhibits and audio and video recordings from the 40s and 50s.

{{< figure src="images/2023/11/CRS_Budapest-5-1-scaled.jpeg" caption="The heroes on Budapest's Heroes' Square" >}}
After this rather dark and gloomy history lesson we needed a short break in the Ecocafe where we got served another great coffee – which elicited an astonished "[Mannaggia](https://en.wiktionary.org/wiki/mannaggia)!" from our Italian friends.

Having found new strength, it was time for another difficult historical challenge: dinner in the “medieval” restaurant [Sir Lancelot](https://sirlancelot.hu/)! While Christian was still looking desperately for something period-appropriate anywhere in the restaurant, we were served two enormous platters of meat, fish, potatoes, corn and cole slaw, and entertained by “medieval” performances from a belly dancer, a fire-juggler and two fighting swordsmen … it was hilarious! In the end, we filled four doggybags with the leftovers.

Last item on the evening’s agenda was a visit to the [Pinball Museum](https://flippermuzeum.hu/). This proved to be a wonderful trip down memory lane for some of us: dozens of pinball machines from the middle of the 20^th^ century up to current times could be played without entering money. And the museum closed only at midnight. Naturally, we came home late (at around 0:45 a.m.) – so late, that the gate to the hotel’s car park was already firmly closed. Some of us had to jump over the fence and get some unsuspecting cleaning woman in the hotel to open the gate for us. The end of another great trip to Budapest.

{{< figure src="images/2023/11/CRS_Budapest-7-1-scaled.jpeg" caption="A medieval feast for the Knights of the Core Rule Set" >}}
#### Project groups, quantitative testing and tautologies

However, the CRS developer retreat is not just discussions, excursions, and fun, most of the time it’s hard work. From Monday morning to Saturday evening, much work was done in the project groups.

For example, the group concerned with [platform specific testing](https://github.com/coreruleset/coreruleset/wiki/DevRetreat23ProjectPlatformSpecificTesting) was looking into bringing the ModSecurity v3 and nginx tests up to the same level as the ModSecurity v2 and Apache tests and doing the same with Coraza. Currently, our automated tests only target Apache httpd. We do have a setup for nginx, but we haven't used it in automation because many of the tests are failing. The group’s goal was to run our test suite against all of the “standard” backends (Apache httpd with ModSecurity v2, nginx with ModSecurity v3, Coraza), and documenting why tests fail on certain platforms. They also wanted to do this in such a way that third party integrators can specify expected failures for their own platforms when using our tests. By the end of the retreat, the group had documented all failing tests for ModSecurity v3 with nginx and Coraza. We are ready to start running tests against those two configurations in our CI pipeline and are now focusing on implementing the required changes in go-ftw.

Meanwhile, in regards to [quantitative testing](https://github.com/coreruleset/coreruleset/wiki/DevRetreat23ProjectQuantitativeTesting), CRS developer Andrew Howe wrote a script that tests payloads of natural language (i.e. English sentences) against CRS on PL2. This gives us testing results which will be used to improve the rules that generate the most false positives, making it easier to use CRS in the future. The first test runs, using a [corpus of English news headlines](https://wortschatz.uni-leipzig.de/en/download) provided by the University of Leipzig, delivered remarkable results. The script shows a list of the rules that generated false positives in descending order of their occurrence together with the natural language expression that triggered those rules. One of the most registered false positive, for example, was the expression “is not” – a combination of words that occurs often in natural language but gets identified as a threat by a tautology rule looking for inequalities. The same can be done with other languages. We still have to run the tests against v3.3.5 and v4 to get a complete overview.

{{< figure src="images/2023/11/CRS_Budapest-2-1-scaled.jpeg" caption="Most of the time, the CRS Developer Retreat means hard work" >}}
#### Azure, the status page and (no) cyclomatic complexity

The group that took care of the [status page](https://github.com/coreruleset/coreruleset/wiki/DevRetreat23ProjectStatusPage) had decided to focus completely on Azure as a test case. Other platforms could be added later. By Saturday evening, the group had implemented everything for the Azure test case.

To figure out what rules Azure supports, isolated tests (i.e., tests that trigger precisely one specific CRS rule at a time) had to be written. Otherwise, Azure may or may not block a payload without us knowing from the result which rule or mechanism was behind it. We already had defined that we want 80 % coverage with isolated tests. As there are 150 PL1 rules in CRSv4, this meant we needed to have 120 tests. So, we did 8 new tests, only against detection rules, to meet the quota. Equally, a lot of new tests on PL3 rules were written, bringing the total from 8 to 29. Now there is a nice stack of tests for PL1 to PL 4 rules, covering 80 % of the rules.

Meanwhile, others pulled together the metadata for Azure from their documentation (looking for answers to questions like do they support paranoia levels, do they support rule exclusion methods, etc.) and got the platform up and running. Azure’s WAF is called Application Gateway and uses CRS in versions [3.2, 3.1, 3.0, or 2.2.9](https://learn.microsoft.com/en-us/azure/web-application-firewall/ag/application-gateway-crs-rulegroups-rules). The Paranoia Level is set on 2 per default and can’t be changed. We ran a choice of isolated tests with go-ftw against the Azure WAF and generated a JSON file from the output together with the documented information. Currently, the JSON file generated is static. A new version that combines static information and live tests has still to be done.

As an MVP to display the (yet static) JSON files, we envisioned a [Hugo website](https://gohugo.io/) with a static page or set of pages. The final status page will probably feature three hierarchical views: a platform overview (Azure, Cloudflare, native Apache etc.), the individual platform, and the tests of the Platform. For the the MVP, we have included the list of tests in the view of the individual platform. The MVP is still a long way from publication, but it delivers a foundation for further discussions: What information is important? Just the tests? Does the page have to show PLs? And so on.

The fourth project for the developer retreat, with the aim of incorporating a [cyclomatic complexity](https://github.com/coreruleset/coreruleset/wiki/DevRetreat23ProjectCyclomaticComplexity) score into all rules, started on Monday. However, it came to an end quickly, when it was discovered that “cyclomatic complexity” was a fixed term used in computer science and that it was not possible to do this with ModSecurity unless implementing it diligently for SecLang. A different approach would be based on the new [performance framework](https://coreruleset.org/20230921/crs-performance-framework-a-gsoc-2023-project/).

#### Sauna, jacuzzi and the Great Dalmuti

All this hard work, of course, called for relaxation in the evening. There was a spa section in the hotel with pools and saunas which got heavily used by many participants of the retreat. Sometimes interesting new ideas and great plans were born there. Even though they tended to not always be practicable.

However, for some of us the day regularly ended in a nerve-wrecking social struggle: who will be the lowest of the low, and who will be the [Great Dalmuti](https://en.wikipedia.org/wiki/The_Great_Dalmuti)?

*PS: If you really have nothing planned and are bored, why not learn Hungarian? With its short words, few letters and simple word forms, you'll pick up the language practically in your sleep. E.g., here's a hearty: "[Egészségedre](https://en.wiktionary.org/wiki/egészségedre)"!*

*PPS: Our second Hungarian word of the week: “[Tilos](https://en.wiktionary.org/wiki/tilos#Hungarian)”. The Hungarians seem to love their “Tilos!” signs.*

{{< figure src="images/2023/11/CRS_Budapest-3-1.jpeg" caption="In the Metro to Budapest city center" >}}
