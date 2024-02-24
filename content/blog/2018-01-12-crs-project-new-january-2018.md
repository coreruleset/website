---
author: csanders-git
categories:
  - Blog
date: '2018-01-12T07:14:45+01:00'
permalink: /20180112/crs-project-new-january-2018/
title: CRS Project News January 2018
url: /2018/01/12/crs-project-new-january-2018/
---


This is the CRS newsletter covering the period from Early December until today (Now in 2018, Happy New Year!!).

We held our monthly community chat. We had quite a few people stop by. Special thanks to lifeforms for leading the chat.

- - csanders
    - fzipi
    - spartantri
    - dune73
    - emphazer
    - fgs
    - franbuehler

Our agenda from before the chat is available [here](https://github.com/coreruleset/coreruleset/issues/991). We had a short chat, during the chat we discussed the following:

- The OWASP CRS Mailing list seemed to be broken for a bit, we confirmed that it is currently working, and who the administrators are (dune73, lifeforms, and csanders)
- csanders committed to making changes to FTW necessary to get azhao155's PR's (and #989 which deals with FTW) merged.
- A number of folks are testing the Java protections PR that is slotted for 3.1
- The Java rules (#990), that are a key feature of 3.1 need some attention 
    - We'd like to see correct formatting before merger
    - And a number of FTW tests added for it.
- There was interest expressed in a format checker script 
    - A reminder the required format is available via https://github.com/coreruleset/coreruleset/blob/v3.1/dev/CONTRIBUTING.md
- OWASP\_TOP\_10 tags are outdated with new release and will be updated as part of rule cleanup 2.0 
    - The older versions are available here: https://github.com/coreruleset/coreruleset/blob/95e7e6b3982eca93989c7948faca4a961737eace/rules/REQUEST-944-APPLICATION-ATTACK-JAVA.conf
    - A new ticket will be opened taking into account discussions from https://github.com/coreruleset/coreruleset/pull/881/files
- Dune73 will review #983 and #982 and merge if ready.
- csanders will write some of the documentation from #986 and provide a space on [coreruleset.org](http://coreruleset.org/) for the information to live.
- \#974, which deals with transfer encoding, is awaiting PR, this change requires both correctly evaluating the TE RFC and the extensions. For 3.1 we're gonna do basic abuse checks in PL and any extension checks will be in PL minimum with further review planed for 3.2.
- We'd like to add the PR for CPanel exclusion to 3.1, due to how CPanel sets up their system it causes false positives, ideally CPanel would fix this but they haven't yet so we'll add a class exclusion similar to how we did with WordPress, Drupal, etc. emphazer said he could take this on.
- We reviewed spartantri idea for filetype checking based on STREAM\_INPUT\_BODY. It is unclear if this feature will be exposed as part of libmodsecurity. A PR will be prepared with the known compatible stuff enabled and the other stuff commented out and possible enabled over time.</span>
- Dune73 discussed a project for a volunteer that would shift rules that only require Phase 1 variables to use the phase:1 action for performance reasons.
- AppSecEU has been moved from Israel to UK and shifted to match the dev summit two weeks earlier. This would thus be perfect for our planned little CRS summit. [@dune73](https://github.com/dune73) is in charge of this.
- dune73 is doing a ModSec/CRS/NGINX webinar with O'Reilly on January 9. Subscription is free, the slides will be shared afterwards.

The next community chats will be held on the following dates:

- February 5, 2018 20:30 CET
- March 5, 2018 20:30 CET
- April 2, 2018 20:30 CET

Some nice new blog posts have come out on coreruleset.org

- [Core Rule Set: The evolution of an OWASP Project ]({{< ref "blog/2018-01-12-core-rule-set-the-evolution-of-an-owasp-project.md">}})
