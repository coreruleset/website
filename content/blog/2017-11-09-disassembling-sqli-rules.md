---
author: franbuehler
categories:
  - Blog
date: '2017-11-09T14:30:37+01:00'
title: Disassembling SQLi Rules
---

## Introduction

I would like to explain my work disassembling highly optimized regular expressions. A project like this might discourage many people, but to me, it is very exciting work! I like this kind of investigative work and want to explain what, exactly, I did, why I did it and how!

## What's the problem?

The SQLi rules in the core rule set consist of 43 rules. 25 of them have been optimized with the [Perl module Regexp::Assemble](https://metacpan.org/pod/Regexp::Assemble). This module assembles multiple regular expressions into one regular expression.  
The source patterns were lost over the years as they were taken from the old CRS project and partly from other projects, and source code management migrations led to the situation we are facing now.  
Unfortunately, there is no tool for disassembling an optimized regex, so we did not have a chance to undo this optimization process and regain the original patterns.

## Why are the optimized patterns a problem?

An optimized regex without its original source regex can not be maintained.  
We had to update an SQLi rule because of a false positive, but we did not understand the regex or even know which part of the regex caused the false positive. Another problem was that some of the rules were manually expanded and mistakes were made.  
How do you update a regex that you do not understand? There's no way! This would mean that the rules are no longer maintained and extended. That would be really bad! It's also very bad for an open source project and its maintainability to have incomprehensible regexes. On top of it, there were complaints from people who said they would not install CRS. They were reluctant to install rules they could not understand.

I encountered this long-running problem when [@lifeforms](https://github.com/lifeforms) reported a false positive in rule [942410](https://github.com/coreruleset/coreruleset/blob/v3.0/master/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf#L934). See [Github issue 761](https://github.com/coreruleset/coreruleset/issues/761).

This was the rule before my work:

{{< highlight "apacheconf" >}}
SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|!REQUEST_COOKIES:/_pk_ref/|REQUEST_COOKIES_NAMES|ARGS_NAMES|ARGS|XML:/* "(?i:(?:(?:s(?:t(?:d(?:dev(_pop|_samp)?)?|r(?:_to_date|cmp))|u(?:b(?:str(?:ing(_index)?)?|(?:dat|tim)e)|m)|e(?:c(?:_to_time|ond)|ssion_user)|ys(?:tem_user|date)|ha(1|2)?|oundex|chema|ig?n|pace|qrt)|i(?:s(null|_(free_lock|ipv4_compat|ipv4_mapped|ipv4|ipv6|not_null|not|null|used_lock))?|n(?:et6?_(aton|ntoa)|s(?:ert|tr)|terval)?|f(null)?)|u(?:n(?:compress(?:ed_length)?|ix_timestamp|hex)|tc_(date|time|timestamp)|p(?:datexml|per)|uid(_short)?|case|ser)|l(?:o(?:ca(?:l(timestamp)?|te)|g(2|10)?|ad_file|wer)|ast(_day|_insert_id)?|e(?:(?:as|f)t|ngth)|case|trim|pad|n)|t(?:ime(stamp|stampadd|stampdiff|diff|_format|_to_sec)?|o_(base64|days|seconds|n?char)|r(?:uncate|im)|an)|m(?:a(?:ke(?:_set|date)|ster_pos_wait|x)|i(?:(?:crosecon)?d|n(?:ute)?)|o(?:nth(name)?|d)|d5)|r(?:e(?:p(?:lace|eat)|lease_lock|verse)|o(?:w_count|und)|a(?:dians|nd)|ight|trim|pad)|f(?:i(?:eld(_in_set)?|nd_in_set)|rom_(base64|days|unixtime)|o(?:und_rows|rmat)|loor)|a(?:es_(?:de|en)crypt|s(?:cii(str)?|in)|dd(?:dat|tim)e|(?:co|b)s|tan2?|vg)|p(?:o(?:sition|w(er)?)|eriod_(add|diff)|rocedure_analyse|assword|i)|b(?:i(?:t_(?:length|count|x?or|and)|n(_to_num)?)|enchmark)|e(?:x(?:p(?:ort_set)?|tract(value)?)|nc(?:rypt|ode)|lt)|v(?:a(?:r(?:_(?:sam|po)p|iance)|lues)|ersion)|g(?:r(?:oup_conca|eates)t|et_(format|lock))|o(?:(?:ld_passwo)?rd|ct(et_length)?)|we(?:ek(day|ofyear)?|ight_string)|n(?:o(?:t_in|w)|ame_const|ullif)|(rawton?)?hex(toraw)?|qu(?:arter|ote)|(pg_)?sleep|year(week)?|d?count|xmltype|hour)\W*?\(|\b(?:(?:s(?:elect\b(?:.{1,100}?\b(?:(?:length|count|top)\b.{1,100}?\bfrom|from\b.{1,100}?\bwhere)|.*?\b(?:d(?:ump\b.*?\bfrom|ata_type)|(?:to_(?:numbe|cha)|inst)r))|p_(?:sqlexec|sp_replwritetovarbin|sp_help|addextendedproc|is_srvrolemember|prepare|sp_password|execute(?:sql)?|makewebtask|oacreate)|ql_(?:longvarchar|variant))|xp_(?:reg(?:re(?:movemultistring|ad)|delete(?:value|key)|enum(?:value|key)s|addmultistring|write)|terminate|xp_servicecontrol|xp_ntsec_enumdomains|xp_terminate_process|e(?:xecresultset|numdsn)|availablemedia|loginconfig|cmdshell|filelist|dirtree|makecab|ntsec)|u(?:nion\b.{1,100}?\bselect|tl_(?:file|http))|d(?:b(?:a_users|ms_java)|elete\b\W*?\bfrom)|group\b.*?\bby\b.{1,100}?\bhaving|open(?:rowset|owa_util|query)|load\b\W*?\bdata\b.*?\binfile|(?:n?varcha|tbcreato)r|autonomous_transaction)\b|i(?:n(?:to\b\W*?\b(?:dump|out)file|sert\b\W*?\binto|ner\b\W*?\bjoin)\b|(?:f(?:\b\W*?\(\W*?\bbenchmark|null\b)|snull\b)\W*?\()|print\b\W*?\@\@|cast\b\W*?\()|c(?:(?:ur(?:rent_(?:time(?:stamp)?|date|user)|(?:dat|tim)e)|h(?:ar(?:(?:acter)?_length|set)?|r)|iel(?:ing)?|ast|r32)\W*?\(|o(?:(?:n(?:v(?:ert(?:_tz)?)?|cat(?:_ws)?|nection_id)|(?:mpres)?s|ercibility|alesce|t)\W*?\(|llation\W*?\(a))|d(?:(?:a(?:t(?:e(?:(_(add|format|sub))?|diff)|abase)|y(name|ofmonth|ofweek|ofyear)?)|e(?:(?:s_(de|en)cryp|faul)t|grees|code)|ump)\W*?\(|bms_\w+\.\b)|(?:;\W*?\b(?:shutdown|drop)|\@\@version)\b|\butl_inaddr\b|\bsys_context\b|'(?:s(?:qloledb|a)|msdasql|dbo)'))"
{{< /highlight >}}

That's scary, isn't? How can you figure out this regex within a reasonable period of time?  
I like detective work, so I started disassembling the optimized regex to find out where I could eliminate the false positive. I succeeded and wrote the source of the regex in util/regexp-assemble/regexp-942410.data. This means that from now on, we can easily update the source patterns and rebuild the optimized regex.  
After updating this rule to avoid this false positive, I was hooked and the other contributors asked me to update ALL optimized regexes. Needless to say, I agreed immediately.

## How did I do it?

I worked in vim and with keen eyes. I hopped from bracket to bracket and typed one letter behind the other.
Let's look at the example of rule 942150:  
```apacheconf
SecRule MATCHED_VARS "@rx (?i)\b(?:c(?:o(?:n(?:v(?:ert(?:_tz)?)?|cat(?:_ws)?|nection_id)|(?:mpres)?s|ercibility|(?:un)?t|llation|alesce)|ur(?:rent_(?:time(?:stamp)?|date|user)|(?:dat|tim)e)|h(?:ar(?:(?:acter)?_length|set)?|r)|iel(?:ing)?|ast|r32)| ... )\W*\("
```

Let's start at the beginning of the regex: `(i)\b(`. We see an ignore case flag for the whole regex and a word boundary. Our work begins with the opening bracket. This is a relatively simple example because the corresponding closing bracket for this first opening bracket is right at the end of the regex. A `\W*\(` follows the closing bracket, which stands for no or multiple non-word characters and an opening bracket. This means all of the alternatives that we find will end with this pattern. That's the first important finding.  
We now proceed: We take the `c`, the `o`, the `n`, the `v`, the `ert` and the `_tz` and now reach a `|` operator. That means we have our first word: `convert_tz`.  
We now move back again because we have some question marks after the closing brackets. This means that `convert` and even `conv` are also valid alternatives.  
We then move behind the `|` to find more alternatives. Since we are still in the `con(` bracket, we now find the words `concat_ws`. And because of the question mark, `concat` is a valid word as well. After the next `|`, we find `connection_id`.  
So far we have found the following alternatives:
```
\bconv\W*\(
\bconvert\W*\(
\bconvert_tz\W*\(
\bconcat\W*\(
\bconcat_ws\W*\(
\bconnection_id\W*\(`
```

Remember, these start with a `\b` and end with the mentioned `\W*\(`

Now we leave the `con(` bracket and move up to the `co(` bracket, where we take apart the next regexes. And so on. It's basically a routine piece of work.

Two things are important: You always have to know which bracket you are currently working in. And secondly, which letter is in front and at the end of this bracket.  
Many hours later, the work is done and I have created the following files in the folder [util/regexp-assemble](https://github.com/coreruleset/coreruleset/tree/v3.1/dev/util/regexp-assemble):`
regexp-942120.data
regexp-942130.data
regexp-942140.data
regexp-942170.data
regexp-942180.data
regexp-942190.data
regexp-942200.data
regexp-942210.data
regexp-942240.data
regexp-942260.data
regexp-942280.data
regexp-942300.data
regexp-942310.data
regexp-942320.data
regexp-942330.data
regexp-942340.data
regexp-942350.data
regexp-942360.data
regexp-942370.data
regexp-942380.data
regexp-942390.data
regexp-942400.data
regexp-942410.data
regexp-942470.data
regexp-942480.data
`

I want to thank the CRS community for their tests! [@dune73](https://github.com/dune73) ran fairly big tests against the optimized rules and found two behavioral changes. [@lifeforms](https://github.com/lifeforms) has done some testing with sqlmap and his own written tests. He found three errors. [@emphazer](https://github.com/emphazer) manually checked the output of Regexp::Assemble line by line via diff and found four small but important errors such as a `)` instead of a `]`. I was able to eliminate these errors relatively quickly.  
I did face some problems during my work: Some regexes were not optimized at all.  
Or, for special regular expressions, the Regexp::Assemble module doesn't work correctly. For example, the regex `\(?` is optimized to `\(\?` and `(a)(b)\2` is optimized to `(a)(b)2`. We have bypassed these bugs by using `[(]?` instead of `\(?` and `(a)(b)(?:\2)` instead of `(a)(b)2`.  
Finally, one optimization process created an ugly output due to its optimization method. The optimization process works from the beginning to the end of the pattern, regardless of whether the optimization would be better starting at the end of the pattern or not. The workaround was to pre-optimize the regex in the source file already.  
The bottom line is that we now have optimized regexes that are easier to read.

**Future work**  
The work is not finished yet. Because 'complexity is the enemy of security,' we've laid an important cornerstone by disassembling the rules. Because the SQLi rules are understandable, the CRS community can now reorganize them. We can remove redundancies, discover holes in the coverage and consolidate and optimize the rules.  
Outside of the SQLi rules, there are about 10 rules that could be disassembled as well.  
This further development is very important, as it will bring better performance and hopefully even better detection rates than we currently have.  
If you are interested in helping us enhance the CRS, [your help is very welcome]({{< ref "blog/2017-09-13-how-you-can-help-the-crs-project.md" >}})!
