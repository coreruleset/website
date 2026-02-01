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
```

Can you quickly understand what this rule does? The metadata, transformations, operators, and actions are all jumbled together in a single string, making it difficult to parse both for humans and machines.

## Enter CRSLang

CRSLang is a YAML-based, technology-agnostic rule language designed to address these limitations while maintaining full backward compatibility with existing Seclang rules. Here's the same rule in CRSLang format:

```yaml
rule:
  metadata:
    comment: |
      "Validate request line against the format specified in the HTTP RFC"
    phase: 1
    id: 920100
    message: Invalid HTTP Request Line
    severity: WARNING
    tags:
      - application-multi
      - language-multi
    version: OWASP_CRS/4.0.0
  conditions:
    - variables:
        - REQUEST_LINE
      operator:
        negate: true
        rx: (?i)^(?:get /[^#\?]...
      transformations:
        - none
  actions:
    disruptive: block
    non-disruptive:
      - logdata: "%{request_line}"
      - setvar:
          collection: TX
          operation: =+
          assignments:
            - inbound_anomaly_score_pl1: "%{tx.warning_anomaly_score}"
```

The difference is immediately apparent. The rule structure is clear, with distinct sections for metadata, conditions, and actions.

## Key Features

### 1. Clear Structure and Separation of Concerns

CRSLang separates metadata, conditions, and actions into distinct, easy-to-understand sections. This makes rules easier to read, validate, and maintain.

### 2. Improved Logical Expressions

Seclang's support for complex logical conditions is limited and often requires workarounds. CRSLang provides a clean AND syntax, and we are working on extending its logical capabilities.


```yaml
rule:
  metadata:
    phase: 1
    id: 920310
    message: Request Has an Empty Accept Header
  conditions:
    - collections:
        - name: REQUEST_HEADERS
          arguments:
            - Accept
      operator:
        rx: ^$
      transformations:
        - none
    - variables:
        - REQUEST_METHOD
      operator:
        negate: true
        rx: ^OPTIONS$
    - collections:
        - name: REQUEST_HEADERS
          arguments:
            - User-Agent
      operator:
        negate: true
        pm: AppleWebKit Android Business Enterprise Entreprise
      transformations:
        - none
  actions:
    disruptive: block
```

### 3. Template Functions

CRSLang introduces reusable rule components, making it easier to maintain consistent patterns across your rule set. You can also define common patterns and use them with different variables:

```
detect-pattern-template: &detect-pattern
  operator:
    rx: "some-pattern"
  transformations:
    - urlDecode
    - lowercase

rule:
  metadata:
    phase: "1"
    id: 1
  conditions:
    - <<: *detect-pattern
      variables:
        - REQUEST_URI
  actions:
    disruptive: pass
```

### 4. Bidirectional Translation

One of CRSLang's most powerful features is its bidirectional translation capability. We've built a robust parser that can:

- Convert existing Seclang rules to CRSLang format
- Generate valid Seclang from CRSLang rules
- Preserve all semantic information during translation
- Maintain comment and documentation context

This means you can gradually migrate to CRSLang while maintaining compatibility with existing tools and deployments. The translation engine ensures that no information is lost in the conversion process, and round-trip testing validates correctness.

## Building on Previous Work

CRSLang builds upon the foundation laid by earlier parser projects. If you're familiar with our [msc_pyparser]({{% ref "2020-09-01-introducing-msc_pyparser.md" %}}) tool, you'll recognize the concept of converting ModSecurity rules into structured formats. CRSLang takes this concept further by providing a complete, production-ready language specification with full tooling support.

While msc_pyparser focused on rule manipulation through Python, CRSLang provides a comprehensive language specification with:

- ANTLR-based parsing with support for multiple target languages (Go, Python, Java), based on [seclang_parser]({{% ref "2026-01-22-introducing-seclang-parser-unified-antlr-based-parser.md" %}})
- Full support for Seclang v2 and v3
- Validation and testing frameworks
- IDE integration capabilities (syntax highlighting, validation, debugging)

## The Technology

CRSLang is powered by a sophisticated parser built with ANTLR, providing:

- **Multi-language support**: Generated parsers for Go, Python, and Java
- **Version compatibility**: Full support for Seclang v2 and v3
- **Semantic preservation**: No information loss during translation
- **Comment preservation**: Documentation and context maintained throughout the conversion process

The project is fully open source and available at [github.com/coreruleset/crslang](https://github.com/coreruleset/crslang).

## Looking Forward

CRSLang represents more than just a syntax change—it's a foundation for the future of OWASP CRS. With this new language, we're opening doors to:

- **Enhanced portability**: Support for multiple WAF technologies beyond ModSecurity
- **Alternative logical engines**: Integration with systems like Google CEL or Wirefilter
- **Better tooling**: IDE support, linting, automated testing, and debugging capabilities
- **Reduced learning curve**: Making it easier for new contributors to join the project
- **Improved maintainability**: Clearer rule structure means fewer bugs and easier updates

## Timeline and Migration

CRSLang will replace Seclang as the primary rule language in the next major release of OWASP CRS. We're committed to making this transition as smooth as possible:

1. **Current state**: CRSLang parser and tooling are available now
2. **Migration period**: Full backward compatibility maintained through translation engine
3. **Next major release**: CRSLang becomes the default format
4. **Long-term support**: Seclang translation capabilities maintained for existing deployments

You can start exploring CRSLang today by:

- Visiting the [CRSLang GitHub repository](https://github.com/coreruleset/crslang)
- Converting your existing rules to see the difference
- Providing feedback to help shape the final specification
- Contributing to the parser and tooling development

## Get Involved

We're excited about this evolution and would love your feedback. Whether you're a long-time CRS contributor or new to the project, your input is valuable as we shape the future of WAF rule development.

Join the conversation:
- GitHub: [github.com/coreruleset/crslang](https://github.com/coreruleset/crslang)
- OWASP Slack: [owasp.org/slack/](https://owasp.org/slack/) (#coreruleset channel)
- Mailing list: Join our community discussions

The future of OWASP CRS is clearer, more maintainable, and more accessible. We can't wait to see what the community builds with CRSLang.
