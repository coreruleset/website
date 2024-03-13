---
author: dune73
categories:
  - Blog
date: '2021-12-09T12:54:13+01:00'
title: Introducing the CRS Sandbox
url: /2021/12/09/introducing-the-crs-sandbox/
---


The OWASP ModSecurity Core Rule Set project is very happy to present the CRS Sandbox. It's an API that allows you to test an attack payload against CRS without the need to install a ModSecurity box or anything. Here is how to do this:

> $ curl -H "x-format-output: txt-matched-rules" "https://sandbox.coreruleset.org/?search=&lt;script&gt;alert('CRS+Sandbox+Release')&lt;/script&gt;"  
> 941100 PL1 XSS Attack Detected via libinjection  
> 941110 PL1 XSS Filter - Category 1: Script Tag Vector  
> 941160 PL1 NoScript XSS InjectionChecker: HTML Injection  
> 949110 PL1 Inbound Anomaly Score Exceeded (Total Score: 15)  
> 980130 PL1 Inbound Anomaly Score Exceeded (Total Inbound Score: 15 - SQLI=0,XSS=15,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 15, 0, 0, 0

As you can see, curl is calling our sandbox with an XSS payload and the sandbox returns the list of CRS rules that the request triggered. If you are unfamiliar with CRS, then the important part is that there are several rules that triggered / detected something. And the total "anomaly score" of 15, which is far beyond the default anomaly threshold of 5 that gets a request blocked for looking like an attack.

The whole set up consists of a neatly orchestrated little herd of servers.

There is a dispatching NGINX server in front. This reverse proxy will forward the request to one of several backend CRS servers depending on configuration via extended HTTP headers. CRS will do its thing and write the results to the standard log files. But no matter how many rules triggered, we are returning a status code 200. The reverse proxy will intercept the response and it will enrich the HTTP response body. Using OpenResty, it will access the backend server - again - and look up the log files written in response to the original request. It will extract these logs, optionally reformat them and return them to the client as the HTTP response.

As you can see the whole traffic is treated as HTTP. Now if you would mean to attack the servers via the HTTP protocol itself (if that is your kink, then go ahead!), then there is a certain chance, that OpenResty or maybe even one of the webservers could mess up or break the response. Other than that, it's meant to behave like a vanilla CRS installation.

Please also notice, that we are anonymizing the IPs for our logs.

#### What's the use?

This is a sandbox that allows you to test whether CRS would block a certain payload. This can be useful for people facing a new CVE and they want to find out whether CRS could buy them time. It's also quite useful for the CRS project, since we can quickly test payloads against various versions and backends to confirm github issues (false negatives, false positives).

Or - and this is our primary audience - it can be useful for security researchers. We've seen several presentations and blog posts where researchers presented their findings against some web application. But on top, they also tested out the new attack against CRS and included the results as a separate paragraph in their publication. So the message was "Application X is vulnerable. But CRS has you covered until you can patch the server." This was very welcome for our project of course. But we also had to acknowledge that this was hard as it involved setting up a CRS docker with the correct version and the painful interpretation of the unintelligible ModSecurity logs.

But these days are over now: the CRS sandbox allows you to run a quick test and it formats the logs in a human readable way.

And there is a bonus on top: There is a header that gives you a draft version of a text snippet you can include in your blog post about a new payload:

> $ curl -H "x-format-output: txt-matched-rules-extended" "https://sandbox.coreruleset.org/?search=&lt;script&gt;alert('CRS+Sandbox+Release')&lt;/script&gt;"  
> This payload has been tested against the OWASP ModSecurity Core Rule Set  
> web application firewall. The test was executed using the apache engine and CRS version 3.3.2.
> 
> The payload is being detected by triggering the following rules:
> 
> 941100 PL1 XSS Attack Detected via libinjection  
> 941110 PL1 XSS Filter - Category 1: Script Tag Vector  
> 941160 PL1 NoScript XSS InjectionChecker: HTML Injection  
> 949110 PL1 Inbound Anomaly Score Exceeded (Total Score: 15)  
> 980130 PL1 Inbound Anomaly Score Exceeded (Total Inbound Score: 15 - SQLI=0,XSS=15,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 15, 0, 0, 0
> 
> CRS therefore detects this payload starting with paranoia level 1.

#### Is this free?

Well of course it is. Yet there is still a price tag. It's running on AWS and OWASP pays the bill. So hammer the service and we will have to switch it off since there is a threshold of how much OWASP can pay for this. And yes, we will look at the payloads we receive. If CRS does not catch them, the exploits might help us improve the rule set for future releases.

#### What headers / options are there?

You can pick the engine and the CRS version via a set of HTTP headers. Also the [CRS Paranoia Level](https://coreruleset.org/docs/configuring/paranoia_levels/) can be selected that way.

Backend: Header `"x-backend"` Values `"apache"` (default) or `"nginx"`.  
CRS version: Header `"x-crs-version:"` Values `"3.3.2"` (default), `"3.2.1"` and `"3.4.0-dev"`  
Paranoia Level: Header `"x-crs-paranoia-level"` Values from `"1"` (default) to `"4"`.

And you can change the format of the output via the help of the HTTP header `"x-format-output"`:

`"json-matched-rules"`: returns the matched rules in JSON format  
`"csv-matched-rules"`: returns the matched rules in CSV format  
`"txt-matched-rules"`: returns the matched rules in human readable  
`"txt-matched-rules-extended"`: returns the matched rules in human readable with  
additional information, ready for a publication (see above):

#### Any future plans?

We are working on an expansion of the set of backend services. And we think about a GUI version and a way to re-access previous payloads. That way you could send a friend a link to a CRS sandbox payload and she could retrieve it together with the rules it triggers.

Hand in hand with this idea is a way to link a payload to a researcher who might want to be listed in a hall of fame or something. It could be a header like "x-contact" or something.

If you have more ideas or feedback, we would be happy to talk to you. Please contact CRS via the website or our github repo.

And stay tuned for more infos.

Felipe Zipitría and Andrea Menin for the CRS project
