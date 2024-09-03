---
author: amonachesi
categories:
  - Blog
date: '2024-09-03'
tags:
  - developer portrait
title: 'Meet the CRS team: Max, the Kiwi-German software developer from the Swiss Alps'
slug: 'meet-the-crs-team-max-the-kiwi-german-software-developer-from-the-swiss-alps'
---



#### *Max Leske is not a security expert, but nevertheless plays an important role in the CRS core team as a software developer. Max is perhaps the most global member of the team: after a brief detour to the other side of the globe, the Berlin native grew up in the Swiss mountains. In everything he does – and he does a lot – he attaches great importance to having fun. For him, the most important thing about the CRS project is the people.*

{{< figure src="images/2024/08/Max_Leske_1.jpg" caption="Whether it's work or sports – he just wants to enjoy what he's doing: Max Leske aka theseion" >}}

*After [Franziska “Fränzi” Bühler]({{< ref "blog/2023-01-17-meet-the-crs-team-franzi-the-puzzle-loving-hard-worker-with-a-mission.md" >}}), Max Leske is the second Swiss member of the CRS core team to be presented here with a developer profile. As with Fränzi, we met in the café of the Stauffacher bookshop in the Swiss capital Bern.*

“I'm not a computer security expert,” Max explains right at the start of the interview with a shy smile as he sips his coffee, “I just kind of slipped into it.” Max has a quiet character and is rather reserved; he doesn't push himself to the fore in groups. When it comes to team discussions, he calmly but concisely argues his point of view and is also willing to compromise. Max is a software developer by profession and knows computer security primarily from the user's perspective: “I have a certain amount of experience because I've had a few points of contact and ultimately a use case myself.” 

The fact that Max now strengthens the Swiss faction in the CRS team is thanks to a few coincidences and decisions that took him halfway around the world from an early age: born in Berlin in 1986 to German parents, he emigrated to New Zealand with them when he was just six months old. His parents separated there. Max was four years old when his new stepfather, a Swiss national, got a job in Davos, Switzerland. The whole family moved to the village in the Swiss Alps, where Max stayed until he started university. And so it was that the New Zealand "Berliner" grew up in the Swiss mountains. Max has since become a Swiss citizen. His family now includes a large number of German, New Zealand and Swiss half-siblings and step-siblings.

Max never had a dream job as a child, and certainly nothing to do with IT. Although he encountered the world of computers at an early age: when he was ten years old, his parents bought a PC with Windows 95. “They were at a loss with the device, but I was fascinated by it,” says Max. “Within a very short time, I was explaining to them how things worked and where their lost documents could be found.” Once, his Latin teacher gave him an old, non-functional computer. Max unscrewed it and moved jumpers around as he pleased until the screen displayed something again. “A little later the computer started to smoke and then it was dead.” Max actually tried to get serious about computer science and programming at age 13 and he bought a book on C development. “But I never really got into it because these abstract terms just didn't mean anything to me.” So, he didn't think about a career in computer science for a long time, but kept on tinkering with the devices in his home.

> "The CRS project benefits enormously when we combine diverse expertise in the team."

Still fascinated with computers when he finished school, Max began studying computer science at the University of Bern in 2007. The guidance he received from his lecturers helped him to quickly understand the subject matter. After just one year, he found his first student job as a Java programmer in a research group at the University of Bern's Institute of Geography. While Max was still working on his bachelor’s thesis, he received another job offer, this time from Netstyle, a Swiss provider of web application solutions. Max accepted and ended up staying there for ten years. During this time, he completed his master’s degree at the University of Bern, which he completed in 2016 with a thesis on debugging asynchronous processes. “This summary will have to suffice at this point,” Max warns with a laugh during the conversation on the café sofa, “otherwise it will get too detailed!”

It was at Netstyle that he first came into contact with CRS. Netstyle offered a self-developed web content management system as a service and had installed ModSecurity v2 with CRS on the server to protect customer instances. When the company decided to switch from Apache httpd to nginx and ModSecurity v3 in 2018, Max took responsibility of the migration. He discovered that the denial of service rules previously used to defend against aggressive bots were no longer working. Max dug deep into the topic and found a workaround, which he published on [GitHub](https://github.com/owasp-modsecurity/ModSecurity/issues/1987). During this time, he approached the CRS team with many questions – and made a positive impression. Eventually, Christian Folini asked him if he would like to become an official member of the core team. 

Max has now been working at Xovis AG, a specialist for people flow analysis, for almost five years. Originally employed as a Java programmer, he now works as a full-stack developer in Java, .Net, Go and Python. As his employer Xovis has no commitment to CRS, working on the rule set is a hobby for Max – albeit a time-consuming one. He spends perhaps five to six hours a week on it, and in intensive phases he can easily spend ten to twelve hours. He does this in his free time in the mornings and evenings, sitting at his computer at home. “I can concentrate well in my home office.” He shares his apartment in Bern with his long-term girlfriend. “We don't have any noisy children or annoying pets,” Max explains with a smile. 

{{< figure src="images/2024/08/Max_Leske_1.jpg" caption="If Max isn't working he likes to hang around ..." >}}

As a professional software developer, Max brings special expertise to the CRS project that few other members of the core team have to this extent. His favorite topics are automation and tooling, which are typical software development topics. He would very much welcome reinforcement of the CRS team, as there is plenty of work. “We have many exciting projects that are part of CRS: container images that need to be maintained; a toolchain for automation; go-ftw for testing; parsers for verification; automated CVE tests …” However, day-to-day business, i.e. fixing bugs and answering questions about the rules, takes up a lot of time, that is then not available for these projects. Support is, therefore, very welcome in all areas – and not just from security specialists, as Max emphasizes: “The CRS project benefits enormously when we combine diverse expertise in the team.”

He himself would like to drive forward the development of a universal rule language. Due to the limitations of the current rule format and the additional platforms and engines that need to be supported, the team keeps coming back to this. A universal language would offer various advantages, especially regarding automation. “I’m convinced that there is no way around the development of a universal rule language in the long term," says Max. “Of course, we could just carry on muddling along as before, and things would probably continue – more badly than well. But it wouldn't be fun.”

Max works a lot and also likes to take on responsibility – sometimes perhaps a little too much. But the key to everything he does is that he enjoys it. This also applies to his hobbies: he used to play club football until he was 15, when he decided that he did not enjoy the aggressive and physical play style in the league. Today, he prefers to meet up with his friends once a week for an informal game. He also goes bouldering twice a week with his girlfriend. In summer, he likes to climb outdoors or go on alpine tours.

> "I’m convinced that there is no way around the development of a universal rule language in the long term. Of course, we could just carry on muddling along as before. But it wouldn't be fun."

And if he still has the energy despite the intellectually demanding work at his job and for the CRS project, Max plays Dungeons & Dragons or reads fantasy novels. His latest read? “‘Shades of Grey’” by Jasper Fforde,” he replies, only to immediately emphasize: “That's not the same as ‘Fifty Shades of Grey!’” And how was the novel? “Great!” says Max – and starts talking.
The conversation on the sofa in the café of the Stauffacher bookshop in Bern then went on for quite a while. While it was an interesting conversation, Max's career, his work and CRS were no longer a topic. Thus, we stop the portrait here.

*However, if you’re interested in Max’s review of the mentioned novel, his D&D ventures, or, possibly, the CRS, you can find Max on Slack under the username* maxleske *and on GitHub under* [@theseion](https://github.com/theseion). *How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*


### Three more questions for the nerds …

**What is your favorite part of CRS? Why is that?**

The people in the project. The work is only fun as long as the people are fun, and also willing to challenge ideas. It's always a special pleasure to meet many of them at our annual developer retreat.

**What is your favorite rule and why?**

932204, the generic Unix remote execution command rule. At our developer retreat in Varese in 2022, Felipe and I spent a considerable amount of time figuring out a way around the limitations we were facing with the RCE rules. 932204 may not be perfect, but it was the key to enabling continued improvements to the Unix RCE rules.

**Can you share the f\*\*\*-up that happened on your ModSecurity setup?**

We use the crs-toolchain program to perform a couple of sanity checks in our CI pipeline, and until recently, we did not pin the version of crs-toolchain. That meant that, whenever we would publish an update to crs-toolchain, it would automatically be used in all new checks. Unfortunately, it also meant that any bugs that we had overlooked in any of the checks would hit all new and open PRs, and since crs-toolchain was in early development, there were many bugs. The team, myself included, wasn't very happy with situation, especially since for most of them it was never obvious what the cause was and they would lose a lot of time, trying to figure out what was going on. We now pin the versions of all tools we use in our CI pipeline, and only update to versions that we have verified to be good. It takes a bit of extra work to update the tool versions, but a stable CI pipeline is worth more.

*Text: Alessandro Monachesi, [science communications](https://science-communications.ch/en/)*

{{< related-pages "developer portrait" >}}


