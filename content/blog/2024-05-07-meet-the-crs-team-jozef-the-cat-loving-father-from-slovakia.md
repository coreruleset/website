---
author: amonachesi
categories:
  - Blog
date: '2024-05-07T06:00:00+01:00'
tags:
  - developer portrait
title: 'Meet the CRS team: Jozef, the cat loving father from Slovakia'
slug: 'meet-the-crs-team-jozef-the-cat-loving-father-from-slovakia'
---


#### *Programming and entrepreneurship run in Jozef Sudolsky's family. When he's not working for his own web hosting company or for the CRS project, you can find him working out at the gym or in his large garden - or just playing with his daughter. His office is at the same time his daughter's playroom.*

{{< figure src="images/2024/Jozef_Sudolsky_1.jpeg" caption="His own company, his daughter, four cats, a house, a large garden, and the CRS project keep him busy: Jozef Sudolsky aka azurit" >}}

We met Jozef Sudolsky at the [November 2023 developer retreat](2023-11-05-universe-domination-plans-in-budapest-the-crs-developer-retreat-2023-day-1.md) in Budapest. It was the first time he met with the CRS core team in person. Jozef brought delicious Slovakian cheese and schnapps as a gift for the whole team. “I like cheese and schnapps,” he concedes. “But I like beer even more.” He once tried to brew his own beer but gave up after realizing it wasn't as easy as he probably thought. “It was drinkable, but too much work.”

Jozef was born in 1985 in the Slovak town of Banská Bystrica, then Czechoslovakia, the youngest of three children. If there is a gene for information technology, Jozef was obviously born with it. After all, he comes from a family of programmers: both his brother and sister studied computer science, and his father was a programmer. The fact that Jozef's mother was a math teacher instead of a computer scientist didn't hurt either.

Jozef began his career as a cybersecurity specialist while still in high school. He had chosen a high school curriculum focused on math and science. As a child, he’d had changing career dreams: At first, he dreamed of becoming a garbage collector (“I really liked those trucks!”), but sometime later, he changed his plans to become “some kind of archaeologist.” “I always loved digging in the ground and looking for things,” Jozef explains. About 10 years ago, he finally bought a metal detector – unfortunately, without much luck: “The most interesting things I found were a few shells from the Second World War.”

When he was 13, things changed: “When I joined Internet Relay Chat, there were a lot of hackers. I was amazed at what they knew and what they could do,” Jozef recalls. “So, I read everything that was available at the time about security and hacking and black hats.” Through the chat, he got in touch with some members of Slovak and Czech hacker groups, where he learned a lot, though he never actually joined a group. “I did some hacking then, but always in the white hat sense.” 

> "My office is half office and half my daughter's playroom. When we're playing and there's an urgency with a client, I'm at the computer in a few steps."

After high school, Jozef went to Comenius University in Bratislava, the Slovak capital, to study applied informatics, a general and very practical course that included programming. “I was fascinated by Linux and Python, but there were no such courses at the university,” he recalls. However, he had learnt already all he later needed before and outside of university. At that time, Jozef's father, a successful company founder himself, motivated his children to start their own businesses. Today, Jozef owns his own web hosting and server services company. The company has grown to a considerable size and now hosts around 10,000 domains. Jozef is still the only employee, but he is already hiring.

As a web hosting service provider, Jozef is in no doubt that web application firewalls and CRS play an important role in today's IT: “About two weeks ago, one of my customers was having some problems installing WordPress. It was late at night, and she decided to leave the installation incomplete and go to sleep,” Jozef says. When she woke up in the morning, someone had already finished the installation and connected it to a MySQL server somewhere on the other side of the planet. “This is what the Internet looks like today, it is a really dangerous place. I think in the very near future a WAF will be part of every web server, just like antivirus software is installed on every computer today.”

That’s why IT security has always been important to Jozef. About five or six years ago, he decided to implement a web application firewall to his offering. He started with ModSecurity and CRS. When he found a few bugs and false positives, he started creating issues on the project's GitHub. “The CRS team asked me if I could try to fix some of the issues I was reporting," Jozef recalls. “I tried – and after a few pull requests, they invited me to a CRS meeting.” Like many others, Jozef was hesitant at first: “I wasn't sure I could do it. It was my first time working on a project like CRS, and I had no experience with Github. But they believed in me more than I believed in myself. So, I joined.”

Where did he since leave his mark on the project? Jozef ponders for a moment before answering: “My biggest contribution, I guess, is the use of the Lua language and parts of the plug-in architecture.” He knew very little about Lua (an efficient, lightweight and embeddable scripting language) himself, but he found its goal of being as small as possible interesting. However, since the language was not suitable to be an integral part of the core rules, it had to be separated. This is how the new plug-in architecture of CRS v4 was born. “My contributions extend mainly to the exclusion rules plug-in and the current antivirus integration plug-in,” says Jozef.

{{< figure src="images/2024/Jozef_Sudolsky_2.jpeg" caption="Mens sana in corpore sano: Jozef goes to the gym 3-4 times a week" >}}

With CRS v4 being released, the team still has many ideas for the future development of the project, and new team members who bring additional skills are always welcome. There are talks about rewriting CRS in another language, like Yaml, to make it more universal. “If we do that, it would be great to have someone on board with some knowledge of those alternative languages”, Jozef argues.

After spending several hours a day on the CRS project for the first few years, he took a step back last year to deal with some personal issues. But now he's back, ready to step up again. Fortunately, he doesn't have to ask his boss for permission to work on CRS.

Jozef has been working completely from home since the pandemic. He still lives in Banská Bystrica, with a population of nearly 76,000 the sixth largest city in Slovakia, in a house with a large garden in a rural area near a forest. “I like gardening and I love animals,” he says. “At the moment I have four cats.” He also used to have a dog, but she died two years ago. While his garden provides him with plenty of activities, Jozef also goes to the gym 3-4 times a week. Physical exercise and gardening may be his way of providing a counterweight to his otherwise rather intellectual life: in addition to his company and the work for the CRS project, Jozef is also a member of Mensa, the worldwide network for gifted people. He finds it interesting that most of the people he meets there don't work in IT or similar fields. “It's nice to have something else to talk about from time to time.”

> "I think in the very near future a WAF will be part of every web server, just like antivirus software is installed on every computer today."

But more than work and hobbies, Jozef loves spending time with his daughter, who turned seven in January. Jozef and her mother are divorced and share custody of the girl. “My office is half office and half my daughter's playroom,” he laughs. “It's the perfect solution, because when we're playing and there's an urgency with a client, I'm at the computer in a few steps, ready to fix the problem. And then I can go back to playing.”

In the end, his daughter was also the reason Jozef couldn't stay the whole week at the developer retreat. Instead, he had to say goodbye on Monday. “I want to go home because it's my turn to take care of her,” he explained. Of course, he could have arranged to stay longer. But that's not Jozef's understanding of family. “I want to be with her,” he says. His family has always played a big role in his life – and it still means a lot to him.

*You can find Jozef on Slack under the username* azurit *. How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*


### Three more questions for the nerds …

**What is your favorite part of CRS? Why is that?**

Plug-ins, because it's a way to get all my crazy ideas into CRS.

**What is your favorite rule and why?**

I really liked rule 941310, because due to a bug it was triggered by all sorts of unicode characters not used in my country (like Russian azbuka). It acted as a very effective spam filter for website posts and comments. Unfortunately, this bug has been fixed in CRS 4.

**Can you share the biggest f\*\*up that happened on your ModSecurity setup?**

Our system is designed to block IP addresses from which a certain number of attacks are detected per minute. This block list is created and distributed in real-time to all servers in our infrastructure. The problem occurred on one of our customer's site, which included a chat with really high traffic. One of the users sent a pinned message to the chat, which was caught by CRS's data leakage rules, so these rules were triggered for every user of the chat who viewed the content of the chat. And it blocked their IP. This IP was distributed in a block list to all our servers. After a few hours, we noticed that the traffic to our infrastructure was suspiciously low. Fortunately, at the same time, we received a notification from the aforementioned customer that his site was experiencing almost no traffic for no reason.

*Text: Alessandro Monachesi, [science communications](https://science-communications.ch/en/)*

{{< related-pages "developer portrait" >}}
