---
title: "How do I resolve error `Unknown variable: &MULTIPART\_PART\_HEADERS`?"
weight: 11
noindex: true
---

From CRS 3.2.2, 3.3.3 and up, **ModSecurity 2.9.6 or 3.0.8** (or versions with backported patches) are required due to the addition of new protections. We recommend upgrading your ModSecurity as soon as possible. If your ModSecurity is too old, your webserver will refuse to start with an *Unknown variable: &amp;MULTIPART\_PART\_HEADERS* error. If you are in trouble, you can temporarily delete file rules/REQUEST-922-MULTIPART-ATTACK.conf as a workaround and get your server up, however, you will be missing some protections. Therefore we recommend to upgrade ModSecurity before deploying a new CRS release.
