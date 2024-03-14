---
author: dune73
categories:
  - Blog
date: '2021-03-02T12:22:10+01:00'
tags:
  - ModSec3
  - ModSecurity
  - ModSecurity-NGINX connector
  - SecRequestBodyAccess
  - security
title: Disabling Request Body Access in ModSecurity 3 Leads to Complete Bypass
url: /2021/03/02/disabling-request-body-access-in-modsecurity-3-leads-to-complete-bypass/
---


If you are running ModSecurity 3 with request body access disabled, then I have some bad news. Please sit down, this will be a while. If you are running ModSecurity 2, or you give the engine access to the request body, then you are not affected. But maybe you want to read this post nevertheless. I'll be discussing a new ModSec3 vulnerability an upcoming new CRS feature and some fundamental problems affecting existing ModSecurity rule sets.

### The Vulnerability

There is a ModSecurity directive that lets you disable access to the RequestBody and ResponseBody: `SecRequestBodyAccess` / `SecResponseBodyAccess`. It's of limited use in a secure setup (since you obviously skip the imporant POST body of the request), yet some people employ the directives in niche use cases, or when they face severe performance problems (and do not want to disable ModSecurity completely).

Now the ModSecurity 3 implementation of this directive comes with a few strings attached. The first string attached: ModSecurity 3 does not really care. It still loads the body into the memory. So the positive performance effect of the directive is not really there. And the second string: When you disable body access in ModSecurity 3, then the entire ModSecurity phase:2 (request body) and phase:4 (response body) rules are skipped, despite the body being loaded into memory.

So when you have a rule that happens in phase 2, then that rule no longer happens. The rule is skipped silently regardless of the parameters that the rule actually inspects. So inspecting a HTTP header in phase 2 is no longer executed.

As it happens, most ModSecurity rules are written in phase 2. This is around 80% with CRS v3.3, and over 99% with the commercial Trustwave Spiderlabs rule set.

This means that the niche directive SecRuleRequestBodyAccess leads to an almost complete rule set bypass when employed on a typical ModSecurity 3 installation.

### Is this a CVE?

You can argue it is a CVE. Most people are not affected, but if you use ModSecurity 3 and you use said directives, then chances are, you have a systematic and complete WAF bypass on your system.

There is a stark contrast to CVE-2020-15598, where anybody running ModSec 3 on Nginx was facing a hard and simple DoS. Here only a much more limited group of users is affected, and it is not in the hands of the attackers to expose the vulnerability. But if it is active, the effect is equally devastating.

We tried to work with the ModSecurity developers at Trustwave Spiderlabs on CVE-2020-15598, but to no avail. We waited out the standard 90 days before going public, we invested countless hours in lengthy discussions and they still dispute CVE-2020-15598 with a CVSS score of 7.5 (HIGH) is a vulnerability at all. So big investment from our side, but very limited returns.

So in this particular case, we decided to inform them of the vulnerability via their github by opening [ModSec issue 2465](https://github.com/SpiderLabs/ModSecurity/issues/2465) and then work on our own turf to minimize the impact for our users instead investing into lengthy discussions. Admittedly, we did not realize the full and total impact of the vulnerability when we made our first report. More below.

### What are the DEVs doing?

Ervin Hegedüs opened the issue on the official ModSecurity GitHub on December 2, 2020. That was three months ago. A discussion evolved, but it was more about killing the directives altogether or replacing it with something subtly different.

But no fix so far. On the positive side, there is a confirmation further down in the thread that this will be fixed. But no timeline despite us asking for one.

### What can you do?

Unfortunately, you can not do much if you are affected. Chances are you disabled the body access for good reasons. In absence of good reasons, you should go back to the default setting by enabling the body access to get back your phase 2 rules (`SecRequestBodyAccess On`). Do this and you are covered.

You can also revert away from ModSecurity 3 to the stable ModSecurity 2. Despite ModSecurity 3 being released a couple of years back, ModSecurity 2 is still the reference platform for the OWASP ModSecurity Core Rule Set. Problems like this one reaffirm our policy in this regard.

So if you can move away from ModSecurity 3 to ModSecurity 2, then this solves the problem too.

And finally, you can move your own custom rules from phase 2 to phase 1. However, phase 1 runs before the request body arrives. So you are limited in the things you can do. You can not access the request body. But given you disable the body access, chances are, you do not care. So moving all your custom rules from phase 2 to phase 1 is solving the problem in your limited use case.

### What can we do for you?

CRS is an anomaly scoring rule set. The final blocking decision happens at the end of phase 2. So the weakness effectively prevents CRS from blocking an attacker ever; even if we identify the attack in phase 1. So we decided to introduce a feature, that has been sitting in the drawer for some time: Early Blocking. Instead of waiting until the end of phase 2 with the blocking decision, there is an optional blocking decision at the end of phase 1. So attacks that are identified in phase 1 can also be blocked in phase 1.

Additionally, we decided to move as many rules as possible from phase 2 into phase 1. Effectively, that's all the rules that deal with request headers and none of the rules that deal with the request body. Keep in mind that even with this change, most of the attack detection will not be active as they run necessarily in phase 2 and later phase 4 in order to scan request/response bodies. But there were a few dozens of rules that we were able to move.

On a functional level, this would not change a thing since it would be the same rules running earlier. That way we could mitigate the problem for those users who are affected while the ModSecurity developers work on their fix.

The plan was then to release this as 3.3.1 and making it clear in the release notes, that this was mainly for users affected by the ModSecurity vulnerability in question.

Or so we thought. But then reality hit and we had to stop the release process after the first release candidate [3.3.1-RC1](https://github.com/coreruleset/coreruleset/releases/tag/v3.3.1-rc1). So our master branch on github has many, many rules in phase 1 now, but we are not yet in a position to release this with full support.
  
Let's talk about why!

### Why our plan to release 3.3.1 faltered

ModSecurity rules can reside in the server context of the webserver configuration, on the virtual host level or inside a location container. While I generally advocate sticking to the webserver level, there are a lot of users configuring or tuning their setup on the container level. In fact, also the [ModSecurity Handbook](https://www.feistyduck.com/books/modsecurity-handbook/) that I co-wrote for the 2nd edition, explains how to configure / tune ModSecurity on the container level.

A typical configuration is the following:

```apacheconf
...

Include /path/to/crs/rules/*.conf

...

<VirtualHost ...>

   ...

   <Proxy https://backend-server:8000/>

      SecRuleEngine Off

   </Proxy>

</VirtualHost>
```

With this setup, you disable ModSecurity for an individual container. The catch: this only works from phase 2. This means that phase 1 is executed just fine and then when phase 2 starts, the ModSecurity engine stops and the request is allowed access.

With a rule set that runs in phase 2 mostly, you do not notice. But if the rule set works in phase 1, then all the phase 1 rules are being applied before you get to disable the engine. And when CRS decides to move a lot of rules form phase 2 to phase 1, they are suddenly running and will start to throw false positives. No request is going to be blocked since the engine stops before the blocking rule is applied at the end of phase 2, but the change is too big for a point release in the 3.3 release line. It's a visible change, and unless you understand the mechanics it is terrifying to see a lot of new false positive alerts you have not seen before.

So we decided to cancel the 3.3.1 release, and concentrate on the next major release, that will bring the rule shift. That way we have more time to tell our users how to avoid the configuration pattern above and how to make their configuration compatible with a rule set that also runs in phase 1.

### How to get the CRS 3.3.1-RC1 in the meantime

Note: You only need to do this if you are running on ModSec 3, and have `SecRequestBodyAccess Off`. We still recommend, if possible, to run with `SecRequestBodyAccess On` instead. However this advice is there for those who cannot do that.

In that case, using our CRS 3.3.1-RC1 release candidate is a valid option. The difference to the release 3.3.0 is the introduction of the early-blocking feature and the shift of dozens of rules from phase 2 to phase 1.

Here is the link to the release candidate, which has been used in production successfully (so you are not our guinea pig).  
  
<https://github.com/coreruleset/coreruleset/releases/tag/v3.3.1-rc1>

### More bad news: The ModSecurity-NGINX connector module

As it turned out, this was not the end of the whole story. People giving 3.3.1-RC1 a spin reported additional problems on ModSecurity 3: There is a problem with the ModSecurity-NGINX connector module. This module provides the API between NGINX and the standalone ModSecurity 3 engine. When we enable the early blocking on ModSecurity 3 with the intention to stop a request at the end of phase 1, the request would simply continue on the server all through phase 2 and 3.

Further analysis revealed, this is a bug in the connector module. Good for us, this has meanwhile been fixed in the code (Head tip to [defanator](https://github.com/defanator) from NGINX). Yet again, there is little sign from Trustwave Spiderlabs that they intend to do a new release for the ModSecurity-NGINX connector with the fix.

While investigating the problem, we also discovered an oddity that can be used as a workaround. By providing NGINX with explicit error-documents, you can hide this bug connector bug. Personally, I have not really understood how the workaround works and I recommend to use the fixed code. Yet the workaround has been tested to work.

Here is how it looks:

```nginxconf
...

    error_page 404 /error_404.html

...
```

In case you have configured the error\_page directive in your configuration, then the workaround for this bug is already in place and you do not even notice the bug it's there.

So, this leaves you with two options if you want to run early blocking on ModSecurity 3 with NGINX:

- You compile the connector module yourself from the sources
- Use the error\_page workaround

### Conclusion

There is a very bad bug in ModSecurity 3 that is affecting installations that have disabled request body access via the directive SecRequestBodyAccess. While discussing this with the ModSecurity developers, we understood the full extent of this security problem. We then tried to put a fix into action to cover our users, but encountered additional problems along the way that killed our plan to release a CRS fix / workaround for the problem as 3.3.1.

It is unfortunate, that ModSecurity 3 continues to surprise us with bugs and security problems on such a fundamental level.

### Update

\[2021-02-04\]: Portswigger is [covering this problem in an](https://portswigger.net/daily-swig/dispute-rages-over-modsecurity-3-waf-bypass-risk)[ ](https://portswigger.net/daily-swig/dispute-rages-over-modsecurity-3-waf-bypass-risk)[article](https://portswigger.net/daily-swig/dispute-rages-over-modsecurity-3-waf-bypass-risk)

Christian Folini, CRS Co-Lead, with a lot of support by Ervin Hegedüs
