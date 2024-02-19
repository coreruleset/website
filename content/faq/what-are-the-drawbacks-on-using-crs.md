---
title: "What are drawbacks of using the CRS?"
weight: 7
noindex: true
---

The CRS can be quite strict in detecting certain attacks. This means that sometimes a normal, bona fide, request may be blocked as a *false alert* or *false positive*, for instance, if it contains suspicious character sequences. We aim to minimize false positives as much as possible, but in some situations it may be necessary for you to write an *exclusion rule* which selectively disables some CRS checks. CRS is updated from time to time in order to address false positives and add new protections, which requires you to replace the files with a new release. Furthermore, the CRS adds some, usually minor, processing overhead to any request.
