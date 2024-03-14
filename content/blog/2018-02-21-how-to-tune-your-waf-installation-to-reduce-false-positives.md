---
author: csanders-git
categories:
  - Blog
date: '2018-02-21T06:00:52+01:00'
title: How to tune your WAF installation to reduce false positives [x-post]
url: /2018/02/21/how-to-tune-your-waf-installation-to-reduce-false-positives/
draft: true
---

Site administrators put in a web application firewall (WAF) to block malicious or dangerous web traffic, but at the risk of blocking some valid traffic as well. A false positive is an instance of your WAF blocking a valid request.

False positives are the natural enemy of every WAF installation. Each false positive means two bad things: your WAF is working too hard, consuming compute resources in order to do something it shouldn't, and legitimate traffic is not being allowed to go through. The damage from a WAF that generates too many false positives could be as bad as the damage from a successful attack—and can lead you to abandon the use of your WAF in frustration.

Tuning your WAF installation to reduce false positives is a tedious process. This article will help you reduce false positives on NGINX, leaving you with a clean installation that allows legitimate requests to pass and blocks attacks immediately.

Get O’Reilly’s weekly security newsletter[![](https://cdn.oreillystatic.com/oreilly/email/security-newsletter-20160315.png)](https://www.oreilly.com/content/how-to-tune-your-waf-installation-to-reduce-false-positives/)

ModSecurity, the WAF engine, is most often used in coordination with the OWASP ModSecurity Core Rule Set (CRS). This creates a first line of defense against web application attacks, such as those described by the [OWASP Top Ten project](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project).

The CRS is a rule set for scoring anomalies among incoming requests. It uses generic blacklisting techniques to detect attacks before they hit the application. The CRS also allows you to adjust the aggressiveness of the rule set, simply by changing its Paranoia Level in the configuration file, `crs-setup.conf`.
