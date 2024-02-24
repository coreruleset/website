---
author: amonachesi
categories:
  - Blog
date: '2023-02-22T22:01:07+01:00'
guid: https://coreruleset.org/?p=2062
id: 2062
permalink: /20230222/a-new-rule-to-prevent-sql-in-json/
title: A new rule to prevent SQL in JSON
url: /2023/02/22/a-new-rule-to-prevent-sql-in-json/
---


Team82 has published an exciting research article about bypassing web application firewalls using a specific SQL syntax that uses JSON. More information about their research can be found [here](https://claroty.com/team82/research/js-on-security-off-abusing-json-based-sql-to-bypass-waf).

An example payload described by Team82 could be:

```
<pre class="wp-block-code">```
1 OR JSON_EXTRACT('{"foo":1}','$.foo')=1
```
```

<figure class="wp-block-image size-full">![](/images/2023/02/SQL-in-JSON.png)</figure>The OWASP Core Rule Set is blocking all payloads reported by Team82 at paranoia level 2 basically just with the rule `942110 "SQL Injection Attack: Common Injection Testing Detected"`.

Though blocking this at paranoia level 2 is great, we decided to define a new rule to block all “JSON in SQL” payloads at the default level (paranoia level 1). More information about the new rule can be reached by visiting the related [pull request page on the CRS GitHub repository](https://github.com/coreruleset/coreruleset/pull/3055).

If you are a fan of bash one line, you can download the new rule by copying and pasting the following command:

```
<pre class="wp-block-code">```
curl -s 'https://raw.githubusercontent.com/coreruleset/coreruleset/v4.0/dev/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf' | grep -Pzo '(?s)\n[#] This rule tries to match JSON SQL.*JSON-Based SQL Injection.*?"\n\n' 
```
```

Or you can copy and paste the new rule from here:

```
<pre class="wp-block-code">```
# This rule tries to match JSON SQL syntax that could be used as a bypass technique.
# Referring to this research: https://claroty.com/team82/research/js-on-security-off-abusing-json-based-sql-to-bypass-waf
#
# Regular expression generated from regex-assembly/942550.ra.
# To update the regular expression run the following shell script
# (consult https://coreruleset.org/docs/development/regex_assembly/ for details):
#   crs-toolchain regex update 942550
#
SecRule REQUEST_FILENAME|REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|ARGS_NAMES|ARGS|XML:/* "@rx [\"'`][\[\{].*[\]\}][\"'`].*(::.*jsonb?)?.*(?:(?:@|->?)>|<@|\?[&\|]?|#>>?|[<>]|<-)|(?:(?:@|->?)>|<@|\?[&\|]?|#>>?|[<>]|<-)[\"'`][\[\{].*[\]\}][\"'`]|json_extract.*\(.*\)" \
    "id:942550,\
    phase:2,\
    block,\
    t:none,t:urlDecodeUni,t:lowercase,t:removeWhitespace,\
    msg:'JSON-Based SQL Injection',\
    logdata:'Matched Data: %{TX.0} found within %{MATCHED_VAR_NAME}: %{MATCHED_VAR}',\
    tag:'application-multi',\
    tag:'language-multi',\
    tag:'platform-multi',\
    tag:'attack-sqli',\
    tag:'OWASP_CRS',\
    tag:'capec/1000/152/248/66',\
    tag:'PCI/6.5.2',\
    tag:'paranoia-level/1',\
    ver:'OWASP_CRS/4.0.0-rc1',\
    severity:'CRITICAL',\
    setvar:'tx.sql_injection_score=+%{tx.critical_anomaly_score}',\
    setvar:'tx.inbound_anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```
```

#### Basic SQLi Challenge

We're constantly working on our sandbox, and since this new bypass has come out we have created a few SQL Injection vulnerable applications to test our ruleset against new bypass techniques.

If you want to test the OWASP Core Rule Set against SQL Injection payloads, you can use the following challenges we’ve prepared:

**MySQL**   
[SQL Injection in querystring parameter](https://sandbox.coreruleset.org/challenges/php-sqli-01/?id=(1%2b1))  
[SQL Injection in URI path](https://sandbox.coreruleset.org/challenges/php-sqli-02/index.php/(1%2b1))

**PostgreSQL**  
[SQL Injection in querystring parameter](https://sandbox.coreruleset.org/challenges/php-sqli-03/?id=(1%2b1))  
[SQL Injection in URI path](https://sandbox.coreruleset.org/challenges/php-sqli-04/index.php/(1%2b1))

#### Examples

We take every bypass seriously, but we expect bypasses at the default paranoia level. So, if you want to test your payloads at higher paranoia levels, you could send specific headers as described in the sandbox documentation [here](https://coreruleset.org/docs/development/sandbox/).

This is an example of a request using paranoia level 2:

```
<pre class="wp-block-code">```
curl 'https://sandbox.coreruleset.org/challenges/php-sqli-01/?id=1+OR+1=1--' \
   -H 'x-format-output: txt-matched-rules' \
   -H 'x-crs-paranoia-level: 2' 
942100 PL1 SQL Injection Attack Detected via libinjection
942130 PL2 SQL Injection Attack: SQL Boolean-based attack detected
942390 PL2 SQL Injection Attack
949110 PL1 Inbound Anomaly Score Exceeded (Total Score: 15)
```
```

#### Timeline

- December 8h, 2022: Team82 publishes the bypass
- December 9, 2022: OWASP CRS Team starts testing the bypass against the nightly version
- December 12, 2022: OWASP CRS creates the first draft of a new PL1 rule to detect the bypass
- December 14, 2022: OWASP CRS merges the new rule
