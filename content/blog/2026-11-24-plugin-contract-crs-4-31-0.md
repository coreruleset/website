---
author: franbuehler
categories:
  - Blog
date: '2026-11-24T09:00:00+01:00'
tags:
  - CRS-News
  - Plugins
  - CRS-v4
title: 'Plugins Can Finally Extend CRS Lists: The New Plugin Contract in CRS 4.31.0'
slug: 'plugin-contract-crs-4-31-0'
---

How can a CRS plugin allow WebDAV methods like `PROPFIND` without copying the whole list of allowed methods from CRS? Until now: it couldn't.

In this blog post I introduce the new **plugin contract** that solves this problem. I also explain a breaking change that comes with it: the lists of allowed **methods** and **HTTP versions** now use the same `|pipe|` format as content types.

Both changes are part of [CRS 4.31.0](https://github.com/coreruleset/coreruleset/releases/tag/v4.31.0), released on 23 November 2026. If you set `tx.allowed_methods` or `tx.allowed_http_versions` in your `crs-setup.conf`, or if you use the Nextcloud, SOGo or Plausible plugin, please read the section about the breaking change before you upgrade!

### The problem

Plugins are loaded **before** `REQUEST-901-INITIALIZATION.conf`. Rule 901 only sets a default value if the variable does not exist yet. So when a plugin sets `tx.allowed_methods` itself, the CRS defaults are skipped.

The Nextcloud plugin, for example, needs WebDAV methods. To add them, it has to copy the CRS defaults first:

```apache
SecRule &TX:allowed_methods "@eq 0" \
    "id:9508100,\
    ...
    setvar:'tx.allowed_methods=GET HEAD POST OPTIONS'"
```

This works, but every plugin keeps its own copy of the CRS defaults. When CRS changes a default, the copies are outdated, and nobody notices. That is exactly the kind of bug you don't want in a WAF!

This was [issue #4286](https://github.com/coreruleset/coreruleset/issues/4286), and I worked on it at the CRS developer retreat in Southampton in November 2026.

### What we tried first

There were a few ideas in the issue:

- **Set the defaults in `crs-setup.conf`.** But most people never update their `crs-setup.conf`, so they would quietly miss new defaults.
- **Load `REQUEST-901-INITIALIZATION.conf` before the plugins.** This changes the include order that every integration and package depends on, just to fix a plugin problem.
- **Move the checking rules (911100, 920420) to phase 2** with `SecRuleUpdateActionById`. ModSecurity v2 refuses to change the phase of a rule (`AH00526`), and libModSecurity v3 does not implement `SecRuleUpdateActionById` at all.

So none of these worked. The next idea was to give plugins their own variables, and CRS adds them to the lists after the defaults are set. Sounds simple. But the three engines had some surprises for us.

### What the engines taught us

We tested every step on ModSecurity v2, libModSecurity v3 and Coraza. Here is what we found:

| Behaviour | v2 | v3 | Coraza |
|---|---|---|---|
| `%{tx.missing}` (variable does not exist) | empty | empty | the text `tx.missing` |
| `setvar:'tx.x='` (empty value) | loads | **config fails to load** | **config fails to load** |
| leading space in a `setvar` value | removed | kept | kept |

Let's look at the first line. Our first idea was that each plugin appends to a shared variable:

```
setvar:'tx.plugin_allowed_methods=%{tx.plugin_allowed_methods} PROPFIND MKCOL'
```

On ModSecurity this works. On Coraza, the variable name itself ends up in the list of allowed methods:

```
GET HEAD POST OPTIONS tx.plugin_allowed_methods PROPFIND MKCOL
```

Ooops! And initializing the variable with an empty value doesn't help either, because then nginx with libModSecurity v3 and Coraza don't even start. (We reported the Coraza part in [corazawaf/coraza#1857](https://github.com/corazawaf/coraza/issues/1857).)

The lesson: test on all three engines. Always.

### The solution: one variable per plugin rule

The design we chose is simple: each plugin rule writes its **own** variable. The name contains the list and the ID of the rule:

```
tx.plugin_<list>_<rule id>
```

This is how a plugin like Nextcloud can allow WebDAV methods, only for its WebDAV endpoints:

```apache
SecRule REQUEST_FILENAME "@rx /(?:remote|public)\.php/dav/" \
    "id:9508190,\
    phase:1,\
    pass,\
    t:none,\
    nolog,\
    setvar:'tx.plugin_allowed_methods_9508190=|PROPFIND| |MKCOL| |MOVE| |COPY|'"
```

CRS then collects all these variables, directly after the defaults are set:

```apache
SecRule TX:/^plugin_allowed_methods_[0-9]+$/ "@rx \S" \
    "id:901600,\
    phase:1,\
    pass,\
    t:none,\
    nolog,\
    setvar:'tx.allowed_methods=%{tx.allowed_methods} %{MATCHED_VAR}'"
```

`TX:/regex/` selects every TX variable whose name matches, and the `setvar` runs once for each of them. So no plugin can overwrite another one, nobody has to initialize anything, and the CRS defaults and your own settings stay in place. There is one collect rule for each of the seven lists, 901600 to 901660.

One small detail cost us some thinking: the `_[0-9]+$` at the end of the regex is required. Without it, the rule for `allowed_request_content_type` would also collect the `allowed_request_content_type_charset` variables. Of course, our tests check this.

### The breaking change: methods and HTTP versions in pipes

While working on the contract, we looked at how 911100 checks the method:

```apache
SecRule REQUEST_METHOD "!@within %{tx.allowed_methods}"
```

`@within` checks for a **substring**. With the default list `GET HEAD POST OPTIONS`, the method `POS` was allowed, because it is part of `POST`. So were `OST`, `ET` and `T`. That's not what we want!

Content types never had this problem, because they are wrapped in pipes: `|application/json|`. Since CRS 4.31.0, methods and HTTP versions use the same format:

```
# before
setvar:'tx.allowed_methods=GET HEAD POST OPTIONS'
setvar:'tx.allowed_http_versions=HTTP/1.0 HTTP/1.1 HTTP/2 HTTP/2.0 HTTP/3 HTTP/3.0'

# since CRS 4.31.0
setvar:'tx.allowed_methods=|GET| |HEAD| |POST| |OPTIONS|'
setvar:'tx.allowed_http_versions=|HTTP/1.0| |HTTP/1.1| |HTTP/2| |HTTP/2.0| |HTTP/3| |HTTP/3.0|'
```

But the pipes in the list are only half of the fix: `POS` would still be found in `|POST|`. So rule 911100 now also wraps the request method in pipes before it checks it. `|POS|` is not part of `|POST|`, so only whole methods match:

```apache
SecRule REQUEST_METHOD "@rx ^.*$" \
    "id:911100,\
    phase:1,\
    block,\
    capture,\
    t:none,\
    setvar:'tx.request_method=|%{tx.0}|',\
    chain"
    SecRule TX:request_method "!@within %{tx.allowed_methods}" \
        "t:none,\
        setvar:'tx.inbound_anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```

Rule 920430 does the same for the HTTP version.

We first tried something else: padding the values with spaces (` POST `). But ModSecurity v2 removes leading spaces from `setvar` values (see the table above), and then `OST` matches `POST` again. Pipes are cleaner, and they work the same on all engines.

Thanks to Neha for the fix of rule 911100 ([#4960](https://github.com/coreruleset/coreruleset/pull/4960))! The HTTP versions and rule 920430 followed in [#4970](https://github.com/coreruleset/coreruleset/pull/4970).

**The message here is:** if you set `tx.allowed_methods` (rule 900200) or `tx.allowed_http_versions` (rule 900230) in your `crs-setup.conf`, you **must** switch to the pipe format when you upgrade. If you don't, nothing matches the old list, and **every request** is flagged by 911100 or 920430. If you never changed these two settings, you don't have to do anything.

### What plugin authors need to know

The full rules are in [PLUGIN-CONTRACT.md](https://github.com/coreruleset/coreruleset/blob/main/PLUGIN-CONTRACT.md), and there is a short how-to on the [Writing Plugins](https://coreruleset.org/docs/4-about-plugins/4-2-writing-plugins/) page. The most important points:

- Set your variables in your `-before.conf` file and in phase 1.
- Use the name `tx.plugin_<list>_<rule id>` and the format of the list: `|METHOD|`, `|type/subtype|`, `.ext/`, `/header-name/`.
- Write content types, charsets, extensions and header names in lowercase. Methods and HTTP versions use the exact case that is sent. An entry in the wrong case never matches, and CRS reports no error.
- Never change `tx.allowed_methods` and the other CRS lists directly.
- Limit your additions to the paths where they are needed.
- When you add a content type, also select the matching body processor (`JSON`, `XML` or `URLENCODED`). Otherwise the body is not parsed, and CRS can't see attacks in it. The only exception is a body without any structure, like a binary upload (`application/octet-stream`). Forcing a processor there makes parsing fail (`REQBODY_ERROR`). In this case, don't force a processor, and limit the addition as narrowly as possible (path, method and content type).

But what about plugins that also support the current LTS release? Older CRS releases don't have the collect rules, so they ignore the `tx.plugin_*` variables. For a transition period, these plugins may still set `tx.allowed_methods` directly, but only in the pipe format. Careful: such a plugin must never replace the list the administrator has configured. It only copies the CRS default if the variable is not set yet (`&TX:allowed_methods "@eq 0"`), and otherwise only appends its own methods, limited to the paths it covers. If a plugin overwrote the list, it could allow methods the administrator excluded on purpose. This works with both versions: the new 911100 compares whole entries, and the old one only checks for a substring, so `GET` is also found in `|GET|`. As soon as all supported CRS releases contain the contract, plugins switch to the `tx.plugin_*` variables.

That's exactly what we did for the three plugins that were affected: [Nextcloud](https://github.com/coreruleset/nextcloud-rule-exclusions-plugin/pull/180), [SOGo](https://github.com/EsadCetiner/sogo-rule-exclusions-plugin/pull/42) and [Plausible](https://github.com/EsadCetiner/plausible-rule-exclusions-plugin/pull/11). Their CI tests against CRS `main` and the LTS release, so we see right away if something breaks. If you maintain a plugin that sets `tx.allowed_methods`, please check it too!

**If you use one of these plugins:** with the current plugin versions, CRS 4.31.0 flags **every request**, because the plugins still write the method list in the old format. The fixes are on the way: as soon as new plugin releases are available, they work with CRS 4.31.0 and with the LTS release. So please wait for the new plugin release, update the plugin first and CRS afterwards. Until then, stay on CRS 4.30.0 or the LTS release.

### What the contract does not do

Plugins can only **add** entries. SecLang can't remove part of a string. So if a plugin needs to allow something that a `restricted_*` list blocks, it still needs a rule exclusion. For example, WebDAV clients send the `If` and `Lock-Token` headers, and both are in `tx.restricted_headers_basic`. The Nextcloud plugin keeps its narrow exclusion for rule 920450 for these requests.

### How we tested it

For the regression tests, CRS now has a small test plugin in `tests/regression/plugins/`. It follows the contract and only adds entries for a test path, so the thousands of other tests are not affected. The tests run on ModSecurity v2, libModSecurity v3 and Coraza in the CRS CI.

We also checked the tests the other way round: without the collect rules, every positive test fails. That's what tests are for!

### Conclusion

Plugins can now extend the CRS lists without copying the defaults, and the lists of methods and HTTP versions finally compare whole entries. The price is one breaking change in `crs-setup.conf`. But you only have to make it once, because all of this ships in the same release.

And personally: the most valuable part was not the final rule, but what we learned about the three engines on the way.

Thanks to Felipe ([@fzipi](https://github.com/fzipi)) for the design discussions, the decisions and the reviews, to Esad ([@EsadCetiner](https://github.com/EsadCetiner)), Jozef ([@azurit](https://github.com/azurit)) and Max ([@theseion](https://github.com/theseion)) for the discussion in the issue, and to Neha ([@Neha406-ui](https://github.com/Neha406-ui)) for the fix of rule 911100!

*I wrote this post and did the testing with the help of Claude (Anthropic). The design decisions were made together with the CRS team.*

### References

- https://github.com/coreruleset/coreruleset/issues/4286
- https://github.com/coreruleset/coreruleset/pull/4960
- https://github.com/coreruleset/coreruleset/pull/4970
- https://github.com/coreruleset/coreruleset/pull/4966
- https://github.com/coreruleset/coreruleset/blob/main/PLUGIN-CONTRACT.md
- https://github.com/corazawaf/coraza/issues/1857
- https://coreruleset.org/docs/4-about-plugins/4-2-writing-plugins/
