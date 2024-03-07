---
author: amonachesi
categories:
  - Blog
date: '2023-01-17T18:54:57+01:00'
permalink: /20230117/meet-the-crs-team-franzi-the-puzzle-loving-hard-worker-with-a-mission/
tags:
  - developer portrait
title: 'Meet the CRS team: Fränzi, the puzzle-loving hard worker with a mission'
url: /2023/01/17/meet-the-crs-team-franzi-the-puzzle-loving-hard-worker-with-a-mission/
---


#### **Franziska Bühler* doesn't feel too comfortable in the limelight. The CISO of a Swiss mid-sized IT company rather likes to work through lists of hundreds of bypasses than being at the forefront. Talking to her, it gets clear quickly: Fränzi loves a challenge. “Once I set my mind to something, I follow through,” she says.*

{{< figure src="images/2023/01/Fraenzi_klein.jpg" caption="She was always fascinated by great heights: Franziska Bühler aka Fränzi on top of the Milan cathedral" >}}

“I don't really like to talk about myself,” Franziska says as she sits down and sips her coffee. We meet in the café of the Stauffacher bookstore in the old town of Bern, the Swiss capital, so that she can tell us something about herself and her motivation for working on the CRS project. It's a shame she doesn't like to talk about herself, because Franziska Bühler (called “Fränzi” by friends<sup>1</sup>) would have a lot to tell. For example, about her career from high school to an apprenticeship to CISO of an IT company – a position she practically created herself. Or about her passion for puzzles and brainteasers and what this has to do with her job. Or about the commitment with which she completes all her tasks. Or about how close she actually came to her former dream job (three guesses, and no, it's not princess).

Franziska has been CISO since 2021 at Bern-based IT solutions provider and software developer Puzzle ITC, a company with around 150 employees. When she joined the company in 2019, she was hired as a systems architect for middleware in the consulting organization; a CISO position did not exist at the time. However, in addition to her actual job, she soon took on more and more security tasks: She organized awareness trainings for employees and CTFs for developers, started a security championship program, set up an internal reporting office, and when security incidents occurred, she took the lead, blocked IPs and analyzed log files.

> “I love puzzles, riddles and detective work. I like to crack problems.”

Eventually, Franziska decided to convince management that Puzzle needed a security officer. “I went ‘all in’ and applied to be the CISO.” After that, she couldn't sleep for two nights at first. Had she been too brash, perhaps? “I was very nervous,” she now admits, “but once I set my mind to something, I follow through.” And indeed: Puzzle was convinced by Franziska's arguments and appointed her CISO and, a little later, gave her a security team.

Yet everything could have turned out differently. “Originally, I wanted to be an astronaut.” Not an uncommon wish among children – but it is remarkable how long it lasted with Franziska. To emulate her role model, Swiss astronaut [Claude Nicollier](https://en.wikipedia.org/wiki/Claude_Nicollier), she even signed up with the Swiss military as a teenager for pre-flight training. By day, she read all about astronaut spacecraft like the Saturn V rocket used in American Apollo lunar missions; by night, she explored the moon with her telescope and learned the names of lunar seas and craters. “When something really interests me,” Franziska says, “I can really dig into it.”

In the end, however, Franziska decided otherwise. After high school, she completed a two-year IT apprenticeship and then a computer science degree with a focus on security, which she completed in 2011 with a bachelor's thesis on forensics in the Android file system. In it, she showed how to recover deleted text messages, contacts and call logs. “That was a huge challenge. I kept staring at the hex dump, trying to glean something from it and find connections,” Franziska recounts. One day, a light suddenly dawned on her – and all of a sudden, she was able to recognize previously hidden patterns. “I saw the matrix, so to speak.”

{{< figure src="images/2023/01/DSC_1040_DxO_2.jpg" caption="On her way to black: Fränzi at her exam for the green belt" >}}
It's these experiences that Franziska loves about IT security: when, after much thought and trial and error, the penny finally drops. “I love puzzles, riddles and detective work. I like to crack problems.” Surely, she's an avid murder mystery reader then? Franziska shakes her head, “I rarely read mystery novels, I'd rather study or be productive.” But Franziska does know how to relax by reading – only she reads IT security literature instead of thrillers. “It's the best way for me to relax.”

This is exactly why Franziska came to the Core Rule Set – at least that's how the saga goes. She had met Christian Folini while working as a system administrator at Swiss Post. In 2009, she moved from systems operations to join him in security, where ModSecurity was deployed. “I don't remember it myself, but apparently at some point I said to Christian that I was often bored in the evenings.” So he encouraged her to join the CRS project.

She has not regretted her acceptance for a minute, as she affirms: “Working with people from all over the world who are so different and yet all brilliant in their own way is so fulfilling.” Over the years, Franziska has come to know and appreciate the members of the team. “We work together so much that they have become dear friends, even if we only meet in person once a year.” She receives paid work time from her employer for her commitment. At the end of the day, Puzzle benefits from Franziska's know-how, as the company also uses the CRS for itself and in solutions for its customers.

> “Working with people from all over the world who are so different and yet all brilliant in their own way is so fulfilling.”

And what skills does Franziska bring to the team? “Supporting people seeking help in the CRS chat is not my thing,” she answers. “Rather give me a list of a hundred bypasses that I can work through and for which I must find solutions. This is where my strength lies.” For example, Franziska managed to recover the original sources from highly optimized regular expressions so that they can [still be used today](https://coreruleset.org/20171109/disassembling-sqli-rules/). “In this work, I can fully live out my inclinations,” Franziska explains.

Last year, Franziska achieved certification as a Certified Information Systems Security Professional (CISSP). That was a hard piece of work. But Franziska wouldn't be Franziska if she sat back now. She started karate lessons in August 2021, and this December she took the exam for her third, the green belt. Her goal is, of course, a black belt. Exams also in her spare time, isn't that stressful? “That's just the way I am, I can't help it,” Franziska says with a mischievous smile.

Yes, that's how Fränzi is: All in!

*How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*

### Three more questions for the nerds ...

**What is your favorite part of CRS. Why is that?**

I think it’s the SQLi rules because I touched almost all of them when I was disassembling the optimized regular expressions in 2017.

**What is your favorite rule and why?**

I had to think about it a bit, but it's the HTTP Request Smuggling Rule 921110, which I modified in 2020. It was my first collaboration with a very friendly security researcher who got in touch via `security@coreruleset.org`. We then sent him a thank you and Swiss chocolate.

**Can you share the biggest f\*\*up that happened on your ModSecurity setup?**

When I added ModSecurity and the Core Rule Set to a web server without checking any other settings and configurations, it filled the file system, and the website was no longer available.

*<sup>1</sup> Pronounced quite like “frenzy”. The e gets a wee bit more emphasis and the z sounds like tz.*

*Text: Alessandro Monachesi, science communications*

{{< related-pages "developer portrait" >}}

