---
author: csanders-git
categories:
  - Blog
date: '2017-11-07T01:46:59+01:00'
title: CRS Project News November
---

This is the CRS newsletter covering the period from Early October until today.

We held our monthly community chat. We had quite a few people stop by. Special thanks to our active participants:

- dune73
- fzipi
- csanders
- franbuehler
- emphazer
- spartantri
- luketheduke
- techair
- jose\_
- airween
- athmane
- bostrt

During the chat we discussed the following

- Promotion of 3 heavy contributors to developers ([@fgsch](https://github.com/fgsch), [@fzipi](https://github.com/fzipi) and [@spartantri](https://github.com/spartantri)) 
    - Docs will be updated to reflect their promotion, congrats and thank you!!!
- CRS Summit at AppSecEU in June in Tel Aviv (?) 
    - dune73 will setup a project and let us know the status as we move along.
    - fzipi spoke at OWASP Dev Summit about WAF test data. A new license is available (<https://cdla.io/>)
- Testing (FTW is working when using with [CRS-support/ftw#14](https://github.com/CRS-support/ftw/pull/14)) 
    - PR is awaiting merge but seems to be working well.
    - dune73 plans to write a blog.
- Idea to update release poster (with logo in the center) 
    - We had some great press about the poster.
    - Need to check balance but Dune73 will finance privately changes.
    - Shooting for by AppSecEU
    - Idea to start to sell the release poster via a printing service like [Redbubble](https://www.redbubble.com/)
- Info: CRS nominated for the German Open Source Business award ([https://osbar.it](http://osbar.it/)) 
    - Everyone is excited thank you to Dune73 for nominating us
- Plans for new blog posts 
    - Franbuehler writing up about SQL disassembly
    - dune73 writing about FTW
    - csanders-git writing about Apache vulnerability breakdown.
- \[PR [\#881](https://github.com/coreruleset/coreruleset/pull/881)\] : Java Attacks 
    - Will be assigned to csanders-git
- \[PR [\#884](https://github.com/coreruleset/coreruleset/pull/884)\] : SQL injection probing rule split 942370 
    - emphazer is working on a PR for this so it's in line with franbuelers comments.
- \[PR [\#896](https://github.com/coreruleset/coreruleset/pull/896)\] : Command substitution backquoted version support 
    - Splitting into two and fixing conflict when available.
- \[PR [\#899](https://github.com/coreruleset/coreruleset/pull/899)\] : Dokuwiki and Nextcloud exclusion packages (work in progress) 
    - Will be done when submitter has time.
- \[PR [\#905](https://github.com/coreruleset/coreruleset/pull/905)\] : Duplicated header bypass fix and chunk support 
    - csanders-git and fzipi are going to take the helm on getting this one through.
- \[PR [\#922](https://github.com/coreruleset/coreruleset/pull/922)\] : New developers (see above) 
    - Merged, need to add other testers also.
    - remove spratantri from 905 as contributor
- Many PRs / test updates by [@azhao155](https://github.com/azhao155) (which are awesome). Bring up a question about what to do with Apache versus Nginx 
    - behaviors when the underlying engine 'fixes' and issue.
    - Going to add support for multiple return status. This should take care of all the test updates.
- \[Issue [\#924](https://github.com/coreruleset/coreruleset/issues/924)\] Tagging of CVE/CWE 
    - The conversation centered around the if adding these added increased complexity of writing rules it may also muddy logs
    - Everyone agreed additional information would be nice, CVE CWE, WASC, CAPEC
    - Pushed the conversation back to the issue with regard to CVE.
- Release 3.1 planning 
    - Possible after Java fixes are done.
- Stickers and maybe shirts (for appsec eu) using Redbubble
- New ModSecv3 t-shirt were made, current order is empty but more may be coming

The next community chats will be held on the following dates:

- Dec 4, 2017, 20:30 CET
- January 8, 2018 20:30 CET (Note: The change from our normal schedule)
- February 5, 2018 20:30 CET

Upcoming talks and talks that were just posted

- ModSec 3.0 talk on B-sides Toronto next week: <https://github.com/bsidesto/bsidesto.github.io/blob/5fc5ef3169e72b0ec42e959ff2caed331acd5ac2/2017/Presentations2017/BSidesTO2017-libModSecurity.pdf>
- BlackHat Europe Arsenal demo for libModSecurity in December: <https://www.blackhat.com/eu-17/arsenal/schedule/#modsecurity-300-9079>
- WAFs FTW! A modern devops approach to security testing: [https://www.youtube.com/watch?v=05Uy0R7UdFw ](https://www.youtube.com/watch?v=05Uy0R7UdFw)
- Introducing the OWASP ModSEcurity Core Rule Set (CRS) 3.0: <https://www.youtube.com/watch?v=oCxW966128A>

Some nice new blog posts have come out on coreruleset.org

- [How You Can Help the CRS Project](https://coreruleset.org/20170913/how-you-can-help-the-crs-project/)
- [Writing FTW test cases for OWASP CRS](https://coreruleset.org/20170915/writing-ftw-test-cases-for-owasp-crs/)
- [OptionsBleed Defenses](https://coreruleset.org/20170920/optionsbleed/)
- [CRS Project Nominated for Swiss DINACon Award](https://coreruleset.org/20171003/crs-project-nominated-for-swiss-dinacon-award/)
