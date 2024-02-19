---
author: Walter Hop
date: '2017-06-08T18:27:47+02:00'
guid: https://coreruleset.org/?page_id=17
id: 17
site-content-layout:
  - default
site-sidebar-layout:
  - default
theme-transparent-header-meta:
  - default
title: FAQ
url: /faq
---


#### [What is the CRS?](#whatiscrs)

The OWASP ModSecurity Core Rule Set (CRS) is a set of firewall rules, which can be loaded into [ModSecurity](https://modsecurity.org/) or compatible web application firewalls. The CRS consists of various `.conf` files, each containing generic signatures for a common attack category, such as SQL Injection (SQLi), Cross Site Scripting (XSS), et cetera. It uses string matching, regular expression checks, and the libinjection SQLi/XSS parser.

#### [What is ModSecurity?](#whatismodsecurity)

[ModSecurity](https://modsecurity.org/) is an open source Web Application Firewall (WAF). It can be installed as a module inside the Apache, Nginx or IIS web servers.

#### [What is the difference between ModSecurity and CRS?](#modsecurityandcrs)

[ModSecurity](https://modsecurity.org/) is a *firewall engine* which can inspect traffic on your web server. It can log and block requests. However, an engine does nothing without a certain *policy*. The CRS delivers a policy where requests to your web applications are inspected for various attacks, and malicious traffic is blocked.

#### [For whom is the CRS intended?](#intended)

The CRS is aimed at web server administrators. You must run your own web server (Apache, Nginx, or IIS), be able to install web server modules (ModSecurity) and insert custom configuration into your web server (the CRS rule files).

#### [Is there a full tutorial on working with the CRS?](#tutorial)

Christian Folini has provided a comprehensive [Apache, ModSecurity and CRS tutorial](https://www.netnea.com/cms/apache-tutorials/). It details everything about installing and configuring a complete Apache, ModSecurity, and CRS setup. The tutorials on [installing ModSecurity](https://www.netnea.com/cms/apache-tutorial-6_embedding-modsecurity/), [configuring the CRS](https://www.netnea.com/cms/apache-tutorial-7_including-modsecurity-core-rules/) and [handling false positives](https://www.netnea.com/cms/apache-tutorial-8_handling-false-positives-modsecurity-core-rule-set/) provide in-depth information on these topics.

#### [What are benefits of using the CRS?](#benefits)

The CRS aims to protect your web applications by detecting a wide range of common attacks, such as SQL injections. Besides blocking, the audit log will also record attack attempts, allowing you to monitor when an application is under attack. Running the CRS on your own server ensures that you do not have to send your web traffic to a third party WAF provider. The CRS contains many generic attack patterns, which means that many newly discovered web application vulnerabilities are caught automatically without requiring frequent rule updates. Since you can control the configuration, you can adjust the strictness of the CRS to your liking and make fine-grained exceptions to the policy.

#### [What are drawbacks of using the CRS?](#drawbacks)

The CRS can be quite strict in detecting certain attacks. This means that sometimes a normal, bona fide, request may be blocked as a *false alert* or *false positive*, for instance, if it contains suspicious character sequences. We aim to minimize false positives as much as possible, but in some situations it may be necessary for you to write an *exclusion rule* which selectively disables some CRS checks. CRS is updated from time to time in order to address false positives and add new protections, which requires you to replace the files with a new release. Furthermore, the CRS adds some, usually minor, processing overhead to any request.

#### [Does the CRS protect against all vulnerabilities?](#protectall)

No, the CRS scans only for generic, commonly occurring, malicious patterns. Application-specific vulnerabilities, such as logic bugs or missing authorization checks, cannot be detected by generic firewall rules. The CRS is therefore not a replacement for patching web applications. To increase your protection against current web application vulnerabilities, you can combine the CRS with a commercial rule set such as the [Trustwave ModSecurity Rules](https://www.trustwave.com/Products/Application-Security/ModSecurity-Rules-and-Support/). Such a rule set contains specific virtual patches for many common web applications.

#### [What are paranoia levels, and which level should I choose?](#paranoialevel)

The Paranoia Level (PL) setting in `crs-setup.conf` allows you to choose the desired level of rule checks. You can adjust the Paranoia Level on a per-website basis, by copying rule 900000 from the `crs-setup.conf` file into the respective `<VirtualHost>` section of your webserver configuration (giving it a new rule id).

With each paranoia level increase, the CRS enables additional rules, giving you a higher level of security. However, higher paranoia levels also increase the possibility of blocking some legitimate traffic due to false alarms (also named false positives or FPs). If you use higher paranoia levels, it is likely that you will need to add some exclusion rules for certain applications that need to receive complex input patterns.

- **A paranoia level of 1 (PL1) is default.** In this level, most core rules are enabled. PL1 is advised for beginners, installations covering many different sites and applications, and for setups with standard security requirements. <span style="font-size: 16px;">At PL1 you should face FPs rarely, and therefore it is recommended for all sites and applications. If you encounter FPs, please [open an issue on the CRS GitHub site](https://github.com/coreruleset/coreruleset/issues/new). Don't forget to attach your complete Audit Log record containing the request with the issue. Be sure to scrub any personal data and sensitive information!</span>
- Paranoia level 2 (PL2) includes many extra rules, for instance enabling many regexp-based SQL and XSS injection protections, and adding extra keywords checked for code injections. PL2 includes some rules which were present by default in CRS 2.x, but excluded in the default level in CRS 3.x because of common false positive complaints. Nevertheless, these rules will add extra protection against advanced and obfuscated attacks which may evade the rules of PL1. <span style="font-size: 16px;">**PL2 is advised for moderate to experienced users who desire more complete coverage, and for all installations with elevated security requirements. PL2 may also be a good choice for existing CRS 2.x users**, as the level of FPs will be comparable to a CRS 2.x installation. PL2 may cause some FPs which you need to handle.</span>
- Paranoia level 3 (PL3) enables more rules and keyword lists that cover less common attacks. PL3 also tweaks limits on all special characters used, which provides high coverage against unknown attack types, obfuscated attacks and attempted WAF bypasses. <span style="font-size: 16px;">**PL3 is aimed at users who are experienced at the handling of FPs and at installations with high security requirements.** PL3 may regularly cause FPs which you need to handle.</span>
- Paranoia level 4 (PL4) further restricts special characters. **PL4 is advised for experienced users protecting installations with very high security requirements.** Running PL4 will likely produce a very high number of FPs which have to be treated before the site can go productive.

#### [I represent a project or web application, can the CRS add support for my application?](#project)

We are interested in improving support for popular web applications. Some types of applications, like content management systems, tend to produce false alerts in administration panels, as administrators submit complex HTML, CSS and JavaScript, which tends to trigger various rules in the CRS. We would like to minimize these by shipping default exclusion profiles for these applications, which can optionally be enabled by the user. [Create an issue on GitHub](https://github.com/coreruleset/coreruleset/issues) if you are interested in working with us to create and test such a profile.

#### [I'm interested in helping your project out, can I sponsor?](#sponsor)

Yes! As a project in order to support activities like summits, hackathons, and speaking at conferences we need sponsors. If you appreciate the work we do, or you use it heavily, you should consider sponsoring. If you are interested, please get in touch with CRS Co-Lead Christian Folini via christian.folini /at/ netnea.com. He is in charge of sponsoring contacts.

#### [What is the license of the CRS? Can I use CRS in my product?](#license)

The Core Rule Set is free software, distributed under [Apache Software License version 2](https://raw.githubusercontent.com/coreruleset/coreruleset/v3.0/master/LICENSE). You can use the CRS in your product, provided you adhere to the terms of the license.

#### [How do I resolve error "Expecting an action, got: ctl:requestBodyProcessor=URLENCODED"?](#urlencoded)

This error can happen when you are using ModSecurity 3.0.0 to 3.0.2. Support for the URLENCODED body processor was only added in ModSecurity 3.0.3. Please upgrade your ModSecurity to 3.0.3.

#### [How do I resolve error "Unknown variable: &amp;MULTIPART\_PART\_HEADERS"?](#multipart)

From CRS 3.2.2, 3.3.3 and up, **ModSecurity 2.9.6 or 3.0.8** (or versions with backported patches) are required due to the addition of new protections. We recommend upgrading your ModSecurity as soon as possible. If your ModSecurity is too old, your webserver will refuse to start with an *Unknown variable: &amp;MULTIPART\_PART\_HEADERS* error. If you are in trouble, you can temporarily delete file rules/REQUEST-922-MULTIPART-ATTACK.conf as a workaround and get your server up, however, you will be missing some protections. Therefore we recommend to upgrade ModSecurity before deploying a new CRS release.