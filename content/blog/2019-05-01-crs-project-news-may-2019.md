---
author: dune73
categories:
  - Blog
date: '2019-05-01T12:34:59+02:00'
tags:
  - CRS-News
  - DoS
  - ReDoS
title: CRS Project News May 2019
---


We are back with the CRS project news. There was not too much to talk about in recent weeks, but now there is real content. So here we go.

### **What has happened in recent weeks**

- Security researcher Somdev Sangwan has looked into Regular Expression Denial of Service attacks. It is a more or less well known fact, that CRS suffers from this
    problem. Usually, it is no big deal as ModSecurity 2 used to protect from
    this type of attack. However, this protection is gone with ModSecurity 3.
    Somdev Sangwan had 5 (!) CVE against CRS created. Yet we came to the
    conclusion, that only one of them (👉 CVE-2019-11387) is directly
    exploitable and only on ModSecurity 3 at paranoia level 2 or higher. The problem is situation in two separate rules. We are now working on a solution for this issue.
    Links:
    <https://nvd.nist.gov/vuln/detail/CVE-2019-11387>
    <https://github.com/coreruleset/coreruleset/issues/1359>
    <https://portswigger.net/daily-swig/unpatched-modsecurity-crs-vulnerabilities-leave-web-servers-open-to-denial-of-service-attacks>
    {{< ref "blog/2019-04-25-regular-expression-dos-weaknesses-in-crs.md" >}}
- CRS contributor Airween has made a big effort to make sure that ModSecurity 3 passes the CRS test suite. He fixed several ModSec bugs along the way (not all of them merged yet) and he has been 100% successful with ModSec3 in combination with the Apache connector. With the nginx connector, he is really close.
    Please note that this means, that none of the released ModSec 3 versions
    are able to pass the CRS 3 test suite so far.
- There was very little interest among the CRS developers to go to Tel Aviv in order to
    hold our CRS community summit during the OWASP AppSec Global conference there later in May. We have thus decided to shift our reunion to September and the
    OWASP AppSec conference in Amsterdam.
- James Walker from Portswigger / Daily Swig covered the ongoing development with ModSecurity in an online article.
    Link: <https://portswigger.net/daily-swig/waf-reloaded-modsecurity-3-1-showcased-at-black-hat-asia>
- We are very happy to welcome Andrea Menin / theMiddleBlue / MeninTheMiddle as a CRS developer with commit rights. The latter took a fair bit of time, but the joy is even bigger now.
- There is a fairly new ModSecurity integration into the Envoy Proxy on Kubernetes. We have not tested it yet, though.
    Link: <https://github.com/octarinesec/ModSecurity-envoy>

### Significant pull requests that were merged

- Extended the list of shell commands that we detect (Co-Lead Chaim Sanders)
    Link: <https://github.com/coreruleset/coreruleset/pull/1325>
- New rule 942500: SQLi bypass via MySQL comments (Developer Franziska Bühler)
    Link: [https://github.com/coreruleset/coreruleset/pull/1326](https://github.com/coreruleset/coreruleset/pull/1326)
- Fixed problems with SOAP encodings (Developer Christoph Hansen)
    Link: <https://github.com/coreruleset/coreruleset/pull/1332>
- Added the gobuster security scanner (Contributor Brent Clark)
    Link: <https://github.com/coreruleset/coreruleset/pull/1375>

### Things that are meant to happen in the coming weeks or thereafter

- Tin Zaw from Verizon is presenting CRS at the OWASP project showcase
    at the AppSec conference in Tel Aviv.
- 3.1.1 is meant to be released with a backported fix for CVE-2019-11387 as soon as we have the fix.

### Important pull requests in the queue

- Several PRs to solve the open CVEs. Yet many of these PRs come with a change
    of behaviour and we would like to avoid that.
    Link:
    <https://github.com/coreruleset/coreruleset/pull/1355>
    <https://github.com/coreruleset/coreruleset/pull/1361>
    <https://github.com/coreruleset/coreruleset/pull/1362>
- Remove Warning from php-errors.data as all the warnings are already
    covered by other strings.
    Link: <https://github.com/coreruleset/coreruleset/pull/1343>
- Add AngularJS client side template injection #1340
    Link: <https://github.com/coreruleset/coreruleset/pull/1340>
- SQLi bypass detection: ticks and backticks #1335
    Link: <https://github.com/coreruleset/coreruleset/pull/1335>
