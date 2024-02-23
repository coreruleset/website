---
author: Christian Folini
categories:
  - Blog
date: '2020-01-14T08:12:50+01:00'
permalink: /20200114/crs-project-news-january-2020/
tags:
  - CRS-News
title: CRS Project News January 2020
url: /2020/01/14/crs-project-news-january-2020/
---


It's been a while since the last CRS project news. It's not because there was nothing to report. It's more like too much going on and no time to sit back and write it all down.  
  
Here are the most important things that happened since the last edition:

ModSecurity 3.0.4 has been released for NGINX. This is a security release covering a problem our project members @airween and @theMiddle have discovered. Trustwave has asked us to withhold any details for the moment, but the release of the full CVE is planned for next week. Packaging is under way as far as we can tell. If you are running ModSec3, then we strongly advise you to update ASAP and we'll probably follow up with a separate blog post once the details are published.  
Link: <https://sourceforge.net/p/mod-security/mailman/message/36899090/>

#### Announcements and News Coverage

- AWS is offering CRS as option in their Managed Rules offering <https://aws.amazon.com/blogs/aws/announcing-aws-managed-rules-for-aws-waf/>
- Gitlab uses CRS for their enterprise customers  
    <https://about.gitlab.com/2019/09/22/gitlab-12-3-released/#web-application-firewall-for-kubernetes-ingress>
    We have established contact with the GitLab engineering teamContact with their engineering team established. Planning to have regular talks.
- Midsized Swiss Bank Acrevis uses CRS; a setup engineered by our Franziska Bühler <https://www.netzwoche.ch/news/2019-11-11/open-source-in-der-bankenwelt>
- CRS has reached the certification level as a Best Practice <https://github.com/coreruleset/coreruleset/issues/502>
- We have generated a private key for the project and we will sign our releases from now on <https://coreruleset.org/security.asc>

#### Blog Posts, articles, tutorials and presentations:

- ModSecurity in Envoy (Kubernetes etc.): <https://medium.com/solo-io/5-minutes-with-gloo-web-application-firewalls-waf-in-api-gateways-160b5eaa1e95>
- Co-Lead Christian Folini presented at OWASP Global AppSec in Amsterdam 2019  
    <https://www.youtube.com/watch?v=ZbTmpJldwPY>   
    An extended version of this talk will be presented at OWASP AppSecCali in January 2020.
- Web Application Firewall (WAF) Evasion Techniques #3 <https://www.secjuice.com/web-application-firewall-waf-evasion/>
- [CRS on DevSlopPixi]({{< ref "blog/2019-09-09-how-the-crs-protects-the-vulnerable-web-application-pixi-by-owasp-devslop.md" >}}) by our Franziska Bühler 
    \\* <https://dev.to/devslop/devslop-s-pixi-crs-pipeline-4bie>
- The LiteSpeed team has done an extensive speed test covering the fast ModSecurity 2 on Apache and the slower ModSecurity 3 on Nginx (we knew about that). But it's impressive how their commercial webserver is really faster. <https://blog.litespeedtech.com/2019/12/02/modsecurity-performance-apache-nginx-litespeed>
- A presentation on ModSecurity and ELK <https://xeraa.net/talks/secure-your-code-injections-and-logging/>
- Dockerized setup of NGINX with ModSec and Brotli <https://medium.com/swlh/nginx-with-modsecurity-and-brotli-production-setup-dockerized-2d1407600415>
- Extensive introduction to CRS at the British Computer Society by project co-lead Christian Folini <https://de.slideshare.net/ChristianFolini/folini-extended-introduction-to-modsecurity-and-crs3>
- "Buying time against attack" - article in ITNow by co-lead Christian Folini <https://www.bcs.org/content-hub/buying-time-against-attack/>
- Franziska Bühler presented the use of CRS in DevOps environments at the German OWASP day in Karlsruhe <https://god.owasp.de/schedule/>  
    She will present a similar talk at the Configuration Management Camp in Belgium on Feb 4. <https://cfp.cfgmgmtcamp.be/2020/talk/8QQMP8/>
- Franziska also spoke on the Testguild podcast about the Core Rule Set project  
    <https://testguild.com/podcast/security/s04-franziska-buehler/>
- CRS project co-lead Chaim Sanders and Franziska had a session in the All-Day-DevOps event where they talked about Unit Testing within the CRS project - and about Unit Testing with the help of the CRS project  
    <https://play.vidyard.com/TkCgrXFjM2ntXrhM7rrGP6?>

#### Helper Scripts

- Trigger a certain CRS anomaly score on a target host. Exactly that score. <https://github.com/dune73/crs-trigger>
- Helper script to facilitate logging from ModSecurity / CRS to ELK by Philipp Krenn / @xeraa [https://github.com/xeraa/mod\_security-log](https://github.com/xeraa/mod_security-log)

*News assembled by Christian Folini, CRS Co-Lead.*
