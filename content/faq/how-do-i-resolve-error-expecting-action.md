---
title: "How do I resolve error `Expecting an action, got: ctl:requestBodyProcessor=URLENCODED`"
weight: 11
noindex: true
---

This error can happen when you are using ModSecurity 3.0.0 to 3.0.2. Support for the URLENCODED body processor was only added in ModSecurity 3.0.3. Please upgrade your ModSecurity to at least 3.0.3.
