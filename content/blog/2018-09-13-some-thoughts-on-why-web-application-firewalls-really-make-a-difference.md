---
author: dune73
categories:
  - Blog
date: '2018-09-13T06:41:21+02:00'
permalink: /20180913/some-thoughts-on-why-web-application-firewalls-really-make-a-difference/
title: Some Thoughts on why Web Application Firewalls Really Make a Difference
url: /2018/09/13/some-thoughts-on-why-web-application-firewalls-really-make-a-difference/
---


*This is a guest piece by Jamie Riden / [@pedantic\_hacker](https://twitter.com/pedantic_hacker). Jamie has been doing penetration tests, secure development training and security code review since 2010 - and other kinds of computer-wrangling for much, much longer.*

Having been a systems engineer, a coder and now a pen-tester, I'd like to take a brief moment of your time to talk about layered defenses; specifically in this case why running a web application firewall is a good idea. In my current job I get engaged to do various forms of pen-testing. Relatively often, we turn up something in a web application that could have been prevented in a couple of ways. Last week for example, I found a lovely old-school OS command injection bug in a single parameter of a reasonable-sized website.

Very few people will have a pen-test knowing of major flaws in their website; if they knew about an issue it would have been fixed already. Given that pen-test is often the last step most companies will carry out before a site goes live, any flaws we find will have evaded all the other controls in place, like secure code training, peer code review as well as unit and regression tests. Sometimes it is not as major as command injection, and only a common-or-garden cross-site scripting issue. Sometimes it's full access to the database via SQL injection.

I probably don't need to argue the point that the earlier you know about a bug in your site the better; you can work out how to mitigate, and get the fix in development which minimizes disruption for the end-user, and therefore also unwanted surprises for the developers, administrators and customer support.

What ModSecurity and the Core Rule Set allows you to do is quickly set something up that (a) will be seeing your web traffic on the server, saving any mucking about with SSL decryption on the wire. It will (b) block or log on a number of things which are generally known to be probes and exploitation of issues such as SQL injection, command injection, XSS, local and remote file inclusion and more. These rules won't be a perfect fit for everyone, but if the use of your site routinely violates one or more, it's good to at least understand why. Often it can be that an insecure direct object reference is being used; it may be that you're taking a file parameter and doing absolutely watertight parsing to make sure that it's OK; however for every person who is doing it right there are plenty who think they are but with subtle flaws.

This means that if you can prevent at least the basic forms of attack against your site, and give yourself visibility at attempted hacking attempts, that can all be very useful information. Even if you just deploy the default rule set in warn-only mode, that provides very valuable insights into what people are trying to do that the WAF thinks they shouldn't be doing. Of course, this is exactly the mode you should initially deploy in, because there is always a chance that some of the data flow will trigger some of the rules and you will need to weed out these false positives for your service to behave smoothly.

Lots of people just set up their website and let it run assuming everything is OK. Getting a support call, or an email from Brian Krebs or Troy Hunt is not a nice way to discover you have security issues. For no money and not too much time you can make the whole website a lot safer and give yourself better visibility of what is going on daily in terms of attempts to subvert the operations.

Of course, these bugs should be fixed in the software. A WAF is only an additional safety net for those bug that continue to exist in the software. And it can come in handy as a bandaid, when fixing a newly discovered bug on the production site takes more time than a couple of hours.

I should also note where it won't help - if you have made a fundamental application logic flaw, ModSecurity doesn't magically know how your site is meant to operate. For example, I occasionally see an anti-pattern where as soon as one user is given permission to create other user, they can create super-users - that is, user accounts with more privileges than the one that created them - which is immediate privilege escalation.

So, it won't solve all your problems - but it is a very useful safety net and does help detect intrusions early on. Remember that you are getting plenty of free web application testing outside of any paid engagements you might get a traditional pentest company in to do for you. Every web application of any seriousness should have a web application firewall, just like there will be a classical firewall protecting it.

*By Jamie Riden / [@pedantic\_hacker](https://twitter.com/pedantic_hacker), who wishes more of his customers would use CRS*
