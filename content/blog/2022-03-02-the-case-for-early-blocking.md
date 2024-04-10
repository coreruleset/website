---
author: dune73
categories:
  - Blog
date: '2022-03-02T08:43:01+01:00'
tags:
  - Early Blocking
title: The Case for Early Blocking
---


Early Blocking is a feature that CRS will deliver with the next major release, probably Spring 2022. You can use it immediately when deploying the latest dev / nightly build. This blog post will explain the feature, how to enable it and why it is very useful.

#### What is *Early Blocking*?

ModSecurity, the engine below CRS, processes requests in multiple phases. The phase 1 is the request header phase, the phase 2 is the request body phase. Normal blocking of attacks happens at the end of phase 2. Now if CRS identifies an attack in phase 1, it will wait until the end of phase 2 to block the request. That is obviously a waste of resources (even if that waste is relatively small). But it is also a missed chance to finish off an attacker in time. But I'll come to that later.

Now, would not it be neat to block the request at end of phase 1? That's *Early Blocking*. If you are not familiar with CRS, then it may come as a surprise this feature has not existed for years. But it really did not, so it's about time CRS introduces it.

#### How to enable *Early Blocking*?

With the nightly builds and the dev-branch on github, look at the crs-setup.conf file. There is a rule 900120 that carries a config item for early blocking. Enable this rule (commented out by default) and *Early Blocking* is effective immediately.

```
SecAction \
    "id:900120,\
    phase:1,\
    nolog,\
    pass,\
    t:none,\
    setvar:tx.early_blocking=1"
```

#### Why is *Early Blocking* useful?

Spending CPU cycles on a request you already identified as malicious is a waste of time. When compared to the amount of good traffic, the malicious traffic is relatively rare for most sites, so the waste is rather small. But allowing the malicious request to proceed will also grow the number of alerts and thus eat a small piece of your attention etc.

On top, it may also allow the attacker to get away with his request in certain situations.

Let's look at a scanner pinging your IP address with an HTTP request.

Here is such a request in the access log:

```
103.203.57.xxx - - [2022-02-24 09:20:22.454279] "GET / HTTP/1.1" 301 199 "-" "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36" … 3 0
```

Nothing very bad about this request, probably lying about the user agent and an anomaly score of 3 near the end of the line. So what rule did this request trigger; there are very few rules scoring 3 after all?

Here is the alert message:

```
[2022-02-28 09:20:22.456699] [-:error] 103.203.57.xxx:35078 YhyFxmMmf45xiCZBeqtbaQAAAAA [client 103.203.57.xxx] ModSecurity: Warning. Pattern match "(?:^([\\d.]+|\\[[\\da-f:]+\\]|[\\da-f:]+)(:[\\d]+)?$)" at REQUEST_HEADERS:Host. [file "/etc/apache2/crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf"] [line "760"] [id "920350"] [msg "Host header is a numeric IP address"] [data "82.220.26.xxx"] [severity "WARNING"] [ver "OWASP_CRS/3.4.0-dev"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-protocol"] [tag "paranoia-level/1"] [tag "OWASP_CRS"] [tag "capec/1000/210/272"] [tag "PCI/6.5.10"] [hostname "www.example.com"] [uri "/"] [unique_id "YhyFxmMmf45xiCZBeqtbaQAAAAA"]
```

So the scanner used a numeric IP (-&gt; `82.220.26.xxx`) as HTTP host header and CRS barked. In the dev branch of CRS, this rule and all the rules that can run in phase 1. So at the end of phase 1, we know this is a client who uses a numeric host header as IP address. There are a few situations where this is acceptable, but it's against the RFC and it is not allowed on this server. But without early blocking the request would continue.

In the access log, we saw that the request got a 301, a redirect to a different URI. That is standard behavior: When you make a request to `/`, you get a redirect to `/anything/index.hml` or whatever. This redirect often happens between ModSecurity's phase 1 and phase 2. At least on Apache and I reckon on many other servers too.

So in fact the malicious request is directed to the desired URI. This redirect works with the Location HTTP response header:

```
Location: https://www.example.com/anything/index.html
```

So with the initial request, the scanner did not know whom he was talking to. It was simply probing IP addresses. But now we are responding with this information (actually a slight case of information leakage) and unless the scanner is very stupid it will pick up the fully qualified domain name and use it in the subsequent request as HTTP host header. So the attacker will issue a new request with valid semantics and we won't be able to detect it in phase 1 anymore.

So CRS identifies an attacker, redirect interferes and before the request can be blocked in phase 2 it is already redirected elsewhere. We had the attacker between our hands and we let the opportunity slip away. How stupid. There will be more requests, more traffic, more reconnaissance, more alerts, more things that grab our attention and all because we did not block the attacker when we could.

*Early Blocking* does away with all of this.

#### How *Early Blocking* Changes the Game

With *Early Blocking*, the access log entry of the request looks as follows:

```
45.146.165.37 - - [2022-02-28 06:36:28.459660] "GET / HTTP/1.1" 403 199 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36" "-" … 3 0
```

So the request is now blocked, no redirect, no fuss, only the minimal number of alerts (-&gt; 1!). That's the desired outcome.

Admittedly, this blockade only works with a very low anomaly threshold of 3. But if you are standing on an anomaly limit of 5, then going to 3 is a small step since there are very, very few rules that will score 3 or 4. Actually, it's mostly protocol alerts that rarely trigger false positives. So there is relatively little risk performing that change if you know what you are doing (and chances are you do since you are running CRS with an anomaly threshold of 5 already).

This is only a simple example where *Early Blocking* makes a difference. There are countless others, so using this feature is recommded.

#### The Bigger Picture

The longer I work with CRS, the more annoyed I get with too many alerts. I no longer think it is cool to have reports with thousands of alerts. I now think it is far cooler to have a clean report with as few alerts as possible and a policy that says, we terminate attackers immediately, so they do not return for subsequent attacks. Early blocking and reducing the anomaly threshold are useful steps in this direction.

After deploying the solution above, I've done the stats and noticed a slight reduction of probes of these scanners. The sample is very small so far, couple of dozens of scanners, but the median number of requests per day dropped from 2 to 1 for IP addresses triggering the numeric host header IP. The mean did not drop so much, since there are scanners that just don't care. They bump into a 403 and they simply continue with their probes. We'll have to stop that behavior with different means.  
