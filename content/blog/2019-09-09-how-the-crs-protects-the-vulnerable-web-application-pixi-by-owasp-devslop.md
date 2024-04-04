---
author: Franziska Buehler
categories:
  - Blog
date: '2019-09-09T10:37:38+02:00'
tags:
  - DevSlop
title: How the CRS protects the vulnerable web application Pixi by OWASP DevSlop
url: /2019/09/09/how-the-crs-protects-the-vulnerable-web-application-pixi-by-owasp-devslop/
---


How could the functionality of a WAF be better demonstrated than with a vulnerable web application?

In this blog post I introduce Pixi, an intentionally vulnerable web application by the OWASP project DevSlop. I show its known vulnerabilities and examine how the CRS protects against these vulnerabilities.

What is Pixi?

Pixi is a deliberately vulnerable web application that is part of the [OWASP DevSlop project](https://devslop.co). Beside Tanya Janca, Nicole Becher and Nancy Gariché I am also part of this project. DevSlop is a training ground for DevSecOps. In addition to Pixi, DevSlop also offers many [YouTube shows](https://www.youtube.com/channel/UCSmjcWvgVBqF3x_7e5rfe3A), blog posts and different [modules](https://devslop.co/Home/Module) on various security topics!

The good news is, the vulnerable web application Pixi can be protected with the Core Rule Set in a very effective way!

Setup

To start Pixi and the CRS in front of it, I use the official [docker-compose.yaml](https://github.com/coreruleset/coreruleset/blob/v3.2.0-rc2/util/docker/docker-compose.yaml) provided by the Core Rule Set and I add the Pixi part below the CRS part:

```dockerfile
# This docker-compose file starts owasp/modsecurity-crs

version: "3"

services:

  crs:
    image: owasp/modsecurity-crs
    ports:
      - "80:80"
      # only available if SETTLS was enabled:
      - "443:443"

    environment:
      - SERVERNAME=localhost

      #############################################
      # CRS Variables
      #############################################
      # Paranoia Level
      - PARANOIA=1
      # Inbound and Outbound Anomaly Score Threshold
      - ANOMALYIN=5
      - ANOMALYOUT=4
      # Executing Paranoia Level
      # - EXECUTING_PARANOIA=2

      #######################################################
      # Reverse Proxy mode
      # (only available if SETPROXY was enabled during the
      # parent ModSecurity image)
      #######################################################
      # PROXYLOCATION: Application Backend of Reverse Proxy
      - PROXYLOCATION=http://app:8000/
      #

  db:
    image: deadrobots/pixi:datastore
    container_name: pixidb
    expose:
      - "27017"
      - "28017"

  app:
    image: deadrobots/pixi:app
    ports:
      - "127.0.0.1:8000:8000"
      - "127.0.0.1:8090:8090"
```

The image `owasp/modsecurity-crs` is the new official OWASP ModSecurity Core Rule Set container image. It supports the TLS and PROXY mode per default.  
We use the standard installation, the Paranoia Level 1 and an inbound anomaly threshold of 5 and outbound anomaly threshold of 4. The backend, Pixi, runs on port 8000 and we set the PROXYLOCATION env var to the service app with port 8000. The CRS Reverse Proxy listens on port 80 and 443.

I will use port 80 for demonstration, but it's very easy to mount a valid TLS server certificate into the container and provide proper TLS.

### Pixis Vulnerabilities

Let's now dive into Pixi's weaknesses:

#### Authentication bypass

With a simple Mongo DB injection, the authentication can be bypassed. For further reading about this class of vulnerabilities, see [here](https://www.owasp.org/index.php/Testing_for_NoSQL_injection).

Unfortunately, I can not show this vulnerability. As soon as I replay this request in ZAP ([Zed Attack Proxy](https://www.zaproxy.org/)) the application Pixi dies. You could say it's a remote DoS on top of the authentication problem. One more reason the use CRS to protect us from this problem!

When I replay the request through the CRS, Pixi doesn't die anymore, because CRS blocks the request at Paranoia Level 1:

{{< figure src="images/2019/09/Authentication_Bypass_Request.png" caption="Authentication Bypass: ZAP Request Editor" >}}
{{< figure src="images/2019/09/Authentication_Bypass_Response.png" caption="Authentication Bypass: ZAP Response" >}}
The logfile tells us that the MongoDB injection was detected (id: 942290). It says that the access was denied (id: 949110) and that the Inbound Anomaly Score of the request at PL1 was 5 (id: 980130). The last two log file entries (id: 949110 and 980130) always occur with a blocked request.

```
[Mon Sep 09 07:40:47.839300 2019] [:error] [pid 44:tid 139999475324672] [client 192.168.0.1:59602] [client 192.168.0.1] ModSecurity: Warning. Pattern match "(?i:(?:\\\\\\\\[\\\\\\\\$(?:ne|eq|lte?|gte?|n?in|mod|all|size|exists|type|slice|x?or|div|like|between|and)\\\\\\\\]))" at ARGS_NAMES:pass[$ne]. [file "/etc/modsecurity.d/owasp-crs/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf"] [line "367"] [**id "942290"**] [**msg "Finds basic MongoDB SQL injection attempts"**] [data "Matched Data: [$ne] found within ARGS_NAMES:pass[$ne]: pass[$ne]"] [severity "CRITICAL"] [ver "OWASP_CRS/3.2.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-sqli"] [tag "OWASP_CRS"] [tag "OWASP_CRS/WEB_ATTACK/SQL_INJECTION"] [tag "WASCTC/WASC-19"] [tag "OWASP_TOP_10/A1"] [tag "OWASP_AppSensor/CIE1"] [tag "PCI/6.5.2"] [hostname "localhost"] [uri "/login"] [unique_id "XXYB-5tiXQGQt80jpPMnxgAAAJc"], referer: http://localhost:80/login

[Mon Sep 09 07:40:47.845881 2019] [:error] [pid 44:tid 139999475324672] [client 192.168.0.1:59602] [client 192.168.0.1] ModSecurity: Access denied with code 403 (phase 2). Operator GE matched 5 at TX:anomaly_score. [file "/etc/modsecurity.d/owasp-crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf"] [line "91"] [**id "949110"**] [**msg "Inbound Anomaly Score Exceeded (Total Score: 5)"**] [severity "CRITICAL"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-generic"] [hostname "localhost"] [uri "/login"] [unique_id "XXYB-5tiXQGQt80jpPMnxgAAAJc"], referer: http://localhost:80/login

[Mon Sep 09 07:40:47.849314 2019] [:error] [pid 44:tid 139999475324672] [client 192.168.0.1:59602] [client 192.168.0.1] ModSecurity: Warning. Operator GE matched 5 at TX:inbound_anomaly_score. [file "/etc/modsecurity.d/owasp-crs/rules/RESPONSE-980-CORRELATION.conf"] [line "86"] [**id "980130"**] [msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 5 - SQLI=5,XSS=0,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): **individual paranoia level scores: 5, 0, 0, 0**"] [tag "event-correlation"] [hostname "localhost"] [uri "/login"] [unique_id "XXYB-5tiXQGQt80jpPMnxgAAAJc"], referer: http://localhost:80/login
```

As the logfiles are a bit hard to read, I will shorten the output of the next vulnerabilities and use Christian Folini's alias `melidmsg`. For further information about his aliases, see Christian's [tutorials](https://www.netnea.com/cms/apache-tutorials/).

### Angular Constructor Injection

Under special circumstances an Angular template injection is possible. This can happen when client side security checks are disabled (that must not be disabled). For further reading, please see [here](http://blog.portswigger.net/2016/01/xss-without-html-client-side-template.html).

So let's see what Pixi does with this command in the login mask:

```javascript
{{constructor.constructor('alert(1)')()}}
```

{{< figure src="images/2019/09/Angular_Request_Form-1.png" caption="Angular Template Injection" >}}
{{< figure src="images/2019/09/Angular_Request_Popup-1.png" caption="Angular Template Injection: Popup" >}}
Ooops, we showed a popup window through XSS!

So let's see what the Core Rule Set does with this command:

{{< figure src="images/2019/09/Angular_PL1.png" caption="Angular Template Injection: Popup at PL1" >}}

The CRS at Paranoia Level 1 does not detect this Angular injection. Why could this happen?

That's possible because the CRS is not meant to protect us from every exploit at Paranoia Level 1.

There are 4 Paranoia Levels available. If our web application is critical and if we want to assure that our web application is well protected we should consider raising the Paranoia Level. This will enable additional rules giving you a rule set with better coverage. But unfortunately also with more false positives.

Let's do this and see what the CRS does at PL2:

{{< figure src="images/2019/09/Angular_PL2.png" caption="Angular Template Injection: CRS blocks at PL2" >}}
The request is now blocked and the log confirms this:

```sh
$ cat my-alert-error.log | melidmsg
941380 AngularJS client side template injection detected
942370 Detects classic SQL injection probings 2/3
942430 Restricted SQL Character Anomaly Detection (args): # of special characters exceeded (12)
949110 Inbound Anomaly Score Exceeded (Total Score: 13)
980130 Inbound Anomaly Score Exceeded (Total Inbound Score: 13 - SQLI=8,XSS=5,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 0, 13, 0, 0
```

An Angular template injection was discovered. That's correct! By the way the rule 941380 is one of many new rules in CRS 3.2.

And also two SQLi rules triggered. That's possible, because the SQL Injection is the most covered vulnerability and the detection is very strong there. Therefore very often SQLi rules, especially at higher PLs, also trigger. But that's not a problem as far as they protect us and as far as they do not generate False Positives. If they protect us, they are very welcome.

### XSS on search field

The next vulnerability is a XSS weakness in the search field.

The following string entered in the search field shows a popup, that demonstrates us the XSS weakness:

```javascript
<script>alert('xss')</script>
```

{{< figure src="images/2019/09/XSS.png" caption="Cross Site Scripting in Search Field" >}}
The Core Rule Set at PL1 blocks this XSS test request:

{{< figure src="images/2019/09/XSS_blocked.png" caption="Cross Site Scripting: CRS blocks" >}}
In the logs we see that three XSS rules were triggered by this request and we got a Inbound Anomaly Score of 15 at PL1!

```sh
$ cat my-alert-error.log | melidmsg
941100 XSS Attack Detected via libinjection
941110 XSS Filter - Category 1: Script Tag Vector
941160 NoScript XSS InjectionChecker: HTML Injection
949110 Inbound Anomaly Score Exceeded (Total Score: 15)
980130 Inbound Anomaly Score Exceeded (Total Inbound Score: 15 - SQLI=0,XSS=15,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 15, 0, 0, 0
```

#### Verbose Errors

When not logged in as an admin of the application, the access to the admin path throws an HTTP 500 error. This error reveals some information about the application:

{{< figure src="images/2019/09/admin-2.png" caption="Verbose Errors in Admin Page" >}}

When accessing the secret page, the error even shows a hint to a server.conf file:

{{< figure src="images/2019/09/secret.png" caption="Verbose Errors in Secret Page" >}}

When running at PL1 this response error remains undetected but not at PL2:

{{< figure src="images/2019/09/admin_blocked-1.png" caption="Verbose Errors in Admin Page are blocked at PL2" >}}
{{< figure src="images/2019/09/secret-blocked.png" caption="Verbose Errors in Secret Page are blocked at PL2" >}}

In the logs we see that the response code 500 was blocked at PL2 due to potential information leakage:

```sh
$ cat my-alert-error.log | melidmsg
950100 The Application Returned a 500-Level Status Code
959100 Outbound Anomaly Score Exceeded (Total Score: 4)"]
980140 Outbound Anomaly Score Exceeded (score 4): individual paranoia level scores: 0, 4, 0, 0
```

#### Insecure Direct Object Reference

In the error message above we saw that there must be a server.conf. So let's access the file and see what it reveals to us:

{{< figure src="images/2019/09/serverconf.png" caption="server.conf reveals session_secret" >}}
The server.conf even shows a session_secret. That is very awful!

Does the Core Rule Set protect us?

{{< figure src="images/2019/09/serverconf_blocked.png" caption="server.conf is blocked at PL1" >}}
The log confirms that a request to a .conf file is potentially dangerous:

```sh
$ cat my-alert-error.log | melidmsg
920440 URL file extension is restricted by policy
949110 Inbound Anomaly Score Exceeded (Total Score: 5)
980130 Total Inbound Score: 5 - SQLI=0,XSS=0,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 5, 0, 0, 0
```

The triggered rule 920440 at PL1 blocks potentially dangerous file extensions. The extension .conf is part of this list. Of course, these file extensions can be configured. But the standard installation protects us. With the CRS in front of Pixi this session_secret will never be exposed!

### Conclusion

The standard installation at PL1 already protects us from a bunch of vulnerabilites. But to be protected from more vulnerabilities and exploits a higher Paranoia Level is highly recommended.

In the examples above the highest Paranoia Level I had to configure was PL2 and there are even PL 3 and PL4!
