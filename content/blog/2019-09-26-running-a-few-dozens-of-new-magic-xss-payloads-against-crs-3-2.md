---
author: Christian Folini
categories:
  - Blog
date: '2019-09-26T23:59:23+02:00'
permalink: /20190926/running-a-few-dozens-of-new-magic-xss-payloads-against-crs-3-2/
title: Running a few dozens of new magic XSS payloads against CRS 3.2
url: /2019/09/26/running-a-few-dozens-of-new-magic-xss-payloads-against-crs-3-2/
---


Earlier today, Gareth Heyes presented a very interesting talk with dozens of new XSS payloads at the OWASP GlobalAppSec conference in Amsterdam. The CRS developers in the audience immediately started to try out the payloads, but Gareth was so quick they lost track...  
  
But being the helpful person he is, he published the slides during the evening. Thank you.  
  
This allowed us to go to business.  
  
We extracted 73 payloads from the presentation, submitted them against a vanilla CRS installation with the new send-payload-pls.sh script, that comes with CRS 3.2 (released on Tuesday), and we found that there is indeed one new payload, that we are not catching in a CRS default installation:  
  
```javascript
{{toString().constructor.prototype.charAt=\[\].join; \[1,2\]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)}}
```
  
Nice one.  
  
But we are catching this at paranoia level 2 thanks to Franziska Bühler's new rule 941380 "AngularJS client side template injection".  
  
**All the other 72 payloads are caught in a default CRS installation at paranoia level 1.**

Here is the Gist with the full report and all the rules catching each payload.

{{< gist dune73 b5012ed09b97063abf3e80fd4d30c9f3 >}}

All in all it's over 2000 alerts.

Admittedly, this was done a bit in a hurry (we also had to attend the OWASP party...), so if there is any error with our conclusion, please get in touch.  
  
*Special thanks to Ervin Hegedüs for extracting the payloads from the presentation.*

**UPDATE**

Gareth has pointed me to the full [Portswigger XSS Cheatsheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet) that formed the source for many of the examples in his talk. So I have now extracted all those payloads (259 in my counting) and sent them against CRS 3.2 in all paranoia levels.  
  
**And here, we're not doing quite as good and we're only detecting 90% of the attacks in the default installation.** In fact we let 26 payloads pass, 4 of them even in paranoia level 2. None of the payloads passes in PL3.  
  
Those PL2 passes are a special form of UTF-7 BOM encoded payloads. A bypass problem we have been completely unaware of. We need a new rule for this.  
  
And the other 22 payloads that managed to sneak past CRS in the default installation are all AngularJS sandbox escapes. This is an area that we only just attacked with the new rule 934100 that has been added in 3.2. We had been planning to expand this new group of rules. And now we have a good source document to guide us.  
  
Here is the full report in a gist: {{< gist dune73 67400bf4d1e23848564ad73c679fcbe5 >}}.

Christian Folini, on behalf of the CRS team
