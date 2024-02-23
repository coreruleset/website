---
author: Christian Folini
categories:
  - Blog
date: '2020-06-08T21:13:59+02:00'
permalink: /20200608/overhauling-the-crs-tags/
tags:
  - CAPEC
  - Tagging
title: Overhauling the CRS Tags
url: /2020/06/08/overhauling-the-crs-tags/
---


Tagging rules is a great feature of ModSecurity since it allows you to add information to your ModSec alert messages. In my tutorial on [Embedding ModSec over at netnea.com](https://www.netnea.com/cms/apache-tutorial-6_embedding-modsecurity/), I use the tag feature in the default action to add a tag to every alert message from a given service. I do this as follows:

```apacheconf
SecDefaultAction "phase:2,pass,log,tag:'Local Lab Service'"
```

One of my customers uses a shortcut URI as the tag. So when an alert pops up, the SoC person can click on the tag, the URI is being expanded (redirection service) and she ends up on a wiki page giving her all the infos about a given service with purpose, architecture, host IDs, security classification and contact information.

So yeah, you can make good use of the tagging feature and it's a bit of a pity, CRS is not using this properly or in a systematic way. This has bugged me for years, but now it's time to do something about it.

The problem we are facing for CRS tags is trifold:

- non-systematic use of tags (some stuff is tagged, some is not)
- inconsistent tag format
- outdated tags

How can tags be outdated? That's easy: We tagged some of the rules with the IDs of OWASP Top Ten security risks. Now given there is a new edition of the Top Ten guide every two years, we're several years behind and it's not so easy what the tag "OWASP\_TOP\_10/A6" really means. It actually means "A6 – Sensitive Data Exposure" based on the OWASP Top Ten 2013 edition.

Here is an overview over all the tags currently set in the rules together with their occurrence count:

```
245 application-multi
213 OWASP_CRS
203 platform-multi
201 language-multi
169 paranoia-level/1
 91 OWASP_TOP_10/A1
 71 PCI/6.5.2
 58 attack-protocol
 49 paranoia-level/2
 49 OWASP_CRS/WEB_ATTACK/SQL_INJECTION
 49 attack-sqli
 48 WASCTC/WASC-19
 48 OWASP_AppSensor/CIE1
 30 OWASP_CRS/WEB_ATTACK/XSS
 30 attack-xss
 29 attack-disclosure
 27 WASCTC/WASC-8
 27 WASCTC/WASC-22
 27 OWASP_AppSensor/IE1
 24 OWASP_TOP_10/A3
 24 CAPEC-242
 24 attack-rce
 23 WASCTC/WASC-31
 19 language-php
 18 paranoia-level/3
 16 OWASP_TOP_10/A7
 16 OWASP_CRS/WEB_ATTACK/PHP_INJECTION
 16 OWASP_CRS/LEAKAGE/ERRORS_SQL
 16 CWE-209
 16 attack-injection-php
 14 OWASP_CRS/WEB_ATTACK/COMMAND_INJECTION
 13 OWASP_TOP_10/A6
 13 language-shell
 12 PCI/6.5.10
 11 WASCTC/WASC-21
 11 WASCTC/WASC-13
 11 PCI/6.5.6
 11 OWASP_CRS/PROTOCOL_VIOLATION/EVASION
 11 language-java
 11 attack-reputation-ip
 10 platform-windows
  9 platform-unix
  9 OWASP_CRS/WEB_ATTACK/JAVA_INJECTION
  9 OWASP_CRS/PROTOCOL_VIOLATION/INVALID_HREQ
  8 attack-dos
  7 paranoia-level/4
  7 CAPEC-272
  6 PCI/12.1
  6 OWASP_CRS/POLICY/SIZE_LIMIT
  6 event-correlation
  5 platform-iis
  5 attack-generic
  4 WASCTC/WASC-15
  4 OWASP_CRS/WEB_ATTACK/RFI
  4 OWASP_CRS/WEB_ATTACK/HEADER_INJECTION
  4 attack-rfi
  4 attack-lfi
  3 WASCTC/WASC-37
  3 WASCTC/WASC-20
  3 platform-apache
  3 PCI/6.5.1
  3 OWASP_TOP_10/A2
  3 OWASP_CRS/WEB_ATTACK/SESSION_FIXATION
  3 OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_ACCEPT
  3 OWASP_CRS/PROTOCOL_VIOLATION/INVALID_REQ
  3 OWASP_CRS/AUTOMATION/SECURITY_SCANNER
  3 OWASP_AppSensor/EE2
  3 CAPEC-63
  3 CAPEC-61
  3 attack-reputation-scanner
  3 attack-fixation
  2 WASCTC/WASC-33
  2 PCI/6.5.4
  2 OWASP_TOP_10/A4
  2 OWASP_CRS/WEB_ATTACK/RESPONSE_SPLITTING
  2 OWASP_CRS/WEB_ATTACK/FILE_INJECTION
  2 OWASP_CRS/WEB_ATTACK/DIR_TRAVERSAL
  2 OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_HOST
  2 OWASP_CRS/POLICY/EXT_RESTRICTED
  2 OWASP_CRS/LEAKAGE/SOURCE_CODE_PHP
  2 OWASP_CRS/LEAKAGE/ERRORS_IIS
  2 CAPEC-460
  1 platform-tomcat
  1 platform-sybase
  1 platform-sqlite
  1 platform-pgsql
  1 platform-oracle
  1 platform-mysql
  1 platform-mssql
  1 platform-msaccess
  1 platform-maxdb
  1 platform-internet-explorer
  1 platform-interbase
  1 platform-ingres
  1 platform-informix
  1 platform-hsqldb
  1 platform-frontbase
  1 platform-firebird
  1 platform-emc
  1 platform-db2
  1 OWASP_CRS/WEB_ATTACK/REQUEST_SMUGGLING
  1 OWASP_CRS/WEB_ATTACK/NODEJS_INJECTION
  1 OWASP_CRS/WEB_ATTACK/HTTP_SPLITTING
  1 OWASP_CRS/WEB_ATTACK/HTTP_PARAMETER_POLLUTION
  1 OWASP_CRS/PROTOCOL_VIOLATION/MISSING_HEADER_UA
  1 OWASP_CRS/PROTOCOL_VIOLATION/IP_HOST
  1 OWASP_CRS/PROTOCOL_VIOLATION/EMPTY_HEADER_UA
  1 OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE_CHARSET
  1 OWASP_CRS/PROTOCOL_VIOLATION/CONTENT_TYPE
  1 OWASP_CRS/POLICY/PROTOCOL_NOT_ALLOWED
  1 OWASP_CRS/POLICY/METHOD_NOT_ALLOWED
  1 OWASP_CRS/POLICY/HEADER_RESTRICTED
  1 OWASP_CRS/POLICY/CONTENT_TYPE_NOT_ALLOWED
  1 OWASP_CRS/LEAKAGE/SOURCE_CODE_JAVA
  1 OWASP_CRS/LEAKAGE/SOURCE_CODE_CGI
  1 OWASP_CRS/LEAKAGE/INFO_DIRECTORY_LISTING
  1 OWASP_CRS/LEAKAGE/ERRORS_PHP
  1 OWASP_CRS/LEAKAGE/ERRORS_JAVA
  1 OWASP_CRS/AUTOMATION/SCRIPTING
  1 OWASP_CRS/AUTOMATION/CRAWLER
  1 OWASP_AppSensor/RE1
  1 language-powershell
  1 language-javascript
  1 language-aspnet
  1 IP_REPUTATION/MALICIOUS_CLIENT
  1 attack-reputation-scripting
  1 attack-reputation-crawler
  1 attack-injection-nodejs
  1 anomaly-evaluation
```

I guess you understand how this feels inconsistent to me. The WASC classification is really oudated, since the project died down many years ago. Top Ten is a moving target and thus not ideal. The CAPITAL letter tags we made up are not systematically applied and do not follow an accepted taxonomy. There is some value in the use of PCI tags I think and the lowercase tags used by our project actually bear some value on their own. But most of the rest should be replaced with something better, ideally with wider acceptance and following a real standard. This would be beneficial, since you could then do proper reporting based on the CRS tags and automatically end up with a document that could help other projects (Hint: OWASP Top Ten).

We looked around for quite a while and after discussing this multiple times, we settled on [CAPEC](https://capec.mitre.org/) as the best solution. CAPEC is a MITRE project and it expands to Common Attack Pattern Enumeration and Classification. MITRE is the organization behind the [CVE](https://cve.mitre.org/) numbering and CAPEC is one of their lesser known standards. The expansion of the name makes it immediately clear this is a perfect match for CRS. CRS attempts to detect attacks and this is an attack classification taxonomy.  
  
There is an [About page](https://capec.mitre.org/about/index.html) on the CAPEC website that is worth reading. I think it's very inspiring. It also does a good job to show why we are working with CAPEC and not with [MITRE ATT&amp;CK](https://attack.mitre.org/) that is becoming very popular: CAPEC is very close to the exploit, while ATT&amp;CK is often a level above. CAPEC is also more about application security, while ATT&amp;CK is more about network defense. There is actually [a website comparing the two](https://capec.mitre.org/about/attack_comparison.html).

What you are getting with CAPEC is a hierarchy of attacks organized in a tree. Let's check out one of our rules and see how it would map to the CAPEC tree.

We'll pick rule 920230 with the alert message "Multiple URL Encoding Detected".

The following CAPEC "Mechanisms of Attack" apply to this rule in hierarchical order:

255: Manipulate Data Structures  
153: Input Data Manipulation  
267: Leverage Alternate Encoding  
120: Double Encoding

I admit I am not happy with the seemingly erratic use of the ID name space, but the names are straight to the point. What should be noted is, that CAPEC provides two different trees. Or actually different trunks if you will. The branches and leaves of the tree are the same, but the tree named CAPEC "Domains of Attack" replaces the "255: Manipulate Data structures" with "513: Software". Below this initial entry, the trees look the same. We plan to link our rules to the "Mechanisms of Attack" tree.

How would we tags this? The discussions are not completely over yet, but this is the latest proposal for the tagging you would see in the alert message:

```
 … [tag "capec:513/153/267/120"] …
```

So the notation is very sparse (we need to save space), but it identifies as CAPEC and the hierarchy is described in the same way that URIs use slashes to lead you down a path (just do not think of the slash as an OR here).  
  
CAPEC is really well documented. Navigating the site, is a bit cumbersome, but the URIs all have the ID in the path. So we can get more information about these attack patterns at:

- <https://capec.mitre.org/data/definitions/513.html>
- <https://capec.mitre.org/data/definitions/153.html>
- <https://capec.mitre.org/data/definitions/267.html>
- <https://capec.mitre.org/data/definitions/120.html>

That's neat, is not it?  
  
We are working actively on this new tagging right now. In fact Fernando Outeda is doing the heavy lifting here with mapping all the rules to CAPEC. We hope to finish this in the next few days to be able to fit it into the 3.3 release, which is coming at the end of the month (we shifted our release schedule from Mid-June to the end of the month lately).

*Christian Folini, on behalf of the CRS team*
