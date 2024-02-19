---
title: "Does the CRS protect against all vulnerabilities?"
weight: 7
noindex: true
---

No, the CRS scans only for generic, commonly occurring, malicious patterns. Application-specific vulnerabilities, such as logic bugs or missing authorization checks, cannot be detected by generic firewall rules. The CRS is therefore not a replacement for patching web applications. To increase your protection against current web application vulnerabilities, you can combine the CRS with a commercial rule set such as the [Trustwave ModSecurity Rules](https://www.trustwave.com/Products/Application-Security/ModSecurity-Rules-and-Support/). Such a rule set contains specific virtual patches for many common web applications.
