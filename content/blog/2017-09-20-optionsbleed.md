---
author: Chaim Sanders
categories:
  - Blog
date: '2017-09-20T03:15:37+02:00'
guid: https://coreruleset.org/?p=532
id: 532
permalink: /20170920/optionsbleed/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: OptionsBleed Defenses
url: /2017/09/20/optionsbleed/
---


This week we saw the release of another named vulnerability (-\_-). This time it was entitled: Optionsbleed. While the name provided is meant in reference to Heartbleed, this vulnerability isn't nearly as far reaching. The vulnerability only affected Apache hosts with a very particular configuration and as a result only 0.0466% of the Alexa top one million sites were detected as vulnerable. Additionally, considering the requirements for exposing the vulnerability is dependent on a complex and unusual configuration it is less likely to be seen on less popular pages that tend to stick more closely to stock configuration.

In spite of it's relative rarity you might be wonder if it can be protected against using SecRules. In this post we'll take a quick look at three different methods in order to prevent this issue. The following three methods will be discussed:

- Using OWASP CRS DOS protection
- Using OWASP CRS to prohibit the OPTIONS method
- Using Mod\_Headers + SecRules to remove bad 'allow' headers.

Generally OWASP Core Rule Set will provide protection against HTTP level DOS attacks. In this case, the POC for the Optiosnbleed attack recommends making 100 subsequent requests. This could easily be blocked by configuring the DOS protection provided with OWASP CRS. To do this one could modify the crs-setup.conf to provide more strict limits. This may look similar to as follows:

`<br></br>SecAction \<br></br>"id:900700,\<br></br>phase:1,\<br></br>nolog,\<br></br>pass,\<br></br>t:none,\<br></br>setvar:'tx.dos_burst_time_slice=60',\<br></br>setvar:'tx.dos_counter_threshold=20',\<br></br>setvar:'tx.dos_block_timeout=600'"`

It may be even easier to solve this. By default, OWASP CRS allows the following HTTP methods: GET, POST, HEAD, and OPTIONS. If you are not using the OPTIONS method for things like CORS, you can disable it. This could be done in the following manner:

`<br></br>SecAction \<br></br>"id:900200,\<br></br>phase:1,\<br></br>nolog,\<br></br>pass,\<br></br>t:none,\<br></br>setvar:'tx.allowed_methods=GET HEAD POST'"<br></br>`

If all else fails, it is possible to remove HTTP headers using mod\_headers. We can limit this removal to only be undertaken in the event that vulnerable HTTP Accept headers are going to be displayed by using SecRules. This can be accomplished in a manner similar to the following:

`<br></br># This will only work on Apache<br></br>SecRule &RESPONSE_HEADERS:Accept "@eq 1" "chain,id:123,log,msg:'Found outbound accept'"<br></br>SecRule RESPONSE_HEADERS:Accept "!@rx (?:GET|POST|HEAD|OPTIONS),?\s*" "t:none,setenv:accept_found=%%{matched_var}"<br></br>Header unset Accept env=accept_found<br></br>`  
There are undoubtedly many other ways to solve this issue in addition to the three we have shown here. Hopefully these examples have demonstrated valuable common design patterns when considering how to protect against newly released vulnerabilities.