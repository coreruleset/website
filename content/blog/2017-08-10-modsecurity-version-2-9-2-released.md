---
author: Walter Hop
categories:
  - Blog
date: '2017-08-10T12:48:47+02:00'
title: ModSecurity version 2.9.2 released
url: /2017/08/10/modsecurity-version-2-9-2-released/
---

Trustwave has released [ModSecurity version 2.9.2](https://www.trustwave.com/Resources/SpiderLabs-Blog/Announcing-ModSecurity-version-2-9-2/).

This is an important update for users of the Core Rule Set. To detect SQL and XSS injections, CRS relies in part on the [libinjection](https://github.com/client9/libinjection/blob/master/README.md) library by Nick Galbreath. This library is bundled with ModSecurity. It is regularly updated to address new types of injections. Therefore, to have optimal protection against SQL and XSS injections, you should always keep ModSecurity updated.

The update also fixes two security vulnerabilities and contains various other improvements.

For more details on the changes in this version, please read the [Trustwave SpiderLabs blog announcing ModSecurity version 2.9.2](https://www.trustwave.com/Resources/SpiderLabs-Blog/Announcing-ModSecurity-version-2-9-2/).

If you are confused about the relationship between the CRS and ModSecurity, please see [our FAQs on this topic](https://coreruleset.org/faq/).
