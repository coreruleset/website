---
author: amonachesi
categories:
  - Blog
date: '2023-11-30T06:00:00+01:00'
tags:
  - developer portrait
title: 'Meet the CRS team: Felipe, the team player on the other side of the Atlantic'
slug: 'meet-the-crs-team-felipe-the-team-player-on-the-other-side-of-the-atlantic'
---


#### *As a South American, Felipe Zipitría has a special status in the CRS core team. The sociable Uruguayan played basketball which taught him all about the value of teamwork. Automation and standardization are key issues for Felipe in the CRS project. “The CRS project offers exciting problems that can make any techie happy”, he says.*

{{< figure src="images/2023/11/Felipe_Budapest-1.jpeg" caption="Our man in South America: Felipe Zipitría enjoys the views of Budpest at the CRS Developer Retreat 2023" >}}

If you enter [The Lab Coffee Roasters](https://thelab.com.uy/) in Uruguay's capital Montevideo on the Rio de la Plata, the river of silver, you might see a man with silver streaks in his hair and beard hunched over a laptop, his glasses on his nose, engrossed in programming, sipping a flat white. Felipe Zipitría is the name of the not quite 50-year-old who is here working on new features for the OWASP ModSecurity Core Rule Set. Since 2021, Felipe has been one of three co-leads of the CRS core team, along with Walter Hop and Christian Folini.

As an Uruguayan, Felipe has a certain special status in the CRS core team: he is the only team member from overseas and even the southern hemisphere; the other members all live in Europe (only recently a new member from India joined the team). For Felipe, however, the distance from the majority of the team on the other side of the Atlantic also has its good side: “Because most of the CRS team are in European time zones, I get time in my mornings to review pull requests and follow up on things from the CRS project before the U.S. West coast wakes up and I have to concentrate on my day-job.”

For the past two and a half years, Felipe has been a security engineer on the cloud engineering security team at Life360, a provider of family security solutions. Here, he handles cloud and application security. Because the California-based company welcomes and supports remote work by its employees, Felipe can do all the work from home. His employer also gives him a lot of freedom for his work on the CRS project. “Since working with them, I’ve been at two CRS developer summits,” he says. “Life360 was very supportive about attending the events, giving me time to focus on CRS.”

> "Team sports really teach you a lot about working together, you learn that you have a role to play in a bigger picture – and of course resilience, which can be very useful later in life."

Remote work at home, programming in the coffee house: Some might imagine this to be a loner. Far from it! Felipe is extremely sociable and feels comfortable among people. Anyone who has seen him live knows how entertaining Felipe is and that he is often at his best in a group. In fact, he sees himself as a team player. The value of good teamwork he learned playing team sports. “I played basketball for about 14 years. Team sports really teach you a lot about working together, you learn that you have a role to play in a bigger picture, and of course resilience, which can be very useful later in life.”

In fact, it wouldn’t have taken much for Felipe to become a professional basketball player. As a kid, he didn’t have a dream job – but he loved team sports! “I finally had to decide if I really wanted to play sports professionally or attending my night classes at university.” In fact, even before he graduated with a bachelor’s degree in computer science in 1999, Felipe had already been working at the Universidad de la República in Montevideo. As an assistant, he taught courses on operating systems, computer networks and, eventually, the foundations of information security.

Felipe also spent the first twenty years of his professional career after finishing his studies at the university: as a member of the system administration group in the Computer Science Department, he took care of everything from simple PC configuration to huge servers and cluster infrastructures. “Fun times!” recalls Felipe. During those years, he learned a lot about approaching complex problems. Over time, he also took responsibility for the operation and planning of all critical systems – and for leading project teams and motivating them. During this time, in 2006, Felipe earned his master’s degree with a dissertation entitled “Towards Secure Distributed Computations.” Today, he still works as a lecturer, teaching Computer Security Fundamentals to pre-graduates and Application Security to postgraduates.

> "Contributing is a way to give back to the community – and this gives you a nice feeling of accomplishment."

In his capacity as a systems administrator at the university, Felipe came into contact with the CRS project. “We were using ModSecurity as a web application firewall, but soon realized that there was no systematic way to write rules. So, we turned to the Core Rule Set.” But Felipe's team didn't really find what they were looking for there either at the time. “That's when I contacted the project, created a pull request with a proposal for a standard, and also rewrote existing rules accordingly.”

Such dedication did not go unnoticed by the CRS project, and soon Felipe received an invitation to become a regular member of the team. He didn’t hesitate for a moment. “From then on, I contributed to the project more often,” he recalls. “It was a way to give back to the community – and this gives you a nice feeling of accomplishment.”

Now made co-lead, Felipe sees his role on the team primarily as an enabler: automation and standardization have been key issues for him since the beginning, especially for such a small team. “But my favorite thing is to think about tools that make it easier to use and contribute to CRS and to ease the maintenance toll.” To be sure, Felipe can’t say exactly how many hours he puts into working on the project. But especially during more intensive phases, such as the current big push toward version 4, he can easily add up to between 30 and 50 hours a month.

{{< figure src="images/2023/11/Felipe_Pool.jpeg" caption="Felipe tries to go swimming every day" >}}

Felipe would like to see reinforcements for the project team, as the scope of the CRS project has grown enormously. Today, CRS provides an umbrella for numerous subprojects that revolve around the actual core rule set – from container building to testing and performance monitoring to development. “There's something for everyone,” Felipe says and adds jokingly: “In fact, we offer really exciting and very application-oriented problems that can make any techie happy.” For example, he says, anyone interested in contributing can simply create their own issue or even just join the discussion in the Slack channel. “There's plenty for you to do, so get in touch!”

However, his employer is not the only one who allows him a lot of freedom; after all, Felipe is a family man. When he is not working for his employer or the CRS project, he likes to read a good book – preferably crime novels, but also science fiction – or go for a walk. He tries to go swimming every day, even if he doesn't always succeed. “And I used to brew my own beer,” Felipe adds. “Unfortunately, nowadays I don't get to do it as often as I would actually like.”

*How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*

### Three more questions for the nerds ...

**What is your favorite part of CRS. Why is that?**

I would say the SSRF detection rules. It was a debt we had since some time, and it is a difficult topic to solve properly. We provide only partial protection, because of DNS Rebinding attacks, but we have added rules in PL1 for automated cases and PL2 covers additional specific attacks.

**What is your favorite rule and why?**

We spent a lot of time with the rules 942130 and 942131 when removing the original PCRE only 942130 rule. And I ended up liking a lot the solution we found for removing the back references in the original rule.

**Can you share the biggest f\*\*up that happened on your ModSecurity setup?**

Of course: writing a rule that you think is going to allow one specific use case but logically allowing all traffic. That’s when you start asking yourself: “Why am I not seeing any blocked attacks now?”

*Text: Alessandro Monachesi, science communications*

{{< related-pages "developer portrait" >}}
