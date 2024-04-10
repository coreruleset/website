---
author: dune73
categories:
  - Blog
date: '2017-10-03T07:25:59+02:00'
tags:
  - DINACon
title: CRS Project Nominated for Swiss DINACon Award
---

The Core Rule Set project (CRS for short) has been nominated for the Swiss [DINAcon Awards](https://dinacon.ch/en/dinacon-awards/). I do not think any of you understand what awards I am talking about, so let me explain.

It is hard to promote Open Source Software in Switzerland. This is not necessarily different from any other place, but let's say there are strong commercial players that effectively block market entry for many open source software projects around here ([Christian Folini](https://www.christian-folini.ch) / [@ChrFolini](https://twitter.com/ChrFolini) writing this).

This is especially true for reverse proxies / web application firewalls, where three commercial offerings have pretty much divided up the market, so the Core Rule Set has a hard time finding servers to be deployed on here in Switzerland.

But there is some change happening and this is thanks to organisations like [CH-Open](https://www.ch-open.ch/) that has been promoting the use of Open Source Software for years. CH-Open, [WilhelmTux](https://wilhelmtux.ch/), the [Research Center for Digital Sustainability](http://www.digitale-nachhaltigkeit.unibe.ch/index_eng.html) and other like-minded initiatives, as well as commercial companies with a very clear Open Source approach have all had an effect over the years and even if public use of Open Source Software is still limited, it is being discussed in public now: If you throw out public money without consideration of Open Source software, you have to [explain](https://www.parlament.ch/de/ratsbetrieb/suche-curia-vista/geschaeft?AffairId=20143532) [yourself](https://www.parlament.ch/centers/eparl/_layouts/15/DocIdRedir.aspx?ID=MAUWFQFXFMCR-2-39102) these days.

The Swiss Open Source Awards have played a key role in this development. For 2017, the Swiss Open Source awards have been re-branded as DINACon awards.

This is an abbreviation of "Digitale Nachhaltigkeit Conference", which can be translated as the conference on digital sustainability. This means, the Open Source idea has been opened up to a wider group of projects and initiatives that go behind pure software: open data, open access and sustainability of digital projects in general are now also covered.

{{< figure src="images/2017/10/dinacon-nomination.png" caption="The Nomination of the CRS Project">}}

But how does this apply to the [Core Rule Set](https://coreruleset.org) project?

The point is that the DINACon represents the same qualities that the OWASP ModSecurity Core Rule Set project covers: Quality, transparency and a sustainable code base that is maintained by a group of specialists passionate about the project and security in general. In our particular case, two of these specialists, Fränzi Bühler / [@bufrasch](https://twitter.com/bufrasch) and I happen to live in Switzerland and we hope to attract more Swiss developers into the project.

CRS has been a one-man show for many years. In early 2016, [Chaim Sanders](https://medium.com/@chaim_sanders) took over the project and invited [Walter Hop](https://lifeforms.nl/) and I to join him. Right now, we have 8 to 10 regular committers on the project and I feel that we have real momentum now. Following all the [discussions on Github](https://github.com/coreruleset/coreruleset) is seriously challenging and there are so many ideas floating around. It's true, the development of the project is very interesting.

This nomination comes at exactly the right moment and means an additional push for our project. It comes at a moment when we are actively working on the sustainability and the transparency of our rule base. Traditionally, the rules of the Core Rule Set have been very hard to read. Yet, new initiatives like the rules cleanup project are changing the situation and lately, Franziska Bühler has committed the [pull request](https://github.com/coreruleset/coreruleset/pull/907) that disassembles all the incomprehensible regular expressions and makes them reproducible and understandable. That work is key and if you have looked at the regular expressions that we leverage in the rule set, you understand why we are in awe of her work.

{{< figure src="images/2017/10/crs-pr-907.png" caption="The PR by Fränzi Bühler passes all the tests." >}}

As I said, it is a tough market in Switzerland for Open Source projects and especially when it comes to webserver security. The commercial products all have a very high TCO, either via high license costs or integration and support contracts. Yet the commercial players are all well established and Open Source alternatives like ModSecurity and the Core Rule Set have a hard time finding their way on webservers around here and probably worldwide. But we need to spread the word that there is a transparent and highly secure open source alternative to commercial black boxes. Smaller companies, public administrations and organisations on a tight budget need to know they can get the best tools on the market without spending big money: ModSecurity and the Core Rule Set are at their disposal serving as the 1st line of defense against web application attacks like those covered by the [OWASP Top 10](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project).

Awards like the DINACon can help us get this message across.

It's great to be nominated for DINACon and I really hope we can get this trophy!
