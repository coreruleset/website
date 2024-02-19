---
author: Christian Folini
categories:
  - Blog
date: '2019-04-25T15:29:15+02:00'
guid: https://coreruleset.org/?p=965
id: 965
permalink: /20190425/regular-expression-dos-weaknesses-in-crs/
site-content-layout:
  - default
site-sidebar-layout:
  - default
tags:
  - DDoS
  - DoS
  - ReDoS
  - Regular Expressions
  - security
theme-transparent-header-meta:
  - default
title: Regular Expression DoS weaknesses in CRS
url: /2019/04/25/regular-expression-dos-weaknesses-in-crs/
---


Somdev Sangwan has discovered several Regular Expression Denial of Service (ReDoS) weaknesses in the rules provided by the CRS project. They are listed under the following CVEs:

- [CVE-2019–11387](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-11387)
- [CVE-2019–11388](https://nvd.nist.gov/vuln/detail/CVE-2019-11388)
- [CVE-2019–11389](https://nvd.nist.gov/vuln/detail/CVE-2019-11389)
- [CVE-2019–11390](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-11390)
- [CVE-2019–11391](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-11391)

The fact that CRS is affected by ReDoS is not particularly surprising and truth be told, we knew that was the case. We just have not solved it yet - or have not been able to solve it yet.

Let me first explain what ReDoS is and then look at CRS and ModSecurity behavior in face of the problem.

#### What is ReDoS?

Pattern matching is a CPU intense task and given CRS is heavily based on regular expression patterns, there is a performance problem inherent to many of our rules. Alas, some of the patterns are more CPU intense than others and some have characteristics that steer the processor down a rabbit hole with an almost infinite number of matches if the payload knows about the weaknesses of a particular pattern. Given we are an open source project, our patterns are well known, and Somdev Sangwan created a script that would point him to potentially vulnerable rules, and he would then craft the payloads to kill the server. Well done.

#### How does ModSecurity deal with it?

Traditionally, the ModSecurity engine has PCRE limits that prevent the fall into the rabbit hole. These are the [<tt>SecPcreMatchLimit</tt>](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#SecPcreMatchLimit) and [<tt>SecPcreMatchLimitRecursion</tt>](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#secpcrematchlimitrecursion) directives. That means that with ModSecurity 2.x, the regex processor stops after a configurable number of matches. You have probably seen the PCRE limit error message in your logs. That is this ReDoS prevention mechanism at work. This mechanism is not without disadvantages, but it is quite successful with preventing ReDoS. More details can be found in the [ModSecurity Handbook 2nd Ed.](https://www.feistyduck.com/books/modsecurity-handbook/), page 185f.

There have been previous issues with ReDoS in CRS, but given that ModSecurity provided a safety belt, we have not given it much priority so far.

Things are different with ModSecurity 3.x, where the PCRE limit directives have not been re-implemented after the complete rewrite. The reason for this design decision is the assumption, that the underlying webservers do not allow ModSecurity to set the said limits independently. This means ModSecurity developers are afraid their code could re-configure the regex behavior of the whole server. Depending on the webserver implementation, this risk is present with ModSecurity 2.x as well. But the ModSecurity developers wanted to make sure they rule out this possible problem for ModSecurity 3.x. So if you want to change the PCRE limits, you need to recompile ModSecurity 3.x instead of re-configuring them via a directive. We would very much prefer to be able to configure the PCRE match limits at run time, even if this feature is an option that has to be enabled at compile time. So we hope the ModSecurity project will reconsider this.

As a consequence of the limitations with ModSecurity 3.x, there is no easy workaround for the ReDoS weaknesses anymore. You can thus claim that ReDoS is a bigger problem with ModSecurity 3.x than it was with ModSecurity 2.x.

The CRS project does not yet fully endorse ModSecurity 3.x for multiple reasons and this is one of them. So giving ReDoS a 2nd priority so far has been reasonable, as ModSecurity 2.x is the preferred platform to run CRS as of this writing.

But when ModSecurity no longer helps with ReDoS, then the rules need to be improved for the future, and that is clearly the job of the CRS project.

#### Why are there rules in CRS that allow ReDoS?

CRS consists of about 200 rules, most of them make use of regular expressions. Quite a few of them are really big and really complicated. And a large number of them is 10 or 15 years old and thus dating from a period when none of the current project members were active within the CRS project.

So when we took over the project, we first had to find our way around the regular expressions. Then we would start a clean-up process. One step was to make sure we re-obtained the sources for the two dozens of machine generated regular expressions. And a second step was a project to remove un-needed capture groups that would affect performance in a negative way.

So it is only fairly recently that we are actually in a position to turn our attention to ReDoS: First to clean up pressing CVEs, then to audit all the rules to learn which ones are really affected by the problem. Then to come up with a style guide / policy on how to write rules that are free from ReDoS. A tricky part with this can be to create a different regular expression that does 100% the same thing without the ReDoS problem. And finally to clean it all up with the style guide in hand. This can take a while.

#### What can you do in the meantime?

Running CRS is a tradeoff between performance (thus CPU and DoS exposure) and basic protection against many of the security risks described in the OWASP Top Ten. DoS is always a risk with a web server. Most DoS attacks are still executed at the network level, without the attacker paying attention to the existence of a WAF or the application at all. If he or she is taking the time to craft specific application level payloads to kill your server, they are likely to have the knowledge to craft similar payloads to kill your authentication server, your search form, or something else. So CRS is not your only DoS risk and I am sure, it is not the biggest one for most sites.

However, if you really suffer from a ReDoS attack, then monitoring is key and disabling individual rules temporarily will help you. That may look like an insecure practice, but given there are probably over 150 rules active, you are not dropping your shields completely with this. Because the worst thing would be to drop ModSecurity and/or CRS because you think that there is DoS problem you can not live with.

You need to take the attack payload, examine the ModSecurity / CRS behaviour and find out which rules are affected. ModSecurity 2.x is again more helpful in this regard than ModSecurity 3.x. And once you have identified the rule or rules, you disable it like you would write a rule exclusion for a false positive. Ideally you do this via the SecRuleRemoveById directive (to be placed after the CRS include in the configuration).

#### Our next steps

We are currently reviewing several pull requests dealing with the CVEs in questions. Somdev Sangwan thankfully did not only announce the weaknesses, but he also supported us with finding a remedy.

Once we have accomplished the step of reviewing and integrating the fixes, we plan to publish a CRS bugfix release 3.1.1 soon; ideally with identical behavior, but without the CVEs.