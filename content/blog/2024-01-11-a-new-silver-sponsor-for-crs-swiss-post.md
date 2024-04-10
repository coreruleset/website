---
author: amonachesi
categories:
  - Blog
date: '2024-01-11T11:30:15+01:00'
title: 'A new silver sponsor for CRS: Swiss Post'
---


We are proud to present [Swiss Post](https://swisspost.ch) as new silver sponsor for the OWASP ModSecurity Core Rule Set. Swiss Post is one of the longest-standing and best-known brands in Switzerland since its establishment in 1849. The company uses many open-source solutions for development and operation and in turn supports the community where possible. Ties between Swiss Post and the CRS project team have traditionally been strong with different core team members having worked for the premier Swiss provider of mail and logistics services.

{{< figure src="images/2024/01/Post_Logo_digital_RGB.png" >}}

Swiss Post uses CRS as its primary web application firewall in a dedicated platform since 2012, when – in order to reduce operating costs and establish a lean infrastructure – a heterogeneous landscape was replaced with a landmark SecDevOps setup with ModSecurity and CRS at its heart. Since 2016, the Core Rule Set is also an important part of Swiss Post’s emerging online voting (e-voting) solution. Here, CRS is used in conjunction with ModSecurity for all four production and seven non-production environments.

The use of CRS has proven itself for Swiss Post in recent years, including several public intrusion tests with the e-voting system. The final report on the public intrusion test in 2022 [states](https://gitlab.com/swisspost-evoting/e-voting/e-voting-documentation/-/blob/master/Reports/PublicIntrusionTest/PIT_FinalReport_SwissPost_2022_EN.pdf): “Access to the e-voting system is protected by the web application firewall (WAF) OWASP ModSecurity Core Rule Set 3 (CRS). The CRS is configured to paranoia level 4, the highest level of protection available in the rule set. Swiss Post has been fine-tuning the CRS installation and the rule set for several years. As a result, there were very few false positives.” You can read more about Swiss Post’s e-voting architecture [here](https://gitlab.com/swisspost-evoting/e-voting/e-voting-documentation/-/blob/master/Operations/Infrastructure%20whitepaper%20of%20the%20Swiss%20Post%20voting%20system.md?ref_type=heads#access-layer-reverse-proxies) and [here](https://gitlab.com/swisspost-evoting/e-voting/e-voting-documentation/-/blob/master/Operations/ModSecurity-CRS-Tuning-Concept.md?ref_type=heads).

In an interview published on [Swiss Post’s e-government blog](https://digital-solutions.post.ch/en/e-government/blog/from-bug-bounty-programmes-to-open-source-solutions-and-quantum-computers-what-will-2024-look-like-for-cybersecurity), CISO Marcel Zumbühl gives more insight into the reasons for the sponsoring of CRS. You can find more about information security at Swiss Post [here](https://www.post.ch/en/about-us/responsibility/information-security-at-swiss-post).
