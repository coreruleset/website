---
author: csanders-git
categories:
  - Blog
date: '2018-03-08T18:21:30+01:00'
title: Building the WAF test harness [x-post]
---


To help our customers secure their sites and applications — while continuing to give their users reliable online experiences — we’ve built a performant, highly configurable, and comprehensive Web Application Firewall (WAF). [In our last post](https://www.fastly.com/blog/building-fastly-waf), we shared some of the tech behind our WAF, including how we chose our ruleset and leverage our findings. In order to provide a fully comprehensive solution for securing your infrastructure, it’s critical to continuously test that solution. Because technology and threats are constantly evolving, the rulesets also need to evolve to ensure proper visibility and mitigation into emerging attacks methods.

In this post, we’ll share how we ensure a quality WAF implementation for our customers, continuously testing it using FTW, and go deeper into the findings and contributions we’ve made to the OWASP CRS community with FTW.
