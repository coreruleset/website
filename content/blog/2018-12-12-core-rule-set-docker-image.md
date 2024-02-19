---
author: Franziska Buehler
categories:
  - Blog
date: '2018-12-12T10:27:37+01:00'
guid: https://coreruleset.org/?p=873
id: 873
permalink: /20181212/core-rule-set-docker-image/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: Core Rule Set Docker Image
url: /2018/12/12/core-rule-set-docker-image/
---


<span class="s1">The Core Rule Set is installed in just four steps, as described in the [Installation Guide](https://coreruleset.org/installation/).</span>

<span class="s1">Now, it's even easier using the CRS Docker container. The effort to start the CRS in front of an application is reduced to a few seconds and only one command.</span>

<span class="s1">Franziska Bühler, one of the CRS developers, enhanced the [official CRS container](https://hub.docker.com/r/owasp/modsecurity-crs/). Various CRS variables and the backend application to be protected can be configured using <https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/>.</span>

## <span class="s1">Vulnerable Web Application</span>

<span class="s1">For this blog post, we use the intentionally vulnerable web application Pixi from the [OWASP project DevSlop](https://devslop.co/). DevSlop is an open source project in which Tanya Janca, Nicole Becher and Franziska Bühler explore DevSecOps through writing vulnerable apps, creating pipelines, publishing proof of concepts, and documenting what they have learned on their [YouTube Channel](https://aka.ms/DevSlopShow) and blogs.</span>

<span class="s1">One of the application vulnerabilities is that the search field is vulnerable to reflected XSS attacks:</span>

![](/images/2018/12/Pixi_XSS-1024x739.png)

<span class="s1">Oops... The injected content is reflected back to the user.</span>

<span class="s1">This is one example.</span>

<span class="s1">Another misbehaviour of the application is that the secret key is stored in a publicly accessible server.conf file:</span>

![](/images/2018/12/Pixi_serverconf-1024x739.png)

<span class="s1">These are just two examples of this vulnerable web application. One is a classic XSS attack and one is a misconfiguration of the application that results in sensitive data exposure.</span>

<span class="s1">The Pixi application has even [more vulnerabilities](http://prezo.s3.amazonaws.com/pixi_california_2018/pixi_lab.md) to demonstrate. Franziska plans to write about it in another blog post and to show how the CRS makes these vulnerabilities unexploitable.</span>

<span class="s1">Of course, these vulnerabilities should be fixed in the application itself. But in the real world, it is not always possible to patch the vulnerabilities within a reasonable timeframe. Or sometimes, we simply have no control over the application software. And this is where the CRS comes in...</span>

<span class="s1">The CRS prevents the exploitation of the two attacks described above. The CRS is not a substitute for patching the software, but an additional layer of defence, a safety net in front of your application, protecting you from these attacks: CRS is the 1st line of defense!  
</span>

## <span class="s1">Start CRS in container</span>

<span class="s1">The Core Rule Set can protect you against vulnerabilities and application security risks, such as those described by the OWASP Top 10.</span>

<span class="s1">This means that our attacks executed in the example above should be blocked by the CRS.</span>

<span class="s1">But first, we have to start the CRS in front of the application. Let's do this in a really easy and straightforward way, in a Docker container:</span>

```
<pre class="p1" style="padding-left: 30px"><span class="s1">docker run -dti \
</span><span class="s1">--name apachecrsrp \
</span><span class="s1">--env PARANOIA=1 \
</span><span class="s1">--env ANOMALYIN=5 \
</span><span class="s1">--env ANOMALYOUT=5 \
</span><span class="s1">--env ALLOWED_METHODS="GET POST" \
</span><span class="s1">--env MAX_FILE_SIZE=5242880 \
</span><span class="s1">--env RESTRICTED_EXTENSIONS=".conf/" \
</span><span class="s1">--env PORT=8001 \
</span><span class="s1">--publish 8001:8001 \
</span><span class="s1">--env BACKEND=http://192.168.1.129:8000 \
</span><span class="s1">franbuehler/modsecurity-crs-rp</span>
```

<span class="s1">Fore more `docker run` examples and a complete list of possible environment variables, visit <https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/>. </span><span class="s1">This blog post only covers a brief selection of them.</span>

<span class="s1">The documentation of the CRS variables can be found in the current crs-setup.conf.example. At the time of this writing, this is <https://github.com/coreruleset/coreruleset/blob/v3.2/dev/crs-setup.conf.example>.</span>

<span class="s1">Let's have a look what we do in the `docker run` command above:  
</span><span class="s1">We start our CRS container with a paranoia\_level of 1, an inbound\_anomaly\_score\_threshold of 5 and an outbound\_anomaly\_score\_threshold of 5. These are internal configuration variables of the CRS that we configure here on the command line. Our values are mostly default values, but f</span><span class="s1">or the sake of clarity, we will do it anyway.  
</span><span class="s1">Then we tell the CRS to allow only GET and POST methods by setting the tx.allowed\_methods CRS variable.  
</span><span class="s1">The application allows for uploading images. We don't want to allow pictures larger than 5 MB. We achieve this by setting the tx.max\_file\_size variable to 5,242,880 bytes.  
</span><span class="s1">As our application leaks sensitive information in a .conf file, we forbid access to this file extension. The default value of restricted\_extensions is a long list of extensions that already contains .conf. Nevertheless, we explicitly set the value .conf for this blog post, as an example. But it's absolutely ok to not touch this value and to let the default value with numerous extensions take effect.  
</span><span class="s1">The listening port 8001 of the Apache Reverse Proxy can be set using the Docker environment variable PORT. This means the Apache inside the Docker container will run under the port 8001.  
</span><span class="s1">We also either need to use port mapping `--port 8001:8001` or make this listening port available on the Docker host with `--expose`. In some CI/CD environments, port mapping can not be used. Instead, we would then use `--expose`.  
</span><span class="s1">But here, we map port 8001 from inside the container to port 8001 on our Docker host. Apache, with the Core Rule Set, can thus be called under port 8001 on the Docker host. [CIS Docker Benchmark](https://www.cisecurity.org/cis-benchmarks/) recommends ensuring that container ports are not mapped to host port numbers below 1024.  
</span><span class="s1">Instead of mapping every interface (0.0.0.0) with `--publish 8001:8001` we could also use an explicit IP address here. That would be more secure, especially on productive systems.  
</span><span class="s1">The backend application listens on the IP address 192.168.1.129 and on port 8000. This can be configured with the Docker environment variable BACKEND=http://192.168.1.129:8000. We can not use the localhosts IP address 127.0.0.1 here, but the real IP address of the application because this localhost would be inside the container and can not be use to address the application outside the container.</span>

<span class="s1">With `docker ps` we test if our CRS container is up and running:</span>

```
<pre class="p1" style="padding-left: 30px"><span class="s1">$ docker ps</span>

<span class="s1">CONTAINER ID<span class="Apple-converted-space">        </span>IMAGE <span class="Apple-converted-space">                                </span>COMMAND<span class="Apple-converted-space">                  </span>CREATED <span class="Apple-converted-space">            </span>STATUS<span class="Apple-converted-space">              </span>PORTS<span class="Apple-converted-space">                                                </span>NAMES</span>

<span class="s1">68ecd59b1a51<span class="Apple-converted-space">        </span>franbuehler/modsecurity-crs-rp      <span class="Apple-converted-space">  </span>"/docker-entrypoint.…" <span class="Apple-converted-space">  </span>4 seconds ago <span class="Apple-converted-space">      </span>Up 3 seconds<span class="Apple-converted-space">        </span>80/tcp, 0.0.0.0:8001->8001/tcp <span class="Apple-converted-space">                      </span>apachecrsrp</span>
```

<span class="s1">We want to repeat our first XSS attack now and see if CRS blocks it, and we hope it does!</span>

<span class="s1">We now call the TCP port 8001 of the CRS container:</span>

![](/images/2018/12/CRS_XSS-1024x739.png)

<span class="s1">The attack can no longer be executed. We get a 403-forbidden status code. That's what we expected.</span>

<span class="s1">But what happened inside the CRS Docker container? We want to examine the error.log.</span>

<span class="s1">We `cat` the error.log from the CRS Docker container. Of course, we could also work with Docker volumes, the command `docker cp apachecrsrp:/var/log/apache2/error.log .` or Splunk drivers here. But for our example we do it with `cat`:</span>

```
<pre class="p2" style="padding-left: 30px"><span class="s1">docker exec -ti apachecrsrp cat /var/log/apache2/error.log</span>
```

<span class="s1">error.log:</span>

<span class="s1">\[2018-11-30 15:01:39.039585\] \[-:error\] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU \[client 172.17.0.1\] ModSecurity: Warning. detected XSS using libinjection. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"\] \[line "60"\] \[id "941100"\] \[msg "XSS Attack Detected via libinjection"\] \[data "Matched Data: XSS data found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"\] \[severity "CRITICAL"\] \[ver "OWASP\_CRS/3.0.0"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-xss"\] \[tag "OWASP\_CRS/WEB\_ATTACK/XSS"\] \[tag "WASCTC/WASC-8"\] \[tag "WASCTC/WASC-22"\] \[tag "OWASP\_TOP\_10/A3"\] \[tag "OWASP\_AppSensor/IE1"\] \[tag "CAPEC-242"\] \[hostname "localhost"\] \[uri "/search/"\] \[unique\_id "W-6t05raviJ3p3xEdXWl4AAAAMU"\]</span>

<span class="s1">\[2018-11-30 15:01:39.039716\] \[-:error\] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU \[client 172.17.0.1\] ModSecurity: Warning. Pattern match "(?i)\[&lt;\\\\xef\\\\xbc\\\\x9c\]script\[^&gt;\\\\xef\\\\xbc\\\\x9e\]\*\[&gt;\\\\xef\\\\xbc\\\\x9e\]\[\\\\\\\\s\\\\\\\\S\]\*?" at ARGS:query. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"\] \[line "92"\] \[id "941110"\] \[msg "XSS Filter - Category 1: Script Tag Vector"\] \[data "Matched Data: &lt;script&gt; found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"\] \[severity "CRITICAL"\] \[ver "OWASP\_CRS/3.0.0"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-xss"\] \[tag "OWASP\_CRS/WEB\_ATTACK/XSS"\] \[tag "WASCTC/WASC-8"\] \[tag "WASCTC/WASC-22"\] \[tag "OWASP\_TOP\_10/A3"\] \[tag "OWASP\_AppSensor/IE1"\] \[tag "CAPEC-242"\] \[hostname "localhost"\] \[uri "/search/"\] \[unique\_id "W-6t05raviJ3p3xEdXWl4AAAAMU"\]</span>

<span class="s1">\[2018-11-30 15:01:39.040062\] \[-:error\] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU \[client 172.17.0.1\] ModSecurity: Warning. Pattern match "(?i)&lt;\[^\\\\\\\\w&lt;&gt;\]\*(?:\[^&lt;&gt;\\\\"'\\\\\\\\s\]\*:)?\[^\\\\\\\\w&lt;&gt;\]\*(?:\\\\\\\\W\*?s\\\\\\\\W\*?c\\\\\\\\W\*?r\\\\\\\\W\*?i\\\\\\\\W\*?p\\\\\\\\W\*?t|\\\\\\\\W\*?f\\\\\\\\W\*?o\\\\\\\\W\*?r\\\\\\\\W\*?m|\\\\\\\\W\*?s\\\\\\\\W\*?t\\\\\\\\W\*?y\\\\\\\\W\*?l\\\\\\\\W\*?e|\\\\\\\\W\*?s\\\\\\\\W\*?v\\\\\\\\W\*?g|\\\\\\\\W\*?m\\\\\\\\W\*?a\\\\\\\\W\*?r\\\\\\\\W\*?q\\\\\\\\W\*?u\\\\\\\\W\*?e\\\\\\\\W\*?e|(?:\\\\\\\\W\*?l\\\\\\\\W\*?i\\\\\\\\W\*?n\\\\\\\\W\*?k|\\\\\\\\W\*?o\\\\\\\\W\*?b\\\\\\\\W\*?j\\\\\\\\W\*?e\\\\ ..." at ARGS:query. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf"\] \[line "217"\] \[id "941160"\] \[msg "NoScript XSS InjectionChecker: HTML Injection"\] \[data "Matched Data: &lt;script found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"\] \[severity "CRITICAL"\] \[ver "OWASP\_CRS/3.0.0"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-xss"\] \[tag "OWASP\_CRS/WEB\_ATTACK/XSS"\] \[tag "WASCTC/WASC-8"\] \[tag "WASCTC/WASC-22"\] \[tag "OWASP\_TOP\_10/A3"\] \[tag "OWASP\_AppSensor/IE1"\] \[tag "CAPEC-242"\] \[hostname "localhost"\] \[uri "/search/"\] \[unique\_id "W-6t05raviJ3p3xEdXWl4AAAAMU"\]</span>

<span class="s1">\[2018-11-30 15:01:39.041614\] \[-:error\] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU \[client 172.17.0.1\] ModSecurity: Access denied with code 403 (phase 2). Operator GE matched 5 at TX:anomaly\_score. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf"\] \[line "93"\] \[id "949110"\] \[msg "Inbound Anomaly Score Exceeded (Total Score: 15)"\] \[severity "CRITICAL"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-generic"\] \[hostname "localhost"\] \[uri "/search/"\] \[unique\_id "W-6t05raviJ3p3xEdXWl4AAAAMU"\]</span>

<span class="s1">\[2018-11-28 15:01:39.042530\] \[-:error\] 172.17.0.1:39792 W-6t05raviJ3p3xEdXWl4AAAAMU \[client 172.17.0.1\] ModSecurity: Warning. Operator GE matched 5 at TX:inbound\_anomaly\_score. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-980-CORRELATION.conf"\] \[line "86"\] \[id "980130"\] \[msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 15 - SQLI=0,XSS=15,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): NoScript XSS InjectionChecker: HTML Injection; individual paranoia level scores: 15, 0, 0, 0"\] \[tag "event-correlation"\] \[hostname "localhost"\] \[uri "/error/403.html"\] \[unique\_id "W-6t05raviJ3p3xEdXWl4AAAAMU"\]</span>

<span class="s1">Three different CRS rules detected the XSS attack:</span>

- <span class="s1">In CRS rule 941100, libinjection says: "XSS data found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;".</span>
- Rule 941110 detects "Matched Data: &lt;script&gt; found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;".
- Rule 941160 complains about the script tag: "Matched Data: &lt;script found within ARGS:query: &lt;script&gt;alert('hi')&lt;/script&gt;"

<span class="s1">These three violated rules result in a total Inbound Anomaly Score of 15, which is higher than our configured Inbound Anomaly Score Threshold of 5. We see this in the request blocking evaluation rule 949110 or with detail values of each paranoia level in rule 980130.</span>

<span class="s1">We also check what happened to the blocked .conf file. This request can no longer be executed:</span>

![](/images/2018/12/CRS_serverconf-1024x739.png)

<span class="s1">The corresponding log entries can be found here:</span>

<span class="s1">\[2018-11-30 15:21:53.786966\] \[-:error\] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE \[client 172.17.0.1\] ModSecurity: Warning. String match within ".conf/" at TX:extension. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf"\] \[line "1069"\] \[id "920440"\] \[msg "URL file extension is restricted by policy"\] \[data ".conf"\] \[severity "CRITICAL"\] \[ver "OWASP\_CRS/3.0.0"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-protocol"\] \[tag "OWASP\_CRS/POLICY/EXT\_RESTRICTED"\] \[tag "WASCTC/WASC-15"\] \[tag "OWASP\_TOP\_10/A7"\] \[tag "PCI/6.5.10"\] \[hostname "localhost"\] \[uri "/server.conf"\] \[unique\_id "W-6ykartDdny6dEbaKB05gAAAJE"\]</span>

<span class="s1">\[2018-11-30 15:21:53.791227\] \[-:error\] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE \[client 172.17.0.1\] ModSecurity: Access denied with code 403 (phase 2). Operator GE matched 5 at TX:anomaly\_score. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf"\] \[line "93"\] \[id "949110"\] \[msg "Inbound Anomaly Score Exceeded (Total Score: 5)"\] \[severity "CRITICAL"\] \[tag "application-multi"\] \[tag "language-multi"\] \[tag "platform-multi"\] \[tag "attack-generic"\] \[hostname "localhost"\] \[uri "/server.conf"\] \[unique\_id "W-6ykartDdny6dEbaKB05gAAAJE"\]</span>

<span class="s1">\[2018-11-30 15:21:53.792642\] \[-:error\] 172.17.0.1:39830 W-6ykartDdny6dEbaKB05gAAAJE \[client 172.17.0.1\] ModSecurity: Warning. Operator GE matched 5 at TX:inbound\_anomaly\_score. \[file "/etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-980-CORRELATION.conf"\] \[line "86"\] \[id "980130"\] \[msg "Inbound Anomaly Score Exceeded (Total Inbound Score: 5 - SQLI=0,XSS=0,RFI=0,LFI=0,RCE=0,PHPI=0,HTTP=0,SESS=0): URL file extension is restricted by policy; individual paranoia level scores: 5, 0, 0, 0"\] \[tag "event-correlation"\] \[hostname "localhost"\] \[uri "/error/403.html"\] \[unique\_id "W-6ykartDdny6dEbaKB05gAAAJE"\]</span>

- <span class="s1">CRS rule 920440 now states that our configured file extension .conf is not allowed: \[msg "URL file extension is restricted by policy"\] \[data ".conf"\]</span>
- In rule 949110, we see that the request was blocked because of the too high Inbound Anomaly Score of 5. And in rule 980130 we see again the details.

<span class="s1">As mentioned earlier, this `docker cat` approach to analyzing logs is just one example of many possible approaches. Other log handling practices may be more compliant or more in line with current best practices.</span>

<span class="s1">If you want to work with this raw log data, I highly recommend [Christian Folini's set of aliases](https://github.com/Apache-Labor/labor/blob/master/bin/.apache-modsec.alias) and the [tutorial on how to use them](https://www.netnea.com/cms/apache-tutorial-8_handling-false-positives-modsecurity-core-rule-set/).</span>

## <span class="s1">CRS Tuning</span>

<span class="s1">Despite the fact that false positives have been massively reduced with CRS version 3.0, false positives can still occur. This means we may need to tune the ModSecurity CRS to partially disable a CRS rule. There are very good tutorials written by Christian Folini on [How to tune ModSecurity and CRS](https://www.netnea.com/cms/apache-tutorial-8_handling-false-positives-modsecurity-core-rule-set/).</span>

<span class="s1">The session Cookie for the Pixi application leads to exactly such false positives. The CRS tuning rules would look like this:</span>

```
<pre class="p1" style="padding-left: 30px"><span class="s1"># Disable rules for request cookie: session:
</span><span class="s1"># 942420 (Restricted SQL Character Anomaly Detection (cookies): # of special characters exceeded (8)
</span><span class="s1"># 942440 (SQL Comment Sequence Detected.)
</span><span class="s1">SecRuleUpdateTargetById 942420 "!REQUEST_COOKIES:session"
</span><span class="s1">SecRuleUpdateTargetById 942440 "!REQUEST_COOKIES:session"</span>
```

<span class="s1">This ModSecurity CRS tuning will disable SQLi rules 942420 and 942440 for the Cookie `session`.</span>

<span class="s1">But how do we do that with our CRS Docker?</span>

<span class="s1">There are currently two ways tune ModSecurity CRS in a container:</span>

- <span class="s1">First, `docker create` the CRS container, then copy the CRS tuning into the container and start the container.</span>
- Mount the CRS tuning into the container during the `docker run` command

<span class="s1">Either way, we need to create a file named REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf or RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf, depending on the type of CRS tuning. For more information about where your tuning rules belong, see the current example files at [REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example) or [RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example).</span>

```
<pre class="p1" style="padding-left: 30px"><span class="s1">docker create -dti \
</span><span class="s1"><span class="Apple-converted-space">  </span>--name apachecrsrp \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env PARANOIA=1 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env ANOMALYIN=5 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env ANOMALYOUT=5 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env ALLOWED_METHODS="GET POST" \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env MAX_FILE_SIZE=5242880 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env RESTRICTED_EXTENSIONS=".conf/" \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env PORT=8001 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--publish 192.168.1.129:8001:8001 \
</span><span class="s1"><span class="Apple-converted-space">  </span>--env BACKEND=http://192.168.1.129:8000 \
</span><span class="s1">  franbuehler/modsecurity-crs-rp</span>
```

Then we copy the CRS tuning file into the container:

```
<pre class="p1" style="padding-left: 30px"><span class="s1">docker cp RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf /etc/apache2/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf</span>
```

And we start the container:

```
<pre class="p1" style="padding-left: 30px"><span class="s1">docker start apachecrsrp</span>
```

<span class="s1">Don't forget to check this file into your repository as it is now an important part of your container configuration.</span>

<span class="s1">In CI pipelines, it is sometimes not possible to work with volumes. You will need to use this 'create - cp - start' approach there.</span>

<span class="s1">The second option is to add CRS tuning with a Docker volume. </span>

```
<pre class="p1" style="padding-left: 30px"><span class="s1">docker run -dti \
</span><span class="s1">--name apachecrsrp \
</span><span class="s1">--env PARANOIA=1 \
</span><span class="s1">--env ANOMALYIN=5 \
</span><span class="s1">--env ANOMALYOUT=5 \
</span><span class="s1">--env ALLOWED_METHODS="GET POST" \
</span><span class="s1">--env MAX_FILE_SIZE=5242880 \
</span><span class="s1">--env RESTRICTED_EXTENSIONS=".conf/" \
</span><span class="s1">--env PORT=8001 \
</span><span class="s1">--publish 8001:8001 \
</span><span class="s1">--env BACKEND=http://192.168.1.129:8000 \
--volume /path/to/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf:/etc/apache2/modsecurity.d/owasp-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf \
franbuehler/modsecurity-crs-rp</span>
```

<span class="s1">Franziska plans to transfer her CRS container to the official OWASP CRS container soon.</span>

## <span class="s1">Bonus: Docker-Compose</span>

<span class="s1">Under <https://github.com/franbuehler/modsecurity-crs-rp/blob/v3.1/docker-compose.yaml> you find a docker-compose.yaml filled with all possible environment variables and even the possibility for ModSecurity CRS tuning via volumes.</span>

<span class="s1">This file can be customized and starting up and stopping is even easier.</span>

## <span class="s1">CRS in DevOps</span>

<span class="s1">With this easy way to start the CRS, we can go even further and integrate it in a CI/CD pipeline. The ideas behind this shift-left approach and early testing of the WAF are described in a blog post at [https://coreruleset.org](https://coreruleset.org/20180619/the-core-rule-set-as-part-of-devops-ci-pipeline/).</span>

## <span class="s1">CRS Container in Action</span>

<span class="s1">If you want to see this CRS container in action, check out Christian Folini's asciinema video at: <https://asciinema.org/a/0JDnaO1Wi42sIYpgJzoYbCdtn>.</span>

And many thanks to Christian for reviewing this blog post.

- - - - - -