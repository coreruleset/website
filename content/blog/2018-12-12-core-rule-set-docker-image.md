---
author: franbuehler
categories:
  - Blog
date: '2018-12-12T10:27:37+01:00'
title: Core Rule Set Docker Image
url: /2018/12/12/core-rule-set-docker-image/
---


The Core Rule Set is installed in just four steps, as described in the [Installation Guide](https://coreruleset.org/installation/).

Now, it's even easier using the CRS Docker container. The effort to start the CRS in front of an application is reduced to a few seconds and only one command.

Franziska Bühler, one of the CRS developers, enhanced the [official CRS container](https://hub.docker.com/r/owasp/modsecurity-crs/). Various CRS variables and the backend application to be protected can be configured using this [enhanced container](https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/).

## Vulnerable Web Application

For this blog post, we use the intentionally vulnerable web application Pixi from the [OWASP project DevSlop](https://devslop.co/). DevSlop is an open source project in which Tanya Janca, Nicole Becher and Franziska Bühler explore DevSecOps through writing vulnerable apps, creating pipelines, publishing proof of concepts, and documenting what they have learned on their [YouTube Channel](https://aka.ms/DevSlopShow) and blogs.

One of the application vulnerabilities is that the search field is vulnerable to reflected XSS attacks:

{{< figure src="images/2018/12/Pixi_XSS.png" >}}

Oops... The injected content is reflected back to the user.

This is one example.

Another misbehaviour of the application is that the secret key is stored in a publicly accessible server.conf file:

{{< figure src="images/2018/12/Pixi_serverconf.png" >}}

These are just two examples of this vulnerable web application. One is a classic XSS attack and one is a misconfiguration of the application that results in sensitive data exposure.

The Pixi application has even [more vulnerabilities](http://prezo.s3.amazonaws.com/pixi_california_2018/pixi_lab.md) to demonstrate. Franziska plans to write about it in another blog post and to show how the CRS makes these vulnerabilities unexploitable.

Of course, these vulnerabilities should be fixed in the application itself. But in the real world, it is not always possible to patch the vulnerabilities within a reasonable timeframe. Or sometimes, we simply have no control over the application software. And this is where the CRS comes in...

The CRS prevents the exploitation of the two attacks described above. The CRS is not a substitute for patching the software, but an additional layer of defence, a safety net in front of your application, protecting you from these attacks: CRS is the 1st line of defense!

## Start CRS in container

The Core Rule Set can protect you against vulnerabilities and application security risks, such as those described by the OWASP Top 10.

This means that our attacks executed in the example above should be blocked by the CRS.

But first, we have to start the CRS in front of the application. Let's do this in a really easy and straightforward way, in a Docker container:

```sh
docker run -dti \
--name apachecrsrp \
--env PARANOIA=1 \
--env ANOMALYIN=5 \
--env ANOMALYOUT=5 \
--env ALLOWED_METHODS="GET POST" \
--env MAX_FILE_SIZE=5242880 \
--env RESTRICTED_EXTENSIONS=".conf/" \
--env PORT=8001 \
--publish 8001:8001 \
--env BACKEND=http://192.168.1.129:8000 \
franbuehler/modsecurity-crs-rp
```

Fore more `docker run` examples and a complete list of possible environment variables, visit <https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/>. This blog post only covers a brief selection of them.

The documentation of the CRS variables can be found in the current `crs-setup.conf.example`. At the time of this writing, this is <https://github.com/coreruleset/coreruleset/blob/v3.2/dev/crs-setup.conf.example>.

Let's have a look what we do in the `docker run` command above:

We start our CRS container with a `paranoia_level` of 1, an `inbound_anomaly_score_threshold` of 5 and an `outbound_anomaly_score_threshold` of 5. These are internal configuration variables of the CRS that we configure here on the command line. Our values are mostly default values, but for the sake of clarity, we will do it anyway.

Then we tell the CRS to allow only GET and POST methods by setting the `tx.allowed_methods` CRS variable.  
The application allows for uploading images. We don't want to allow pictures larger than 5 MB. We achieve this by setting the `tx.max_file_size` variable to 5,242,880 bytes.

As our application leaks sensitive information in a .conf file, we forbid access to this file extension. The default value of `restricted_extensions` is a long list of extensions that already contains .conf. Nevertheless, we explicitly set the value` .conf` for this blog post, as an example. But it's absolutely ok to not touch this value and to let the default value with numerous extensions take effect.

The listening port 8001 of the Apache Reverse Proxy can be set using the Docker environment variable PORT. This means the Apache inside the Docker container will run under the port 8001.
We also either need to use port mapping `--port 8001:8001` or make this listening port available on the Docker host with `--expose`. In some CI/CD environments, port mapping can not be used. Instead, we would then use `--expose`.
But here, we map port 8001 from inside the container to port 8001 on our Docker host. Apache, with the Core Rule Set, can thus be called under port 8001 on the Docker host. [CIS Docker Benchmark](https://www.cisecurity.org/cis-benchmarks/) recommends ensuring that container ports are not mapped to host port numbers below 1024.
Instead of mapping every interface (0.0.0.0) with `--publish 8001:8001` we could also use an explicit IP address here. That would be more secure, especially on productive systems.

The backend application listens on the IP address 192.168.1.129 and on port 8000. This can be configured with the Docker environment variable BACKEND=http://192.168.1.129:8000. We can not use the localhosts IP address 127.0.0.1 here, but the real IP address of the application because this localhost would be inside the container and can not be use to address the application outside the container.

With `docker ps` we test if our CRS container is up and running:

```sh
docker ps

CONTAINER ID        IMAGE                                 COMMAND                  CREATED             STATUS             PORTS                                                NAMES

68ecd59b1a51  franbuehler/modsecurity-crs-rp     /docker-entrypoint.…"   4 seconds ago       Up 3 seconds        80/tcp, 0.0.0.0:8001->8001/tcp                       apachecrsrp
```

We want to repeat our first XSS attack now and see if CRS blocks it, and we hope it does!

We now call the TCP port 8001 of the CRS container:

{{< figure src="images/2018/12/CRS_XSS.png" >}}

The attack can no longer be executed. We get a 403-forbidden status code. That's what we expected.

But what happened inside the CRS Docker container? We want to examine the error.log.

We `cat` the error.log from the CRS Docker container. Of course, we could also work with Docker volumes, the command `docker cp apachecrsrp:/var/log/apache2/error.log .` or Splunk drivers here. But for our example we do it with `cat`:

```sh
docker exec -ti apachecrsrp cat /var/log/apache2/error.log
```

error.log:
```
[2018-11-30 15:01:39.039585] [-:error] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU [client 172.17.0.1] ModSecurity: Warning. detected XSS using libinjection. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"] [line "60"] [id "941100"] [msg "XSS Attack Detected via libinjection"] [data "Matched Data: XSS data found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"] [severity "CRITICAL"] [ver "OWASP_CRS/3.0.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-xss"] [tag "OWASP_CRS/WEB_ATTACK/XSS"] [tag "WASCTC/WASC-8"] [tag "WASCTC/WASC-22"] [tag "OWASP_TOP_10/A3"] [tag "OWASP_AppSensor/IE1"] [tag "CAPEC-242"] [hostname "localhost"] [uri "/search/"] [unique_id "W-6t05raviJ3p3xEdXWl4AAAAMU"]
[2018-11-30 15:01:39.039716] [-:error] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU [client 172.17.0.1] ModSecurity: Warning. Pattern match "(?i)[&lt;\\\\xef\\\\xbc\\\\x9c]script[^&gt;\\\\xef\\\\xbc\\\\x9e]\*[&gt;\\\\xef\\\\xbc\\\\x9e][\\\\\\\\s\\\\\\\\S]\*?" at ARGS:query. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"] [line "92"] [id "941110"] [msg "XSS Filter - Category 1: Script Tag Vector"] [data "Matched Data: &lt;script&gt; found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"] [severity "CRITICAL"] [ver "OWASP_CRS/3.0.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-xss"] [tag "OWASP_CRS/WEB_ATTACK/XSS"] [tag "WASCTC/WASC-8"] [tag "WASCTC/WASC-22"] [tag "OWASP_TOP_10/A3"] [tag "OWASP_AppSensor/IE1"] [tag "CAPEC-242"] [hostname "localhost"] [uri "/search/"] [unique_id "W-6t05raviJ3p3xEdXWl4AAAAMU"]
[2018-11-30 15:01:39.040062] [-:error] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU [client 172.17.0.1] ModSecurity: Warning. Pattern match "(?i)&lt;[^\\\\\\\\w&lt;&gt;]\*(?:[^&lt;&gt;\\\\"'\\\\\\\\s]\*:)?[^\\\\\\\\w&lt;&gt;]\*(?:\\\\\\\\W\*?s\\\\\\\\W\*?c\\\\\\\\W\*?r\\\\\\\\W\*?i\\\\\\\\W\*?p\\\\\\\\W\*?t|\\\\\\\\W\*?f\\\\\\\\W\*?o\\\\\\\\W\*?r\\\\\\\\W\*?m|\\\\\\\\W\*?s\\\\\\\\W\*?t\\\\\\\\W\*?y\\\\\\\\W\*?l\\\\\\\\W\*?e|\\\\\\\\W\*?s\\\\\\\\W\*?v\\\\\\\\W\*?g|\\\\\\\\W\*?m\\\\\\\\W\*?a\\\\\\\\W\*?r\\\\\\\\W\*?q\\\\\\\\W\*?u\\\\\\\\W\*?e\\\\\\\\W\*?e|(?:\\\\\\\\W\*?l\\\\\\\\W\*?i\\\\\\\\W\*?n\\\\\\\\W\*?k|\\\\\\\\W\*?o\\\\\\\\W\*?b\\\\\\\\W\*?j\\\\\\\\W\*?e\\\\ ..." at ARGS:query. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"] [line "217"] [id "941160"] [msg "NoScript XSS InjectionChecker: HTML Injection"] [data "Matched Data: &lt;script found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"] [severity "CRITICAL"] [ver "OWASP_CRS/3.0.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-xss"] [tag "OWASP_CRS/WEB_ATTACK/XSS"] [tag "WASCTC/WASC-8"] [tag "WASCTC/WASC-22"] [tag "OWASP_TOP_10/A3"] [tag "OWASP_AppSensor/IE1"] [tag "CAPEC-242"] [hostname "localhost"] [uri "/search/"] [unique_id "W-6t05raviJ3p3xEdXWl4AAAAMU"]
[2018-11-30 15:01:39.041614] [-:error] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU [client 172.17.0.1] ModSecurity: Access denied with code 403 (phase 2). Operator GE matched 5 at TX:anomaly_score. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf"] [line "93"] [id "949110"] [msg "Inbound Anomaly Score Exceeded (Total Score: 15)"] [severity "CRITICAL"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-generic"] [hostname "localhost"] [uri "/search/"] [unique_id "W-6t05raviJ3p3xEdXWl4AAAAMU"]
[2018-11-28 15:01:39.042530] [-:error] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU [client 172.17.0.1] ModSecurity: Warning. Operator GE matched 5 at TX:inbound_anomaly_score. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-980-CORRELATION.conf"] [line "86"] [id "980130"] [msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 15 - SQLI=0,XSS=15,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): NoScript XSS InjectionChecker: HTML Injection; individual paranoia level scores: 15, 0, 0, 0"] [tag "event-correlation"] [hostname "localhost"] [uri "/error/403.html"] [unique_id "W-6t05raviJ3p3xEdXWl4AAAAMU"]
```

Three different CRS rules detected the XSS attack:

- In CRS rule 941100, libinjection says: "XSS data found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;".
- Rule 941110 detects "Matched Data: &lt;script&gt; found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;".
- Rule 941160 complains about the script tag: "Matched Data: &lt;script found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"

These three violated rules result in a total Inbound Anomaly Score of 15, which is higher than our configured Inbound Anomaly Score Threshold of 5. We see this in the request blocking evaluation rule 949110 or with detail values of each paranoia level in rule 980130.

We also check what happened to the blocked .conf file. This request can no longer be executed:

{{< figure src="images/2018/12/CRS_serverconf.png" >}}

The corresponding log entries can be found here:

```
[2018-11-30 15:21:53.786966] [-:error] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE [client 172.17.0.1] ModSecurity: Warning. String match within ".conf/" at TX:extension. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf"] [line "1069"] [id "920440"] [msg "URL file extension is restricted by policy"] [data ".conf"] [severity "CRITICAL"] [ver "OWASP_CRS/3.0.0"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-protocol"] [tag "OWASP_CRS/POLICY/EXT_RESTRICTED"] [tag "WASCTC/WASC-15"] [tag "OWASP_TOP_10/A7"] [tag "PCI/6.5.10"] [hostname "localhost"] [uri "/server.conf"] [unique_id "W-6ykartDdny6dEbaKB05gAAAJE"]
[2018-11-30 15:21:53.791227] [-:error] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE [client 172.17.0.1] ModSecurity: Access denied with code 403 (phase 2). Operator GE matched 5 at TX:anomaly_score. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf"] [line "93"] [id "949110"] [msg "Inbound Anomaly Score Exceeded (Total Score: 5)"] [severity "CRITICAL"] [tag "application-multi"] [tag "language-multi"] [tag "platform-multi"] [tag "attack-generic"] [hostname "localhost"] [uri "/server.conf"] [unique_id "W-6ykartDdny6dEbaKB05gAAAJE"]
[2018-11-30 15:21:53.792642] [-:error] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE [client 172.17.0.1] ModSecurity: Warning. Operator GE matched 5 at TX:inbound_anomaly_score. [file "/etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-980-CORRELATION.conf"] [line "86"] [id "980130"] [msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 5 - SQLI=0,XSS=0,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): URL file extension is restricted by policy; individual paranoia level scores: 5, 0, 0, 0"] [tag "event-correlation"] [hostname "localhost"] [uri "/error/403.html"] [unique_id "W-6ykartDdny6dEbaKB05gAAAJE"]
```

- CRS rule 920440 now states that our configured file extension .conf is not allowed: `[msg "URL file extension is restricted by policy"] [data ".conf"]`
- In rule 949110, we see that the request was blocked because of the too high Inbound Anomaly Score of 5. And in rule 980130 we see again the details.

As mentioned earlier, this `docker cat` approach to analyzing logs is just one example of many possible approaches. Other log handling practices may be more compliant or more in line with current best practices.

If you want to work with this raw log data, I highly recommend [Christian Folini's set of aliases](https://github.com/Apache-Labor/labor/blob/master/bin/.apache-modsec.alias) and the [tutorial on how to use them](https://www.netnea.com/cms/apache-tutorial-8_handling-false-positives-modsecurity-core-rule-set/).

## CRS Tuning

Despite the fact that false positives have been massively reduced with CRS version 3.0, false positives can still occur. This means we may need to tune the ModSecurity CRS to partially disable a CRS rule. There are very good tutorials written by Christian Folini on [How to tune ModSecurity and CRS](https://www.netnea.com/cms/apache-tutorial-8_handling-false-positives-modsecurity-core-rule-set/).

The session Cookie for the Pixi application leads to exactly such false positives. The CRS tuning rules would look like this:

```
# Disable rules for request cookie: session:
# 942420 (Restricted SQL Character Anomaly Detection (cookies): # of special characters exceeded (8)
# 942440 (SQL Comment Sequence Detected.)
SecRuleUpdateTargetById 942420 "!REQUEST_COOKIES:session"
SecRuleUpdateTargetById 942440 "!REQUEST_COOKIES:session"
```

This ModSecurity CRS tuning will disable SQLi rules 942420 and 942440 for the Cookie `session`.

But how do we do that with our CRS Docker?

There are currently two ways tune ModSecurity CRS in a container:

- First, `docker create` the CRS container, then copy the CRS tuning into the container and start the container.
- Mount the CRS tuning into the container during the `docker run` command

Either way, we need to create a file named REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf or RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf, depending on the type of CRS tuning. For more information about where your tuning rules belong, see the current example files at [REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example) or [RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example).

```sh
docker create -dti \
  --name apachecrsrp \
  --env PARANOIA=1 \
  --env ANOMALYIN=5 \
  --env ANOMALYOUT=5 \
  --env ALLOWED_METHODS="GET POST" \
  --env MAX_FILE_SIZE=5242880 \
  --env RESTRICTED_EXTENSIONS=".conf/" \
  --env PORT=8001 \
  --publish 192.168.1.129:8001:8001 \
  --env BACKEND=http://192.168.1.129:8000 \
  franbuehler/modsecurity-crs-rp
```

Then we copy the CRS tuning file into the container:

```sh
docker cp RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf /etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
```

And we start the container:

```sh
docker start apachecrsrp
```

Don't forget to check this file into your repository as it is now an important part of your container configuration.

In CI pipelines, it is sometimes not possible to work with volumes. You will need to use this 'create - cp - start' approach there.

The second option is to add CRS tuning with a Docker volume. 

```sh
docker run -dti \
--name apachecrsrp \
--env PARANOIA=1 \
--env ANOMALYIN=5 \
--env ANOMALYOUT=5 \
--env ALLOWED_METHODS="GET POST" \
--env MAX_FILE_SIZE=5242880 \
--env RESTRICTED_EXTENSIONS=".conf/" \
--env PORT=8001 \
--publish 8001:8001 \
--env BACKEND=http://192.168.1.129:8000 \
--volume /path/to/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf:/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf \
franbuehler/modsecurity-crs-rp</span>
```

Franziska plans to transfer her CRS container to the official OWASP CRS container soon.

## Bonus: Docker-Compose

Under <https://github.com/franbuehler/modsecurity-crs-rp/blob/v3.1/docker-compose.yaml> you find a docker-compose.yaml filled with all possible environment variables and even the possibility for ModSecurity CRS tuning via volumes.

This file can be customized and starting up and stopping is even easier.

## CRS in DevOps

With this easy way to start the CRS, we can go even further and integrate it in a CI/CD pipeline. The ideas behind this shift-left approach and early testing of the WAF are described in a [new blog post]({{< ref "2018-06-19-the-core-rule-set-as-part-of-devops-ci-pipeline.md" >}}).

## CRS Container in Action

If you want to see this CRS container in action, check out Christian Folini's [asciinema video](https://asciinema.org/a/0JDnaO1Wi42sIYpgJzoYbCdtn).

And many thanks to Christian for reviewing this blog post.
