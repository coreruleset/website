---
author: Franziska Buehler
categories:
  - Blog
date: '2018-06-19T09:13:14+02:00'
guid: https://coreruleset.org/?p=701
id: 701
permalink: /20180619/the-core-rule-set-as-part-of-devops-ci-pipeline/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: The Core Rule Set as Part of DevOps (CI pipeline)
url: /2018/06/19/the-core-rule-set-as-part-of-devops-ci-pipeline/
---


<span class="s1">A Web Application Firewall (WAF) raises concerns that it does not fit into the DevOps methodology. </span><span class="s1">The problem is that when a WAF is added to production, the impact on the application is tested too late. The application developer gets extremely late feedback and the WAF could break the application. This can lead to production issues.</span>

<span class="s1">But what if a WAF is involved in the DevOps process very early on and not just at the end, at production?</span>

<span class="s1">The whole DevOps process only makes sense when all components are part of it! A service can only be successfully complemented by a WAF if the WAF is part of the pipeline from the beginning. </span><span class="s1">I will show how to integrate a WAF, specifically ModSecurity with the Core Rule Set, and its testing into continuous integration.</span>

<span class="s1">My three main goals are:</span>

- <span class="s1">To spread the word about the Core Rule Set (CRS)</span>
- To take the fear of WAFs
- To get WAFs involved in DevOps

### <span class="s1">Problem</span>

<span class="s1">Despite the fact that the number of false positives has been massively reduced in CRS3, there is still the possibility that legitimate traffic from a legitimate user might trigger a CRS rule. This means the user receives a '403 - Forbidden' message and can't use the application. She gets blocked. </span>

<span class="s1">This problem is even worse in a DevOps culture. Everything is fully automated and well-tested and in the end, we add a WAF to production and kill the whole positive experience: When production issues arise, it is often too late to find and correct the problems. </span><span class="s1">Instead, an operator is likely to disable the WAF and never re-enable it again. This is because operators have a lot of other work to do and security is not always the top priority.</span>

### <span class="s1">Solution</span>

<span class="s1">The solution is to insert the WAF / CRS very early in the DevOps process and give the developers and operators early feedback:</span>

- <span class="s1">If we automate application tests, we must add the CRS to these tests. All tests have to succeed first without, then with the CRS! Additionally, no CRS rule should be triggered by the tests.</span>
- Each commit of the application code into the repository triggers a continuous integration run. This launches the application, starts the WAF and runs the application tests.  
    We are thus testing an application with the CRS after every commit of the code.
- We always want to have the application in a deployable and runnable state with the CRS.  
    This way, we know that our current app version's traffic is not blocked by the CRS.
- We guarantee this by testing the application and the CRS in a production-like environment. There can always be false positives. We can remove them by tuning the rules via the configuration.  
    If we have to perform these adjustments to the CRS, we already have our configuration for production because we tested it in a production-like environment.
- The application should not go to release until it is fully tested with the CRS!  
    An application whose legitimate traffic triggers a rule should not go into production until the error is fixed either. With every false positive, we need to decide if it is something we can fix in the application, or if the CRS needs to be tuned.

<span class="s1">This way, the application's traffic is tested with the CRS and we don't have to fear production issues later on.  
</span>

### <span class="s1">CRS Docker Container</span>

<span class="s1">As you can read at <https://coreruleset.org/installation>, it only takes a few steps to install the Core Rule Set. </span><span class="s1">And it gets even easier if you use it in a Docker Container.</span>

<span class="s1">I have created a Docker Image that inherits from the official OWASP ModSecurity Core Rule Set Container (<https://hub.docker.com/r/owasp/modsecurity-crs/>). My image adds an Apache reverse proxy configuration. The reverse proxy configuration is used to put the CRS in front of an application. It also adds some more CRS variables. The CRS container can be found at <https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/>. </span><span class="s1">This way, the CRS can be very quickly and easily integrated into automated tests.</span>

<span class="s1">A special feature of my Docker Container is that it returns the [UNIQUE\_ID](https://httpd.apache.org/docs/2.4/mod/mod_unique_id.html) of a blocked request in the 403.html error page. I plan to match this UNIQUE\_ID with the application tests in the future.</span>

<span class="s1">Here is how to run the container:</span>

`docker run -dt --name apachecrsrp -e PARANOIA=1 -e \<br></br>ANOMALYIN=5 -e ANOMALYOUT=4 -e BACKEND=http://172.17.0.1:8000 \<br></br>-e PORT=8001 --expose 8001 franbuehler/modsecurity-crs-rp<br></br>`

<span class="s1">The following environment variables are configurable:</span>

- <span class="s1">`PARANOIA`: paranoia\_level</span>
- `ANOMALYIN`<span style="font-size: 16px">: inbound\_anomaly\_score\_threshold</span>
- `ANOMALYOUT`<span style="font-size: 16px">: outbound\_anomaly\_score\_threshold</span>
- `BACKEND`<span style="font-size: 16px">: IP address and TCP port of application backend</span>
- `PORT`<span style="font-size: 16px">: listening TCP port of Apache, this port must also be exposed: `--expose`</span>

<span class="s1">Explanations of the individual parameters can be found in the main CRS configuration file crs-setup.conf (current version: <https://github.com/coreruleset/coreruleset/blob/v3.0/master/crs-setup.conf.example>) or as part of the tutorial series about ModSecurity and CRS at [netnea](https://netnea.com/apache-tutorials).</span>

### <span class="s1">Proof of Concept Setup</span>

<span class="s1">I have implemented a proof of concept in CircleCI. Of course, the continuous integration can also be implemented on TravisCI, Jenkins, and so on. Then </span><span class="s1">I used TestCafe to write the application tests. It's a Node.js tool for performing end-to-end tests.</span>

<span class="s1">In the basic setup, we have application tests that are performed against the application. Naturally, these application tests should succeed:</span>

![](/images/2018/06/Setup1-1024x640.png)

<span class="s1">As a next step, we put CRS in front of the same application in order to funnel the same tests through the WAF. </span><span class="s1">We expect the application tests to still succeed and the log to remain empty. This would confirm that no CRS rule were triggered by the tests.</span>

![](/images/2018/06/Setup2-1024x640.png)

<span class="s1">Each of these components runs in a separate Docker container.</span>

<span class="s1">The time taken to pull and start the Core Rule Set container and to run the application tests are only a small part (approx. 1 minute and 30 seconds in this PoC) of the overall testing process (approx. 3 minutes and 30 seconds in my example). </span>

<span class="s1">The message here is: We do not waste a lot of time but get a lot of extra security.</span>

![](/images/2018/06/circleci_output.png)


### <span class="s1">CI Configuration</span>

<span class="s1">In summary, the CircleCI configuration .circleci/config.yml consists of the following steps:</span>

<span class="s1">`# .circleci/config.yml<br></br>`</span><span class="s1">`version: 2<br></br>`</span><span class="s1">`jobs:<br></br>`</span><span class="s1">`   build:<br></br>`</span><span class="s1">`      docker:`</span>  
<span class="s1">`         - image: circleci/node:9.11.1-stretch`</span>  
<span class="s1">`      steps:<br></br>`</span><span class="s1">`          -run:<br></br>`</span><span class="s1">`             name: Install dependencies<br></br>`</span><span class="s1">`             ...<br></br>`</span><span class="s1">`         -run<br></br>`</span><span class="s1">`             name: Install Docker Compose<br></br>`</span><span class="s1">`             ...<br></br>`</span><span class="s1">`         -setup_remote_docker<br></br>`</span><span class="s1">`         -checkout<br></br>`</span><span class="s1">`         -run:<br></br>`</span><span class="s1">`             name: Start App Container<br></br>`</span><span class="s1">`             ...<br></br>`</span><span class="s1">`         -run:<br></br>`</span><span class="s1">`             name: Start OWASP ModSecurity CRS Container in front of application for application tests<br></br>`</span><span class="s1">`             #http://172.17.0.2:8001<br></br>`</span><span class="s1">`             #we set inbound and outbound anomaly score to 1, no tolerance<br></br>`</span><span class="s1">`             command: |<br></br>`</span><span class="s1">`                docker pull franbuehler/modsecurity-crs-rp && \<br></br>`</span><span class="s1">`                docker run -dt --name apachecrstc -e PARANOIA=2 -e \<br></br>`</span><span class="s1">`                ANOMALYIN=1 -e ANOMALYOUT=1 -e BACKEND=http://172.17.0.1:8000 \<br></br>`</span><span class="s1">`                -e PORT=8001 --expose 8001 franbuehler/modsecurity-crs-rp<br></br>`</span><span class="s1">`         -run:<br></br>`</span><span class="s1">`             name: ModSecurity Tuning - Load rule exclusions<br></br>`</span><span class="s1">`             command: |<br></br>`</span><span class="s1">`                printf '# Rule 942450 (msg: SQL Hex Encoding Identified) triggers,\n' > tmp.conf<br></br>`</span><span class="s1">`                printf '# because of random characters in the session cookie.\n' >> tmp.conf<br></br>`</span><span class="s1">`                printf '\nSecRuleUpdateTargetById 942450 "!REQUEST_COOKIES:session"\n' >> tmp.conf<br></br>`</span><span class="s1">`                # CRS container for application tests:<br></br>`</span><span class="s1">`                docker cp tmp.conf apachecrstc:/etc/httpd/modsecurity.d/owasp-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf;<br></br>`</span><span class="s1">`                docker exec apachecrstc /usr/sbin/httpd -k graceful<br></br>`</span><span class="s1">`         - run:<br></br>`</span><span class="s1">`             name: Application Tests with Testcafe<br></br>`</span><span class="s1">`             command: |<br></br>`</span><span class="s1">`                # https://circleci.com/docs/2.0/building-docker-images/#mounting-folders<br></br>`</span><span class="s1">`                # creating dummy container which will hold a volume with config<br></br>`</span><span class="s1">`                docker create -v /tests --name configs alpine:latest /bin/true<br></br>`</span><span class="s1">`                # copying config file into this volume<br></br>`</span><span class="s1">`                docker cp /home/circleci/project/testcafe/tests/test.js configs:/tests<br></br>`</span><span class="s1">`                # starting application container using this volume<br></br>`</span><span class="s1">`                docker pull testcafe/testcafe<br></br>`</span><span class="s1">`                docker run --volumes-from configs:rw --name testcafe -it testcafe/testcafe 'chromium:headless --no-sandbox' /tests/test.js<br></br>`</span><span class="s1">`         - run:<br></br>`</span><span class="s1">`             name: Application Tests with CRS with Testcafe<br></br>`</span><span class="s1">`             command: |<br></br>`</span><span class="s1">`                docker cp /home/circleci/project/testcafe/tests/testcrs.js configs:/tests<br></br>`</span><span class="s1">`                docker run --volumes-from configs:rw --name testcafecrs -it testcafe/testcafe 'chromium:headless --no-sandbox' /tests/testcrs.js<br></br>`</span><span class="s1">`         - run:<br></br>`</span><span class="s1">`             # Fail if ModSecurity log is not empty<br></br>`</span><span class="s1">`             name: Show ModSecurity logs of Testcafe Tests<br></br>`</span><span class="s1">`             ...<br></br>`</span><span class="s1">`         - run:<br></br>`</span><span class="s1">`            # Fail if ModSecurity log does not contain WAF Test String "My evil WAF Test"<br></br>`</span><span class="s1">`            # '<script>alert("My evil WAF Test")</script>'<br></br>`</span><span class="s1">`            name: Search for WAF Test String "My evil WAF Test" in ModSecurity logs<br></br>`</span><span class="s1">`            ... `</span>

<span class="s1">For all details see: </span>

[<span class="s1">https://github.com/DevSlop/pixi-crs/blob/master/.circleci/config.yml</span>](https://github.com/DevSlop/pixi-crs/blob/master/.circleci/config.yml)

<span class="s1">Let's go through the steps and take a closer look:</span>

#### <span class="s1">Step "Spin up Environment"</span>

<span class="s1">First, we have to tell CircleCI which image to use for the primary Docker Container. That is where all of the following steps are performed.</span>

#### <span class="s1">Steps "Install dependencies", "Install Docker Compose" and "setup\_remote\_docker"</span>

<span class="s1">Then we want CircleCI to install some dependencies, docker-compose and docker.</span>

#### <span class="s1">Step "checkout"</span>

<span class="s1">The configuration .circleci/config.yml is in the root of the application repository. And in step 'checkout', CircleCI checks out the application code, where the .circleci/config.yml resides.</span>

#### <span class="s1">Step "Start App Container"</span>

<span class="s1">In the next step, we start the application in a container.</span>

#### <span class="s1">Step "Start OWASP ModSecurity CRS Container in front of application for application tests"</span>

<span class="s1">Then we start our CRS container in front of the application we have just started above.</span>

#### <span class="s1">Step "ModSecurity Tuning - Load rule exclusions"</span>

<span class="s1">In this step, we have the ability to tune the ModSecurity / CRS setup. We exclude certain rules or we hide certain parameters from the set of over 150 rules to avoid false positives and to keep the logfile empty.</span>

#### <span class="s1">Step "Application Tests with Testcafe"</span>

<span class="s1">Here, we perform the application tests against the TCP port of the application container. We do this to be sure that the application and the application tests are working. We want to distinguish failed application tests caused by the application itself from false positives introduced by CRS.</span>

#### <span class="s1">Step "Application Tests with CRS with Testcafe"</span>

<span class="s1">We repeat the application tests, but this time via the WAF / CRS. This is done by pointing the tests against the TCP port of the CRS container. Of course, these tests must be successful, too. </span><span class="s1">In addition to the existing application tests, we add a WAF test to be sure that the CRS really triggers: We send an Cross Site Scripting (XSS) payload to a search form and expect the CRS to block the attack.</span>

#### <span class="s1">Step "Show ModSecurity logs of Testcafe Tests"</span>

<span class="s1">In the end, we check the results: </span><span class="s1">The ModSecurity log should be empty. This means that no CRS rule was triggered by the standard application tests.  
</span>

#### <span class="s1">Step "Search for WAF Test String "My evil WAF Test" in ModSecurity logs</span>

<span class="s1">We also test that our intentionally added XSS string appears in the log. If it does not appear, either the tests have been aborted or the CRS did not work properly and we should look into this. </span>

<span class="s1">In the image above, we see a problem that should be resolved before the application can be released. </span><span class="s1">The message here is: If and when every step is successful and the application works behind the CRS, then the application can go into production!</span>

### <span class="s1">Recommendations for Production</span>

<span class="s1">This PoC covers the continuous integration part. But of course, it could be extended to an entire deployment pipeline.</span>

<span class="s1">To do all this in production, I recommend the following:</span>

- <span class="s1">The more tests you write, the better!  
    </span>But at least test your login process. I often see false positives in cookies and cookie names in production, if, for example, special characters or random strings are used.  
    Click through your entire application. Testing all GET and POST arguments covers a broad part of the application. I also often see problems there.  
    The broader the tests are, the better the chance to get all possible false positives caused by the application's legitimate traffic.
- Perform your tests during continuous integration with a very low inbound and outbound anomaly threshold.  
    We want to see and alert every false positive.
- If there are false positives in production (lack of tests?), then write a test for every issue discovered this way. This makes sure the false positives goes away.
- Each new feature of the application should be covered by a test. Of course, this should always be the case, but it's even more important with CRS in place.
- You will probably have to adapt the CRS Docker container to fit into your organization. My Docker container is an example of how it could be done (Think about adding SSL/TLS for example).

<span class="s1">Take the CI pipeline and the Docker container of this PoC and customize it for your organization. This PoC is meant to give you free samples of how to implement a pipeline with a WAF in it.</span>

### <span class="s1">Future work</span>

- <span class="s1">I plan to implement this pipeline on other continuous integration platforms, such as Jenkins, TravisCI, GitLab CI, and so forth to spread its use.</span>
- <span class="s1">As mentioned earlier, the CRS container already returns the UNIQUE\_ID of a blocked request in the 403.html error page. I plan to match this UNIQUE\_ID to the application test.</span>

### <span class="s1">Presentation and slides</span>

<span class="s1">I gave a presentation at the [DevOpsDays ZH](https://www.devopsdays.org/events/2018-zurich/program/franziska-buehler/), the [Open Cloud Day in Zurich](https://opencloudday.ch/wp-content/uploads/sites/6/2018/05/Franziska-Buehler_presentation_open_cloud_day.pdf), the [Open Security Summit in England](https://open-security-summit.org/tracks/devsecops/user-sessions/adding-crs3-pixi-to-circleci-pipeline/) and the [DevOps Meetup Bern](https://www.meetup.com/de-DE/DevOps-Bern/events/248088984/) where I explain this whole idea. </span><span class="s1">The slides can be found at <https://www.slideshare.net/franbuehler></span><span class="s1"> and the video from the DevOpsDays ZH can be found at <https://vimeo.com/271451246>.</span>

### <span class="s1">References</span>

<span class="s1">The backend application I tested in this PoC is the Pixi application from the [OWASP project DevSlop](http://devslop.co), where I am also a part of the team.  
</span><span class="s1">The OWASP DevSlop project consists of several modules, all aimed at either presenting proof-of-concept DevSecOps pipelines, or insecure implementations of DevOps to teach better practices.  
</span>[<span class="s1">http://devslop.co</span>](http://devslop.co)  
<span class="s1">[https://www.owasp.org/index.php/OWASP\_DevSlop\_Project](https://www.owasp.org/index.php/OWASP_DevSlop_Project) </span>

<span class="s1">The CircleCI configuration can be found on GitHub. Please take this example and customize it for your organization.  
</span>[<span class="s1">https://github.com/DevSlop/pixi-crs/blob/master/.circleci/config.yml</span>](https://github.com/DevSlop/pixi-crs/blob/master/.circleci/config.yml)

<span class="s1">My CRS Docker image can be found at:  
</span>[<span class="s1">https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/</span>](https://hub.docker.com/r/franbuehler/modsecurity-crs-rp/)

<span class="s1">Source:  
</span>[<span class="s1">https://github.com/franbuehler/modsecurity-crs-rp</span>](https://github.com/franbuehler/modsecurity-crs-rp)

<span class="s1">One of the triggers of the idea behind this blog post is the book 'Securing DevOps' by Julien Vehent:  
<https://www.manning.com/books/securing-devops>.</span>

<span class="s1">Of course, every CRS user knows the ModSecurity Guides from Christian Folini. They provide the basic knowledge to understand the concepts and inner working of CRS and ModSecurity:  
</span>[<span class="s1">https://netnea.com/apache-tutorials</span>](https://netnea.com/apache-tutorials).

Thanks Christian Folini for proofreading my blog post!

<div></div><div></div>![](/assets/uploads/2017/11/franziska_buehler-432x432.png) Franziska Buehler / [@bufrasch](https://twitter.com/bufrasch)