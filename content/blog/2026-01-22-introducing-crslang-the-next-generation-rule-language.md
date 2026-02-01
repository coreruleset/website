---
title: 'Introducing CRSLang: The Next Generation Rule Language for OWASP CRS'
date: '2026-01-22'
author: fzipi
categories:
  - Blog
---

We're excited to introduce **CRSLang**, a new YAML-based rule language that will replace Seclang in the next major release of OWASP CRS. This represents a significant evolution in how we write, maintain, and deploy WAF rules.

## Why CRSLang?

For nearly two decades, the OWASP CRS has relied on ModSecurity's Seclang syntax. While Seclang has served us well, it comes with significant limitations that have become increasingly apparent as the project has grown:

### The Problems with Seclang

- **Technology Lock-in**: Rules are tightly coupled to ModSecurity syntax, making it difficult to support other WAF engines
- **Portability Issues**: Direct deployment to alternative WAF platforms requires significant translation efforts
- **Complexity**: Rules are hard to read, write, and maintain, with all components mixed in long strings
- **Learning Curve**: The steep barrier to entry discourages new contributors
- **Limited Expressiveness**: Complex logical conditions (especially OR operations) require workarounds, and there's no support for template functions

Consider this typical Seclang rule:

```apache
# Validate request line against the format specified in the HTTP RFC
SecRule REQUEST_LINE "!@rx (?i)^(?:get /[^#\?]..." \
    "id:920100,\
    phase:1,\
    block,\
    t:none,\
    msg:'Method is not allowed by policy',\
    logdata:'Matched Data: %{MATCHED_VAR} found within %{MATCHED_VAR_NAME}',\
    tag:'application-multi',\
    tag:'attack-protocol',\
    ver:'OWASP_CRS/4.0.0',\
    severity:'WARNING'"
