---
author: amonachesi
categories:
  - Blog
date: '2023-11-09T18:03:48+01:00'
tags:
  - developer portrait
title: 'Meet the CRS team: Andrew, the technical writer who loves Eurovision and Doom II'
url: /2023/11/09/meet-the-crs-team-andrew-the-technical-writer-who-loves-eurovision-and-doom-ii/
---

#### *When invited to join the Core Rule Set project, Andrew Howe felt a bit intimidated by the highly talented team at first. Today he is a valued member of the CRS core team, bringing his experience as a technical writer and a CRS integrator. “Having people onboard with experience of running CRS at a large-scale would be very useful,” he says. What else he said, you can read in this interview.*

{{< figure src="images/2023/11/photo_portrait.jpg" caption="Full steam ahead: CRS core team member Andrew Howe lives in the same place where the Titanic started" >}}

*Hello, Andrew. Thanks for taking the time to answer some questions. Let’s start with: where do you live?*

I live in Southampton, a port city on the south coast of the UK. I’ve lived here for fifteen years. Southampton is probably best known as the departure port of the Titanic. The city remains busy to this day with some of the world’s largest cruise liners: when they set sail, I can hear their (often musical) horns from my home office.

*What did you want to become as a child? When did you realise you wanted to do something with computers?*

I had an interest in computers from a young age, but it wasn’t until I was an adult that I realised I could turn that into a job. As a child, I wanted to become either an ice cream man or a roller-coaster tester. During my school years I had a lot of musical interests and played the clarinet in every school band I could. As a teenager I developed a passion for compositing and visual effects. It’s a perfect blend of artistry, problem solving, and computing. It’s a fascinating discipline but it’s a very challenging industry to work in.

*What’s your educational background?*

I moved to Southampton to study physics but wasn’t able to finish for financial reasons. I didn’t enjoy the course at any rate and probably should have studied computer science instead. I ended up staying in Southampton and, through a friend, found a job at a homeless hostel and worked there for several years. It’s great to do socially useful work but those roles are badly underpaid and deserve much more recognition.

> "I’m fortunate to have a home office which is where you can find me working on CRS things. Usually with a cup of tea at hand."

*So, how did you end up in IT?*

During this period, I spent a lot of time tinkering with Linux boxes and attending free and open-source software conferences, notably FOSDEM in Brussels which I volunteered at for many years pre-pandemic. I ended up landing an IT job, providing tech support for petrol stations, and soon afterwards saw a Linux-based role advertised through my local Linux User Group, or LUG. That led to me working as a Linux engineer for Loadbalancer.org, a load balancer vendor, and then specialising in technical writing and WAF-related work. So, I have a non-traditional background in the world of software and IT.

*What do you do today, jobwise?*

Until recently, I worked as a “Technical Author/Architect” for Loadbalancer.org. One of my main responsibilities was technical writing, such as writing documentation and blog posts. I was also the resident WAF expert, providing WAF consultancy and training to customers when needed. Currently I’m looking for a new challenge.

*How and why did you join the Core Rule Set project?*

We used the Core Rule Set to power our load balancer’s WAF functionality at Loadbalancer.org, alongside the ModSecurity WAF engine. My previous department head encouraged me to learn ModSecurity: that was my entry into the world of WAFs. In 2021 I started a project to integrate CRS version 3 into our load balancer. That involved auditing the CRS code by asking myself “what impact would this line of code have on our customers?” I gained a much deeper understanding of CRS and discovered a small discrepancy in a tucked-away corner of the code. I reported the discrepancy to the CRS project, and it was confirmed as a fairly severe bypass vulnerability, which was quickly fixed. From that point on, I started attending the CRS meetings on Slack and was encouraged to help out by fixing easy issues on GitHub. After being involved for a while, I was invited to join the project as a developer and to attend the inaugural developer retreat meetup in Switzerland. That experience cemented my involvement with CRS, and I’ve been involved ever since.

*Did you hesitate to join?*

Yes! It’s intimidating to join a widely used project that’s developed by very talented people. But everyone is friendly and welcoming and there’s a lot of encouragement given to newcomers who show an interest in the project, which is great. I learned that everyone brings their own strengths to the project, and I realised that being involved was an opportunity to put my otherwise quite niche ModSecurity knowledge to good use. Plus, it’s great to be able to contribute to the world of free and open-source software.

{{< figure src="images/2023/11/photo_eurovision_2023.jpg" caption="The United Kingdom: 24 points. Le Royaume-Uni: 24 points ... The result did not dampen Andrew's joy of being live at the ESC Grand Final" >}}

*What is your role in the team?*

I landed into a bit of a technical writing role. I’ve helped to write and rework lots of the project’s published documentation, and we have a lot more writing work left to do. In addition, I bring the perspective of a CRS integrator to the table, as well as customers’ perspectives. I also bring ModSecurity v2 knowledge, which allows me to help write and review rule changes and troubleshoot problems that CRS users report to us.

*How much time do you invest in the project?*

I try to spend one day a week doing CRS-related things. My former employer was supportive of my contributions to the CRS project as we used CRS in our products. Employers definitely benefit from having strong CRS and WAF knowledge on-staff because security is an ever-growing factor for companies and their customers, especially load balancer and proxy vendors.

*Where and how do you usually work when working for the CRS?*

I’m fortunate to have a home office which is where you can find me working on CRS things. Usually with a cup of tea at hand.

> "Everyone in the CRS team is friendly and welcoming and there’s a lot of encouragement given to newcomers who show an interest in the project."

*Why do you think the CRS project is necessary?*

Security should be accessible to everybody, whether you’re a small community group or a huge company. The protocols that underpin the web, like HTTP, are free and open, so it makes sense for us to share our knowledge and experience on how to secure them. The Core Rule Set project does exactly that.

*What attributes and skills do people need who want to join the project?*

I think it’s very varied. Having an interest in CRS is the most important part. Being pragmatic is useful, as we need to strike a balance between security and ease of use. Creativity is invaluable when thinking about how we can use the tools in our toolbox to solve the problems we encounter. There’s lots of room for innovation and improvement. Knowledge of ModSecurity and Apache is helpful as that’s our reference platform. If you enjoy thinking about how HTTP, TCP and friends work then you’d fit in well. And if you like working with regular expressions then we definitely have a place for you.

*What skills are currently needed in the project?*

It would be great to have more people involved who run CRS in production, especially at scale. We know we have lots of work ahead of us to improve the raw performance of CRS, so having people onboard with experience of running CRS at a large scale would be very useful. Experience of running CRS in production also helps us improve our rules and reduce false positive rates to make life easier for everyone who uses CRS.

*What is your message to people who are interested but hesitant to join?*

Take a look at who we are and what we do as a project. If you have a genuine interest in CRS, then there’s sure to be a role for you. Get involved in the community: join our Slack channel, ask questions, and attend our twice-monthly meetings on Slack.

*If you’re not doing Cybersecurity, what do you do? Have you got any hobbies (beside CRS)?*

I play competitive Doom II (yes, the video game released in 1994!) and I’ve participated in some organised leagues over the past few years. That’s a lot of fun, and the Doom engine being open-source means that the community continues to evolve to this day through a variety of engine ports. Tabletop role-playing is awesome (I’m currently playing a human paladin) and I have an ever-growing collection of board games. I’ve also been a big Eurovision Song Contest fan since I was young, and I was lucky enough to attend the jury show of this year’s final when Eurovision came to the UK!

*How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*

{{< spacer >}}

### Three more questions for the nerds ...

**What is your favorite part of CRS? Why is that?**

I like the protocol rules in CRS. It's interesting when an application violates those rules in weird and wonderful ways: then you get to see the peculiar, non-standard things that an application is doing. It's like peeking under the hood of an application, inspecting its communications at the protocol level.

**What is your favorite rule and why?**

There's a pair of SSRF (server-side request forgery) rules that I really like: 934110 and 934120. They detect unusual formats and characters for representing IP addresses, because applications like web browsers will often accept strange, ridiculous-looking input. For example, input like:

http://⑯⑨。②⑤④。⑯⑨｡②⑤④

Those rules are fun.

**Can you share your biggest f\*\*up that happened on your ModSecurity setup?**

I used to maintain a custom rule set that made heavy use of ModSecurity's persistent storage mechanism. It did *not* perform well and was prone to strange errors; definitely the wrong tool for the job, but for various reasons I had to make it work. It was a bit of a nightmare to work with! I ended up porting the rule logic into the proxy layer (HAProxy) which was a much better choice for handling stateful session information, especially under load.

*Text: Alessandro Monachesi, science communications*

{{< related-pages "developer portrait" >}}

