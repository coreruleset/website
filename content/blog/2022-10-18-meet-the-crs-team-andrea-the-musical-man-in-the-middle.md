---
author: amonachesi
categories:
  - Blog
date: '2022-10-18T15:37:21+02:00'
permalink: /20221018/meet-the-crs-team-andrea-the-musical-man-in-the-middle/
tags:
  - developer portrait
title: 'Meet the CRS team: Andrea, the musical man-in-the-middle'
url: /2022/10/18/meet-the-crs-team-andrea-the-musical-man-in-the-middle/
---


#### *He likes to play board games and the guitar, and he loves to fix bypasses to CRS rules: Italian Andrea Menin joined the Core Rule Set team in 2018. The most important requirement for anybody joining the project, he says, is to enjoy it.*

{{< figure src="images/2022/10/02-2-1024x768.jpg" caption="Andrea Menin with the famous DeLorean: “*Back to the Future *sparked a love of technology and music in me“" >}}
He never wanted to be a locomotive engineer or an astronaut, but Andrea Menin (born in 1983) actually had an alternative to being a developer and IT crack: “After school, I either wanted to do something with computers or become a musician.” It had been the movie *Back to the Future* that sparked a love of technology and music in Andrea early on. “Back then, when I saw Marty play ‘Johnny B. Goode’ at the high school dance, I wanted to learn guitar, too.” Eventually, he studied both computer science at the Istituto Tecnico Industriale Statale (ITIS) and classical guitar at the Conservatorio A. Vivaldi in Alessandria, Italy, his birthplace.

Andrea still plays classical and electric guitar, but in recent years unfortunately much too rarely, as he says himself. Since the possibilities as a professional musician seemed limited to him, he decided to pursue a career in information technology. He got his first job as a security consultant with a company in Milan. He didn't get the tools for the job in college, though, Andrea points out: “We were a group of friends who were heavily into hacking and offensive techniques.”

> “Many WAF vendors can only sell their product because the CRS project exists.”

After many years in Milan, Andrea now works as a web application security business unit manager at [Sicuranext](https://sicuranext.com/), a managed defense services provider in Turin. Here he is responsible for the company's web application and API protection (WAAP) service. Since December 2021, he lives in the Piedmontese capital, just ten minutes from the city center. Andrea feels more comfortable in Turin than in the Lombard metropolis. “People here are not as stressed as in Milan, and it's easier to make new acquaintances.” When he's not working on web application security, Andrea enjoys jogging or playing board games and – of course – guitar.

Andrea has been an active member of the Core Rule Set team since 2018. Before that, he had started to develop his own web application firewall based on ModSecurity and Openresty for his former employer. For this, he sent several pull requests to GitHub with fixes for bypasses he found in CRS. This is how the CRS dev team became aware of the Italian developer, who usually appears on the Internet as “theMiddle”. TheMiddle? That's right: Andrea Menin theMiddle – man in the middle, get it? When they finally asked him to become part of the core team, did he hesitate? “Of course not!” replies Andrea, “I was totally excited. Many WAF vendors can only sell their product because the CRS project exists. We're not even twenty developers, but our project is used by companies like Microsoft, Cloudflare, and Google.”

{{< figure src="images/2022/10/01.jpg" caption="“Get in touch with us!” Even the Vulcan way." >}}

Andrea is convinced of the importance of the CRS: “The CRS is currently the most widely used and most complete rule set for WAF. Anyone who has tried to write a general ruleset against attacks such as cross-site scripting, SQL injection or remote code execution knows the difficulty – and how many bypass possibilities you have to keep in mind. Ivan Ristić once said, paraphrasing, ‘When you write a WAF rule, you create ten ways to bypass it.’” The OWASP CRS can count not only on the core team, but also on the support of an entire developer community.

Andrea also saw the invitation to join as a chance to expand his own expertise and learn from others on the team. Ultimately, this also benefits his employer. Sicuranext therefore supports Andrea in his engagement for the CRS and allows him to spend part of his working hours on the project. On average, he spends around five days a month working for CRS. When there are a lot of tasks to be done, such as recently for fixing the vulnerabilities found during a bug bounty program, it can be a few hours more. Andrea is particularly interested in rule bypass and input sanitization/validation, where he best can apply his offensive skills. Mostly he fixes bypasses on rules, or he develops rules that prevent bypasses.

> “The invitation to join the CRS core team was a chance to expand my expertise and learn from the others on the team.”

What message does Andrea have for people who would like to join CRS but don't know if they are talented enough to do so? “My message is quite simple: get in touch with us!” The only requirements for Andrea are a basic knowledge of the regular expression syntax and how the HTTP protocol works, as well as a bit of web security knowledge. The most important requirement, however, is to enjoy the project and contributing to it as well as learning new things. At the end of the day, Andrea says: “No matter what skill level, join us on our Slack channel and say hi. The CRS team welcomes every contributor and all opinions.”

{{ spacer }}

*How to get onto the project Slack? You can get an invitation from <https://owasp.org/slack/invite>, once registered head to our channel #coreruleset.*

### Three more questions for the nerds ...

**What is your favorite part of CRS? Why is that?**

My favourite part is the new plugins functionality. I've not contributed too much yet, but my plan is to create new plugins for most used CMS/applications.

**What is your favorite rule and why?**

Its rule 933180 (PHP Injection Attack: Variable Function Call Found, PL1), because my first contribution was preventing bypasses of this rule. Before fixing it, it was possible to bypass detecting RCE via some PHP tricky syntax.

**Can you share your biggest f\*\*up that happened on your ModSecurity setup?**

I never had big problems with ModSecurity plus CRS, but during the last 15 years I made a lot of big and stupid errors about system administration and security.

*Text: Alessandro Monachesi, science communications*

{{< related-pages "developer portrait" >}}
