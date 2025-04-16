+++
title = 'False Negatives, False Positives – How the CRS team decide when to add or modify rules, and when we decide not to add them'
date = 2025-04-15T13:51:38-07:00
draft = false
+++
My name is Michela, and I’ve quite recently and gradually begun participating in the CRS project – a group of very sharp and incredibly welcoming people, who work to make the Internet safer. Needless to say, it’s been very interesting, and fun, so far! 
As part of my onboarding, so to speak, I’ve been reading lots of [documentation](https://coreruleset.org/docs/1-getting-started/1-1-crs-installation/) on how the project is run, official rule syntax and formatting guidelines, collaborations with other teams like those of ModSecurity and Coraza, and of course, how decisions are made about rule-making. 

I thought an effective way to learn, and to be productive right away, would be to go through an issue or two in the project issue tracker. So, I scanned the list of open issues, and clicked on one that caught my eye, “[SQL Injection in User-Agent #4035](https://github.com/coreruleset/coreruleset/issues/4035)”. There, the issue reporter described an attack against their infrastructure that involved thousands of requests that contained SQL queries – a possible SQL injection attack. The reporter noticed that these requests were not intercepted by ModSecurity and CRS, hence the labelling of this issue as a *false negative*.

Issue 4035 was interesting to me because it is labelled as a false negative, meaning it is potentially an area not covered by CRS that could be abused by attackers. Of course, we want to keep those to a minimum. 

After reading through the issue comments by other team members, I decided to do some of my own testing to confirm the situation described in the issue report, and to work out possible web application firewall (WAF) rule-based remedies. In doing so, I wrote these two basic rules: 

```apacheconf
SecRule REQUEST_HEADERS:User-Agent "@rx (?i)select(\s+)(.*)where" 
"id:1000200, 
 phase:1, 
 deny, 
 t:none, 
 msg:'User agent not allowed - possible SQL injection attempt', 
 logdata:'Matched Data: Unauthorised user agent in %{MATCHED_VAR_NAME}: %{MATCHED_VAR}'" 
```

```apacheconf
SecRule REQUEST_HEADERS:User-Agent "@rx (?i)case(\s+)(.*)when" 
"id:1000201, 
 phase:1, 
 deny, 
 t:none, 
 msg:'User agent not allowed - possible SQL injection attempt', 
 logdata:'Matched Data: Unauthorised user agent in %{MATCHED_VAR_NAME}: %{MATCHED_VAR}'"
```

With these new rules in place in my test environment, I used curl to make requests pulled from the issue reporter’s log files. All of my test requests from those log entries were caught by ModSecurity with the new rules in place. That seemed like a decent first pass at a possible solution. Hooray! 
When I brought my findings back to the team in the CRS Slack channel, I received a lot of helpful information and advice about the CRS regex generation tools and rule testing kit. These tools help make writing new rules more efficient, less prone to error, and more comprehensive in their scope. Project veteran, Christian Folini, ran some tests of his own, formatting the output neatly and as described in one of his own blog posts at netnea.com. 

**First, Christian ran tests using log files included by the issue reporter:**

```bash-session
$ N=1; cat /mtmp/user-agent.sql.injections.txt | while read LINE; do echo $N; N=$((N+1)); echo "$LINE" > /tmp/tmp.$$; curl localhost -d "@/tmp/tmp.$$"; done
```

**The output:** 

```bash-session
cat access.log.issue-4035-pl2 | alscores | modsec-positive-stats.rb 
INCOMING                     Num of req. | % of req. |  Sum of % | Missing %
Number of incoming req. (total) |    508 | 100.0000% | 100.0000% |   0.0000%

Empty or miss. incoming score   |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   0 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   1 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   2 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   3 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   4 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   5 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   6 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   7 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   8 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of   9 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of  10 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of  11 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of  12 |      0 |   0.0000% |   0.0000% | 100.0000%
Reqs with incoming score of  13 |      2 |   0.3937% |   0.3937% |  99.6063%
Reqs with incoming score of  14 |      0 |   0.0000% |   0.3937% |  99.6063%
Reqs with incoming score of  15 |      1 |   0.1968% |   0.5905% |  99.4095%
Reqs with incoming score of  16 |      0 |   0.0000% |   0.5905% |  99.4095%
Reqs with incoming score of  17 |      0 |   0.0000% |   0.5905% |  99.4095%
Reqs with incoming score of  18 |      5 |   0.9842% |   1.5748% |  98.4252%
```

He then identified a number of requests that bypassed CRS. When he added the user agent header to rules 942151, 942100, 942190, and 942230 while running CRS in paranoia level 2, coverage in deflecting these attacks was a lot better, at 82%, but still not great. It also resulted in false positives. 

With that, we determined that rule changes are likely not the best course of action for this specific type of attack at this time. 

One important reason not to change or make new rules based on this particular attack in question is that by all available indications, it would not actually work -- it appears the "queries" in these bogus requests might just be random garbage that (even if allowed to run) could not actually exfiltrate or manipulate data. Project community member, Dan Kegel, says, *"I think the first question one should ask when looking at a false negative report might be something like 'What system do these attacks work on?' In other words: if they're just the output of some fuzzer, and no system is actually vulnerable to these patterns, why should coreruleset detect them?"* It may however be difficult in some situations to know with absolute certainty that a given attack -- or one with similar characteristics -- can actually cause harm. This is why CRS takes a *generalised* approach to intercepting attack patterns. More on that in a moment.

So, even assuming the attack or one like it could function as intended, the logic behind the decision not to make any rule changes is that in order for the attack described in this issue to be effective, it would likely have to be run against an application that is actively parsing logs – think Logstash, Graylog, and the like – and that application would have to have gaps in its input sanitisation, allowing the code inserted into the user agent field of the requests in question to be run. That’s a fair number of uncommon “ifs”, meaning there would have to be quite an unusual convergence of circumstances for this attack, or one like it, to succeed. That alone is not a reason to avoid adding or changing rules, however. After all, highly targeted attacks are ever more common, as nation-states and sophisticated criminal gangs become the dominant cyber threat actors that stewards of applications and infrastructure face.
 
So, why aren’t we adding new rules for this particular type of attack? Basically, our testing indicates that doing so would introduce a significant enough number of new false positives, without a strong enough benefit to CRS users. After all, WAF administrators, who consider their exposure to certain highly specific sorts of attack, can always add their own custom rules, like the ones I’ve written above. CRS is run by a relatively small all-volunteer team – time is limited, so it is crucial that we prioritise effort for maximum benefit to the community at large. Finally, WAFs and CRS are a “first line of defence” for generic attack types – SQL injection, generally, for example, rather than specific SQL injection attack methods or vulnerabilities. If CRS had rules for every single vulnerability and attack in existence, the rule-set would be insanely large – that's just not realistic, and it doesn’t quite line up with the core design philosophy of CRS as a generalised form of defence. CRS is meant to be part of a comprehensive multi-layered cyber security approach to protecting infrastructure, applications, and data. In other words, we of course consider WAFs vital components in defending against cyber threats, but there is no one solution to protect against every possible threat or attack – whether we are talking about WAFs or any cyber defence technology. 

Having said all that, the CRS project team want CRS to be as effective at blocking malicious activity as possible, and we therefore adopt a posture that errs on the side of false positives, as opposed to false negatives. That means we would rather administrators have to deal with making exceptions for a reasonable (but still hopefully small) number of false *positives*, as opposed to them being at risk from false negatives. In fact, this posture is one key difference between CRS and most commercial options, and it is a difference that we believe makes users of the project safer. 

To this end, we may consider adding new rules that apply to user agent fields for cases like that described in issue 4035. Another possibility is changing some rules *(942151, 942100, 942190, 942230)* to serve the same end. Due to the relatively long to-do list the team are always working through -- and because making such a rule change would be no small effort -- it may be some time before such changes are made, if it is determined that they should be made at all. We also help guide users of CRS to our comprehensive documentation on how to write effective rules and exceptions, as well as how to test them. That way, they can quicky respond to and defend against threats targeted towards their environments, use cases, and applications. 

Hopefully, this gave you a bit of insight into the approaches, thinking, and philosophies behind CRS, and helps explain how decisions are made about when and how to make rule changes. Have any questions or thoughts to share? Let us know! You can get in touch with us via the [CRS mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project) or our [Slack channel](https://coreruleset.org/20181003/owasp-crs-slack/).