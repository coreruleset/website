---
author: dune73
categories:
  - Blog
date: '2019-06-27T06:32:41+02:00'
title: 'Announcement: OWASP ModSecurity Core Rule Set Version 3.1.1'
---


The OWASP ModSecurity Core Rule Set team is pleased to announce the CRS release v3.1.1.

This is a minor release fixing a Regular Expression Denial of Service weakness (CVE-2019-11387) as well as some minor bugs and false positives.

The CVE is only affecting users of the libModSecurity 3 release line and only under special circumstances. However, we advise all users to upgrade to this latest stable CRS release.

We have been notified of 5 ReDoS problems in our rules in April. Upon closer inspection, only 1 of them proved real (the others were found in the naked regular expression, not taking payload transformation and protection mechanisms of the engine into consideration). Once this was established, we had to fix the regex without changing the detection capabilities of the affected rules. And this is what took us so long.

But here we are. This is replacement for 3.1.0 with almost identical behavior (minus the ReDoS and a few other fixes). As always with point releases, there are no new rules and an update should thus be smooth and should not bring any new false positives.

CRS 3.1 requires an Apache/IIS/NGINX web server with ModSecurity 2.8.0 or higher. CRS 3.1 will run on libModSecurity 3.0 on NGINX.

Our GitHub repository is the preferred way to download and update CRS:

```bash
$> wget https://github.com/coreruleset/coreruleset/archive/v3.1.1.tar.gz
```

For detailed installation instructions, see the INSTALL document.  
<https://github.com/coreruleset/coreruleset/blob/v3.1/dev/INSTALL>

Sincerely.

Chaim Sanders, Walter Hop and Christian Folini on behalf of the OWASP ModSecurity Core Rule Set development team
