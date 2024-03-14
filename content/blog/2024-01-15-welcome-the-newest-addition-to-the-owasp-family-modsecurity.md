---
author: dune73
categories:
  - Blog
date: '2024-01-15T13:32:16+01:00'
title: 'Welcome the newest addition to the OWASP family: ModSecurity!'
url: /2024/01/15/welcome-the-newest-addition-to-the-owasp-family-modsecurity/
---


With the new year comes good news: last week, Trustwave and the OWASP Foundation have announced the agreement to transfer ModSecurity to OWASP. The transition will commence on January 25. The incubation phase of the new OWASP ModSecurity project will focus on the establishment of a development community to lay the basis for a successful continuation of the project under the new stewardship. This entails the three areas: communication, administration and development. OWASP calls all interested parties to join hands and help with the future development of ModSecurity.

For the time being, the meeting point is the #project-modsecurity channel on the OWASP Slack. If you do not have an account, get one from <https://owasp.org/slack/invite>.

{{< figure src="images/2024/01/OWASP-logo.png" >}}With the transfer to OWASP, the uncertainty over ModSecurity's future, that has plagued the engine for some time now, has finally come to an end. "This landmark move promises to inject fresh energy and perspectives into the project, ensuring its continued evolution as a vital line of defense for countless websites worldwide," OWASP states in [a blog post](https://owasp.org/blog/2024/01/09/ModSecurity.html) announcing the agreement with Trustwave. As part of the OWASP family, ModSecurity is guaranteed to remain free to use and modify, ensuring its accessibility for organizations of all sizes.

What does this mean for the Core Rule Set project? Being the custodian of ModSecurity, Coraza as well as CRS, OWASP plans to steer ModSecurity's development with a holistic view, fostering even tighter integration between the Core Rule Set and the underlying ModSecurity and Coraza engines. This integration under one roof will further simplify the rule creation and testing process.

As for Coraza, the first WAF engine project to come under the OWASP umbrella, OWASP states the following: "Coordination with Coraza will guarantee that both engines implement the same rules language." This is of course very important for CRS and will keep future development more simple.

Juan-Pablo Tosso, the original author of OWASP Coraza, shared the following:

"While Coraza offers compatibility with ModSecurity's features, the reverse is not true. Our developmental trajectories have diverged, with Coraza adopting innovative approaches more aligned with contemporary community needs.

A key distinction is Coraza's inherent cloud-native architecture. Backed by the support of various companies and our dedicated development team, Coraza stands out as the sole open-source Web Application Firewall (WAF) natively compatible with WebAssembly (WASM)."

So Coraza sees a common ground, but emphasizes the different use cases for the two engines with the different profile. A useful distinction, from the perspective of CRS.

Under the line, it is very good that the anxiety about the future of ModSecurity is now gone and having the three projects under one roof will certainly simplify things going forward.

So welcome ModSecurity and good luck!
