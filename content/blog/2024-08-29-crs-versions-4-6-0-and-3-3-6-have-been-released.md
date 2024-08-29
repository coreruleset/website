---
title: CRS Versions 4.6.0 and 3.3.6 have been released
date: 2024-08-29
author: amonachesi
categories:
    - Blog
---
We have recently released version [4.6.0](https://github.com/coreruleset/coreruleset/releases/tag/v4.6.0) for CRS 4, fixing a serious problem. As this problem affects CRS 3 as well, we also did a backport release for v3. ([3.3.6](https://github.com/coreruleset/coreruleset/releases/tag/v3.3.6)).

The new releases tackle two multipart file upload bypass methods that were reported by [@luelueking](https://github.com/luelueking):

1.	Wrapping the Content-Disposition with non-printable characters like \x0e (e.g. “%0e Content-Disposition %0e”) may allow the header to go undetected by the WAF engine as it may not be correctly parsed.
2.	Inserting the character \ in a filename (e.g. “1.j\s\p”) may let the filename go undetected.

The fixes introduced in both versions are the same:

1.	We have added a new rule 922130 which checks if any multipart header contains a non-ASCII character (v4: [#3796](https://github.com/coreruleset/coreruleset/pull/3796); v3: [#3797](https://github.com/coreruleset/coreruleset/pull/3797)).
2.	The use of backslashes in file names is prevented (v4: [#3799](https://github.com/coreruleset/coreruleset/pull/3799), v3: [#3800](https://github.com/coreruleset/coreruleset/pull/3800)).

Thanks to @luelueking for bringing this to our attention.

Release 4.6.0 contains other features and fixes like

-	a rule to detect bash tilde expansions by [@Xhoenix](https://github.com/Xhoenix) ([#3765](https://github.com/coreruleset/coreruleset/pull/3765))
-	the addition of the .pem format to the restricted file extensions by [@EsadCetiner](https://github.com/EsadCetiner) ([#3789](https://github.com/coreruleset/coreruleset/pull/3789))
-	the removal of unnecessary chain rule and capture in rule 921180 by [@EsadCetiner](https://github.com/EsadCetiner) ([#3787](https://github.com/coreruleset/coreruleset/pull/3787))
-	a fix for rule 942160 by checking against REQUEST_FILENAME by [@mat1010](https://github.com/mat1010) ([#3782](https://github.com/coreruleset/coreruleset/pull/3782))
-	an update of rule 932270's version variable by [@airween](https://github.com/airween) ([#3786](https://github.com/coreruleset/coreruleset/pull/3786))