---
title: "What is CRS?"
weight: 1
noindex: true
---

The OWASP CRS is a set of firewall rules, which can be loaded into [ModSecurity](https://www.modsecurity.org/) or compatible web application firewalls. The CRS consists of various `.conf` files, each containing generic signatures for a common attack category, such as SQL Injection (SQLi), Cross Site Scripting (XSS), et cetera. It uses string matching, regular expression checks, and the libinjection SQLi/XSS parser.
