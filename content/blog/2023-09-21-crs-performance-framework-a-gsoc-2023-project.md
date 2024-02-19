---
adv-header-id-meta:
  - ''
ast-featured-img:
  - disabled
author: Alessandro Monachesi
categories:
  - Blog
date: '2023-09-21T13:05:47+02:00'
footnotes:
  - ''
guid: https://coreruleset.org/?p=2273
id: 2273
permalink: /20230921/crs-performance-framework-a-gsoc-2023-project/
stick-header-meta:
  - ''
theme-transparent-header-meta:
  - ''
title: CRS Performance Framework &#8211; A GSoC 2023 Project
url: /2023/09/21/crs-performance-framework-a-gsoc-2023-project/
---


This year, the OWASP ModSecurity Core Rule Set for the second time took part in the Google Summer of Code initiative. Google Summer of Code (GSoC) is a global online program focused on bringing new contributors into open-source software development. GSoC contributors work with an open-source organization of their choice on a 12+ week programming project under the guidance of the mentors from the organization. [Dexter Chang](https://github.com/dextermallo) had applied to the CRS project with a proposal for a performance framework. We spoke to Dexter about his GSoC experience with the Core Rule Set.

**Please tell us about yourself: Who are you, what is your educational background?**

I am Dexter Chang and I’m currently based in Taiwan. I have more than three years of experience as a backend engineer, when I shifted my career into the security domain. At the time I applied for the GSoC project in May 2023, I was taking my master’s degree in cyber security engineering at the University of Warwick, UK.

**Why did you choose to participate in the Google Summer of Code initiative (GSoC)?**

Participating in GSoC is a great opportunity for anybody – even more so now since it isn’t limited to students anymore. The program not only provides opportunities to collaborate with communities on open-source projects but also provides stipends to the participants. As for me, the most valuable part of joining GSoC was that the participants can develop their experience and learn from their mentors how to contribute to the communities. And you can even stay in the community once the campaign is completed.

<figure class="wp-block-image size-full is-resized">![](/images/2023/09/Dexter_Chang.jpg)<figcaption class="wp-element-caption">*Dexter Chang applyed for a Coogle Summer of Code project with the Core Rule Set.*</figcaption></figure>**Why did you want to contribute to the OWASP ModSecurity Core Rule Set?**

The Core Rule Set is an open-source project with valuable impact on the industry. It is used by many enterprises and organizations to fight against cyber threats. Joining the development of the CRS not only accelerated my knowledge regarding cybersecurity but knowing that my contribution to the project will be integrated into CRS and thus put into real practice is quite fascinating and exciting! Just like every engineer enjoys it when the results of their efforts can be seen in the final product. More importantly, the mentors and the community are experts in cybersecurity, and they were very generous to support and guide me when I was lost. Another reason that I applied to CRS is that my master's program also uses another open-source project under OWASP. Thus, I thought it would be a great opportunity for me to join the organization.

**Tell us about your project for GSoC.**

The project I was working for during the GSoC campaign is called the [CRS Performance Framework](https://summerofcode.withgoogle.com/programs/2023/projects/jdv2MaJR) and aims to support future development on CRS. While one of the problems with WAF is that the performance will be affected, there is no appropriate method to measure or evaluate the impacts caused by a change. For instance, we may have a rule that aims to block cyberattacks when the incoming request contains a keyword like “hacker cat”. This may look something like this (this is not the exact way a rule works, just a readable way for demonstration):

```
<pre class="wp-block-code">```
SecRule: text-contain-regex: "hacker cat"
```
```

In this case, when a request flows in one's server and attaches a message like “I am a hacker cat!”, it can be detected and blocked by the Core Rule Set. Then we may want to extend the rule to other expressions for felines:

```
<pre class="wp-block-code">```
SecRule: text-contain-regex: "hacker (cat|kitty|meow)"
```
```

In this case, how can we measure the performance impact caused by the change, especially since there are many considerable-length regexes in the project? The CRS Performance Framework aims to resolve the issue. The framework is developed to help developers testing the performance of CRS and to provide a benchmark in order to compare the performance of CRS with different versions or different configurations.\*

<figure class="wp-block-image size-large is-resized">![](/images/2023/09/process-diagram-1024x528.png)<figcaption class="wp-element-caption">*A lovely little diagram of how performance tests in Dexter Chang's performance framework work. [Work in progress](https://github.com/coreruleset/rules-performance-tests/blob/main/assets/process-diagram.png).*</figcaption></figure>**What challenges did you encounter during your GSoC project?**

Developing a side-project for the Core Rule Set is very difficult for individuals because it requires knowing many tiny pieces: How to run the services with containerization, how to interpret the rule, and so on. Specifically, preferences for evaluating performance can vary by individual. Some people may be interested in response time while some may care more about memory and CPU utilization. Nonetheless, my mentors and I discussed and successfully developed a framework that can integrate multiple packages to provide customized needs. It also benefits the future development.

**What was your overall experience as a GSoC contributer to the CRS project?**

Though the overall experience was quite intensive – I needed to manage my academic work and the open-source contribution simultaneously – the project went smoothly since my mentors and I had a weekly meeting to discuss, check, and drive the project in superior directions.

**So, all in all, would you recommend joining GSoC to others?**

The journey of GSoC is not easy, but it is definitely worth it. I would like to thank my mentors – CRS project co-leads Felipe Zipitría and Christian Folini – for their guidance and support. I would also like to thank the CRS community for their support and feedback. Though the GSoC is finished, my journey with CRS is not. I will keep on contributing to the Core Rule Set.

You can read more about GSoC 2023 project results and feedback on the [Google Open Source Blog](https://opensource.googleblog.com/2023/09/gsoc-2023-project-results-and-feedback-part-1.html).

*\* More details concerning the CRS Performance Framework including live demos can be found in the [project repository](https://github.com/coreruleset/rules-performance-tests#gsoc-2023---crs-waf-performance-testing-framework).*