---
author: dune73
date: '2017-11-21T16:36:31+01:00'
tags:
  - Cross-Site-Scripting
  - Logging
  - ModSecurity
  - Monitoring
  - OWASPTop10
  - SQLInjection
title: The Top 5 Ways CRS Can Help You Fight the OWASP Top 10
---


The new edition [OWASP Top Ten](https://github.com/OWASP/Top10/raw/master/2017/OWASP%20Top%2010-2017%20%28en%29.pdf) list mentions [ModSecurity](https://www.modsecurity.org) and the [OWASP ModSecurity Core Rule Set](https://coreruleset.org) for the first time.

Let me explain you what the Core Rule Set does and how it can help you protect your services from these risks.

The CRS - short for OWASP ModSecurity Core Rule Set - is a set of generic attack detection rules. They are meant for use with ModSecurity or compatible web application firewalls. The CRS aims to protect web applications from a wide range of attacks with a minimum of false alerts. The Core Rule Set is thus meant as a 1st line of defense against web application attacks as described by the OWASP Top Ten.

But let me be straight here: CRS is no silver bullet that allows you to forget about security altogether. We mean you to use it in front of your secure application as an additional layer of security. And then, when your application has a bug (as it will invariably happen some day), an attacker will have more problems detecting and exploiting it. So CRS buys you time and good sleep. But it does not guarantee you protection from very smart adversaries.

First, let's look at monitoring!

## A10 : Insufficient Logging and Monitoring

This is where OWASP Top Ten mentions CRS under "Prevention". The deal with this risk is you are under fire, but you do not even notice because you fail to detect the attackers. I think it is safe to say that application logs are generally underdeveloped. Namely security events either go undetected, or they are buried under non-relevant events. What A10 really ask is a consistent visibility into security events and a systematic monitoring of these alerts.

Top Ten mentions a vulnerability scan by OWASP Zap as a typical example during the reconnaissance phase of an attack.  
Here is a list of CRS alerts that went off during a scan by OWASP Zap:

```
713970 942100 SQL Injection Attack Detected via libinjection
157788 930110 Path Traversal Attack (/../)
 96038 930100 Path Traversal Attack (/../)
 72433 930120 OS File Access Attempt
 61424 942190 Detects MSSQL code execution and information gathering attempts
 59558 920420 Request content type is not allowed by policy
 51879 932115 Remote Command Execution: Windows Command Injection
 38355 932105 Remote Command Execution: Unix Command Injection
 37891 932160 Remote Command Execution: Unix Shell Code Found
 24882 932100 Remote Command Execution: Unix Command Injection
 13584 921120 HTTP Response Splitting Attack
 13572 921160 HTTP Header Injection Attack via payload (CR/LF and header-name detected)
 12312 920440 URL file extension is restricted by policy
 11310 933160 PHP Injection Attack: High-Risk PHP Function Call Found
 ....
```

This list is based on a default installation of CRS. Since the release of CRS v3.0 in November 2016, we received about 20 issues related to false positives in the default installation. This is little given the very big user base of the rule set.

The alerts are systematic and they cover most attacks web applications face. A CRS default installation therefore gives you high visibility into the security events on your web application. Also if we let CRS run in pure monitoring mode, there is no risk of blocking legitimate traffic no matter how low the fale positive rate is.

## A1 : Injection

This category consists of a variety of ways to inject code into a service. SQL Injection is classical, but you can also inject OS commands, PHP code, you name it.

In the list of alerts seen above, the SQL Injection attacks are prevalent. This has to do with the parameterization of the OWASP Zap scanner. But it also shows the superb capabilities of CRS to detect SQL, system command and PHP Injections.

OWASP Top Ten tells you that CRS can detect attacks as seen above under A10. But it does not tell you, that CRS can also stop many of the attacks for you.

{{< figure src="images/2017/11/tmp.png" caption="Burp vs. CRS" >}}

Here is a graphic that depicts a scan as carried out by the Burp vulnerability scanner. In our example, Burp probed a special vulnerable application. In the first column, you see Burp's report when no protection shielded the application. In the 2nd column, you see a CRS default installation used as a 1st line of defense in front of the vulnerable service. Unlike under A10, we are immediately blocking the probes here. Again, false positives are very rare in the default installation and they can be handled with relative ease thanks to existing guides.

It's not like the application was immune to the injection attacks, but CRS mitigated SQL Injections as far as Burp is concerned.

## A7 : Cross-Site Scripting (XSS)

Cross-Site Scripting occurs when a user is able to send javascript commands to the server, that are then reflected back to other users. As you can see in the graphic above, CRS is pretty good at detecting this in the default installation. It stopped like 80% of Burp's attempts with the default CRS installation.

We can go higher by raising the awareness level of the rule set. Within CRS, we call this Paranoia Level. The default level is 1 and the max is 4. The default means little hassle and a decent baseline security level: That's CRS for everyone. As soon as you have sensitive data, you should go with Paranoia Level 2. Online banking should be a 3 and everything beyond that should have a 4. As a rule of thumb.

The correct choice of a correct Paranoia Level setting is thus a decision you need to to make your self. You need to base it on your threat model, your assets and the available resources. CRS is one tool within a multilayered security setup.

## A9 : Using Components with Known Vulnerabilities

Wall all now, Equifax should have patched their servers. The Swiss Military should have patched their servers too. But then they did not and the attackers exploited them. Equifax was stupid enough to blame it on an individual administrator failing to do his job. Apparently, when you have a single point of failure as this, then you need to look into your complete setup. An individual sysadmin tasked with patching should not be a single point of failure. And the obvious failure here is the lack of resources and an additional safety net. Sometimes, server are not patched in time. So you better put a 1st line of defense in front in order to reduce the risk.

CRS is such a 1st layer of defense. And it is particularly good at preventing the PHP exploits that plague the best known Content Management Systems.

We also would have caught the Equifax hack. But truth be told, not in the default installation. It would have taken a higher Paranoia Level. We have identified this weakness in our rule set and launched a project to cover this gap. CRS 3.1 will come out with a much improved detection mechanism for Java exploits.

## A3 : Sensitive Data Exposure

CRS can not solve this problem for you. But it can reduce the risk for a nasty subcategory. We call this Local File Inclusions. That is files exposed on a server and an attacker being able to retrieve them. We are very good at detecting attackers requesting OS system files and we won't let them have them.

Admittedly, A9 goes far beyond Local File Inclusion. But these files are extremely valuable in the reconnaissance phase of an attack. Failing to protect them is a huge problem. So this a significant reduction of the A9 attack surface.

## Where to go from here?

You should take CRS for a spin. The [default installation](https://coreruleset.org/docs/deployment/install/) only takes a couple of minutes. You can also use a ready-made [docker image](https://github.com/coreruleset/modsecurity-crs-docker). And if you do all this in your lab or on a dev server, you can get a first feeling of CRS without risking anything.

There are a couple of [video presentations](https://www.youtube.com/watch?v=eO9gBAmKS58&feature=youtu.be) on our website that give an overview. And I also wrote a length introduction to CRS over at Linux Weekly News.

There is a [series of tutorials](https://www.netnea.com/cms/apache-tutorials/) that explain the use of the rule set in detail. Likewise, I teach [ModSecurity / Core Rule Set courses](https://www.feistyduck.com/training/modsecurity-training-course) several times a year. The next ones probably in February 2018, but I also do in-house courses [on request](mailto:folini@netnea.com).

Finally, let me tell you a about a little known feature: If you are afraid ModSecurity or CRS could blow up your existing service, there is a neat little option that you can enable in the `crs-setup.conf`. It's called the sampling size. It allows you to enable CRS only for let's say 1% of the requests on your service. That way you get minimal impact from potential problems, but enough alerts to get used to it. As you grow more confident you raise the sampling size step by step until you hit one hundred again. That is really useful.

Thanks for reading. If you are interested in CRS, I suggest you follow the project on twitter at [@coreruleset](https://twitter.com/coreruleset) or you come here more often for future blog posts.

