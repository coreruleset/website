---
author: dune73
categories:
  - Blog
date: '2022-02-09T11:51:09+01:00'
guid: https://coreruleset.org/?p=1646
id: 1646
permalink: /20220209/introducing-the-fake-bot-plugin/
tags:
  - Fake Bot Plugin
  - Lua
  - Plugins
title: Introducing the Fake Bot Plugin
url: /2022/02/09/introducing-the-fake-bot-plugin/
---


In one of my previous blog posts, I introduced the CRS plugin mechanism that we are rolling out for the next major release. Check out the blog post to learn how you can start using plugins immediately, without waiting for the next release (hint: really simple).

Several plugins are already available. One of them is the Fake Bot Plugin that I put into production recently. It's a neat little plugin written by CRS dev Azurit / Jozef Sudolsky and it can serve as a perfect illustration of the capabilities of CRS plugins.

Link to [Fake Bot Plugin](https://github.com/coreruleset/fake-bot-plugin).

#### The Problem

The bots of the big search engines are constantly scanning the internet for new and updated content. People really want to make sure their content is indexed, so they make sure any HTTP request with a user agent HTTP header belonging to a search engine is being accepted. No surprise attackers on a reconnaissance missions use strings like `"Googlebot"` as their user-agent as well. But this is in fact a lie. They pretend to be `"Googlebot"` so they are granted access. These are fake bots.

There is nothing wrong with scanning the internet, but pretending to be somebody else is bad and it leads to the wrong conclusions. And besides, reconnaissance is often a first step when preparing for an attack and therefore not welcome on most servers.

#### The Solution

Now the good thing is, the fake bots can be detected: The big search engines use specific and well known IP ranges to perform the scans and the fake bots obviously use different IP addresses. If you do a reverse lookup on the IP address of the client (or bot in our case), you will easily see it is not an official IP address used for the search engine business.

That means if we want to make sure Googlebot is really a Googlebot, then all we need to do is to make a reverse lookup and check the result.

DNS lookups are relatively heavy when compared to simple pattern matching. However, if we limit the lookup to the user-agents in question, then it becomes doable. Unfortunately, ModSecurity can not really do DNS lookups. It is necessary to perform this externally: Externally like a Lua script.

#### Putting the Solution Into a Plugin

CRS is strictly limited to ModSecurity functionality. It does not contain any Lua scripts and we want to keep it that way. Yet the lookup functionally is really handy here, so plugins to the rescue. That way we can leverage Lua without compromising the mainstream CRS functionality.

And given the set up of the plugin mechanism, we can write the code in a way that integrates into CRS. Or in other words, the Fake Bot Plugin can use anomaly scoring and leave the blocking of the request in the hands of CRS. So no separate policy, no separate administration, just an additional rule / mechanism to detect fake bots and feed into the CRS anomaly scoring.

#### The Code

The Lua code is relatively simple. Please check it out in the [github repo](https://github.com/coreruleset/fake-bot-plugin/blob/main/plugins/fake-bot.lua).

But let's look at the new rule that this plugin brings. The rule is in a file named [fake-bot-after.conf](https://github.com/coreruleset/fake-bot-plugin/blob/main/plugins/fake-bot-after.conf) in the plugins folder.

```
<pre class="wp-block-code">```
SecRule REQUEST_HEADERS:User-Agent "@pm googlebot bingbot facebookexternalhit facebookcatalog facebookbot" \
    "id:9504110,\
    phase:1,\
    block,\
    capture,\
    t:none,\
    msg:'Fake bot detected: %{tx.fake-bot-plugin_bot_name}',\
    logdata:'Matched Data: %{TX.0} found within REQUEST_HEADERS:User-Agent: %{REQUEST_HEADERS.User-Agent}',\
    tag:'application-multi',\
    tag:'language-multi',\
    tag:'platform-multi',\
    tag:'attack-bot',\
    tag:'capec/1000/225/22/77/13',\
    tag:'PCI/6.5.10',\
    tag:'paranoia-level/1',\
    ver:'fake-bot-plugin/1.0.0',\
    severity:'CRITICAL',\
    chain"
    SecRule TX:0 "@inspectFile fake-bot.lua" \
    "t:none,\
    setvar:'tx.anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```
```

First we use the parallel match operator to detect those user-agents that the plugin and its Lua script support. It's simple for Googlebot and Bingbot, but a bit more complicated for Facebook. If the user-agent is something else, we do not get a match here and the plugin execution is done. If we get a rule hit though, we advance to a chained rule, where we branch out to the Lua script. The script will either return nothing or a value that will be interpreted as a rule hit. So the Lua script is in fact the operator of this rule and a positive return value means our chained rule has triggered and we face a fake bot. We therefore use *`setvar`* to raise the CRS anomaly score at paranoia level 1. An interesting detail: The Lua script also set a variable with the name of the bot in question. That variable is used in the log message of the rule for reporting.

#### The Installation

Beyond the plugin support that is being prepared in the aforementioned blog post, you also need to be sure you have Lua-Support enabled as well as the Lua-Socket library. As far as I can tell, all the major Linux distribution provide Lua-Support with their ModSecurity packages these days. But if you want to be sure, check for the library being linked by the ModSecurity module file. Here is what I did:

```
<pre class="wp-block-code">```
$ ldd /apache/modules/mod_security2.so | grep lua
liblua5.3.so.0 => /usr/lib/x86_64-linux-gnu/liblua5.3.so.0 (0x00007f91181f2000)
```
```

When you have the pre-requisites in place (don't forget the socket library!), you simply drop the Lua script and the rule-file into the plugins folder, reload the server and you're done.

#### How it looks like in action

Here is a test call so we see the plugin in action:

```
<pre class="wp-block-code">```
$ curl https://<your-server>/ -H "User-Agent: I'm pretending to be a Bingbot"
```
```

And here is the access log entry in the extended access log described in my tutorials at [netnea.com](https://www.netnea.com/cms/apache-tutorials/).

```
<pre class="wp-block-code">```
83.76.112.xxx - - [2022-02-04 09:03:32.220707] "GET / HTTP/1.1" 403 199 "-" "I'm pretending to be a Bingbot" "-" 35480 example.com 192.168.3.7 443 - - + "" Yfzd1OCP8LadrNjJCMOyHwAAAAM TLSv1.3 TLS_AES_256_GCM_SHA384 726 6282 -% 10207 6245 0 0 5-0-0-0 0-0-0-0 5 0
```
```

You see the request being blocked with a status 403 and an anomaly score of 5 near the end of the line.

And now the corresponding error log:

```
<pre class="wp-block-code">```
[2022-02-04 09:03:32.225840] [-:error] 83.76.112.xxx:35480 Yfzd1OCP8LadrNjJCMOyHwAAAAM [client 83.76.112.xxx] ModSecurity: Warning. Fake Bot Plugin: Detected fake Bingbot. [file "/etc/apache2/coreruleset-3.3.2/plugins/fake-bot-after.conf"] [line "27"] [id "9504110"] [msg "Fake bot detected: Bingbot"] [data "Matched Data: bingbot found within REQUEST_HEADERS:User-Agent: i'm pretending to be a bingbot"] [severity "CRITICAL"] [ver "fake-bot-plugin/1.0.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-bot"] [tag "capec/1000/225/22/77/13"] [tag "PCI/6.5.10"] [tag "paranoia-level/1"] [hostname "example.com"] [uri "/"] [unique_id "Yfzd1OCP8LadrNjJCMOyHwAAAAM"]
```
```

So everything works as planned.

#### The First Harvest

Here is what I got after running this for a bit more than two weeks on a not overly popular webserver:

```
<pre class="wp-block-code">```
 13 JP 126.55.130.xxx   mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
 12 DE 130.180.17.xxx   mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  6 US 34.77.181.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  6 DE 46.80.21.xxx     mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  5 US 97.33.129.xxx    mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  5 US 75.137.221.xxx   mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  5 ES 5.59.61.xxx      mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  5 DE 62.176.253.xxx   mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  5 BG 82.103.64.xxx    mozilla/5.0 applewebkit/537.36 (khtml, like gecko; compatible; googlebot/2.1; +http://www.go ...
  5 BG 82.103.64.xxx    mozilla/5.0 applewebkit/537.36 (khtml, like gecko; compatible; googlebot/2.1; +http://www.go ...
  5 BG 79.132.20.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  4 US 69.131.91.xxx    mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  4 HK 103.126.24.xxx   mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  4 AS 35.240.117.xxx   mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  3 US 34.76.60.xxx     mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  3 GB 86.159.85.xxx    mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  3 DE 217.247.149.xxx  mozilla/5.0 (macintosh; intel mac os x 10_11_1) applewebkit/601.2.4 (khtml, like gecko) vers ...
  2 US 35.187.23.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  2 US 207.244.252.xxx  mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  2 US 130.211.96.xxx   mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  2 US 104.230.194.xxx  googlebot/2.1 (+http://www.google.com/bot.html)
  2 RU 5.165.248.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  2 CY 85.208.98.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  2 AT 178.238.2.xxx    googlebot/2.1 (+http://www.google.com/bot.html)
  1 US 65.108.4.xxx     mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  1 UA 91.235.227.xxx   mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  1 RU 88.201.163.xxx   mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  1 CY 85.208.98.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
  1 CY 85.208.98.xxx    mozilla/5.0 (compatible; googlebot/2.1; +http://www.google.com/bot.html)
```
```

This report was done with the help of a [fake-bot-report.sh](https://github.com/coreruleset/fake-bot-plugin/blob/main/util/fake-bot-report.sh) script that I cobbled together to help with reporting.

```
<pre class="wp-block-code">```
$ cat fake-bot-report.sh
#!/bin/bash
#
# Script to analyze the alerts of the OWASP ModSecurity Core Rule Set
# Fake Bot Plugin based on the error log alerts.
#
# Usage: cat error.log | fake-bot-report.sh
#
# Created in 2022 by Christian Folini.
# License: Public Domain
#
# CAVEAT: Please note that this script only reports 1 User-Agent 
# per offending IP.
# Also, need to have geoiplookup installed.


UAWIDTH=`expr $(tput cols) - 27`
TMPFILE=$(mktemp)

cat | grep 9504110 > $TMPFILE

(cat $TMPFILE | grep -o "\[client [^]]*" | cut -b9- | sort | uniq | while read IP; do
    COUNTRY=$(geoiplookup $IP | egrep -o "[A-Z]{2}," | tr -d ,)
    USERAGENT=$(grep $IP $TMPFILE | grep -o 'REQUEST_HEADERS:User-Agent: [^]]*' | sort | uniq | cut -d: -f3- | sed -e 's/\(.\{'$UAWIDTH'\}\).*/\1 .../' | tr -d \" | head -1)
    N=$(grep -c $IP $TMPFILE)
    printf "%3s %2s %-15s %s\n" $N $COUNTRY $IP "$USERAGENT"
done) | sort -nr

trap 'rm -f "$TMPFILE"' EXIT
```
```

The script can also be found in the [plugin repository](https://github.com/coreruleset/fake-bot-plugin/blob/main/util/fake-bot-report.sh).  
Feel free to use it any way you please, but please notice that it depends on `geoiplookup`.

So this is was the first blog post about the existing CRS plugins. If there is interest, I'm going to cover the auto-decoding plugin in an upcoming blog post.
