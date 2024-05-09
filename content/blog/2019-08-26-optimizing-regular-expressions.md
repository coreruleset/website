---
author: lifeforms
categories:
  - Blog
date: '2019-08-26T10:44:51+02:00'
title: How the CRS optimizes regular expressions
slug: 'optimizing-regular-expressions'
---


As many of you have noticed, the Core Rule Set contains very complex regular expressions. See for example [rule 942480](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf#L1234):

```text
(?i:(?:\b(?:(?:s(?:elect\b.{1,100}?\b(?:(?:(?:length|count)\b.{1,100}?|.*?\bdump\b.*)\bfrom|to(?:p\b.{1,100}?\bfrom|_(?:numbe|cha)r)|(?:from\b.{1,100}?\bwher|data_typ)e|instr)|ys_context)|in(?:to\b\W*?\b(?:dump|out)file|sert\b\W*?\binto|ner\b\W*?\bjoin)|...
```

These regular expressions are assembled from a list of simpler regular expressions for efficiency reasons. See [regexp-942480.data](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/util/regexp-assemble/regexp-942480.data) for the source expressions which were combined to form this expression.

A single optimized regular expression test takes much less time than a series of simpler regular expression tests. By combining related patterns in one rule, we lower our number of rules, which helps to keep the code base compact. The downside is readability and ease of development.

#### Regexp::Assemble

Manual assembly and optimization is both hard and error prone, so for the Core Rule Set we use a clever Perl Module: [Regexp::Assemble](https://metacpan.org/pod/Regexp::Assemble). As the name suggests, Regexp::Assemble knows how to assemble a number of regular expressions into one optimized regular expression.

Since Regexp::Assemble is not a program, but rather a Perl module, you will need some glue code to use it. The following instructions will help you if you are not Perl wizards.

If you don't have Perl, you will need to install it. The easiest Perl distribution to install on Windows is [ActivePerl](https://www.activestate.com/Products/activeperl/). For Unix-like systems, use your package manager.

Now install Regexp::Assemble. If you used ActivePerl, you can use the following command:

```sh
ppm install regexp-assemble
```

If you use another Perl distribution, the command will usually be:

```sh
cpan install Regexp::Assemble
```

#### Assembling a rule

Once you have Perl and Regexp::Assemble installed, all you need is a little script in our code repository under [util/regexp-assemble/regexp-assemble-v2.pl](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/util/regexp-assemble/regexp-assemble-v2.pl). On Unix-like systems, you can use it as follows:

```sh
cd util/regexp-assemble
./regexp-assemble-v2.pl regexp-942480.data
```

If your perl interpreter cannot be found, you may need to precede the script name with the command `perl`:

```sh
perl regexp-assemble-v2.pl regexp-942480.data
```

The script will take either standard input or an input file with each line containing a regular expression, and prints out the optimized expression.

#### Using the assembled expression

When you run the `regexp-assemble-v2.pl` script, hopefully a combined expression will be printed to your terminal.

You can then copy that optimized regular expression into the `.conf` rule file.

Also be sure to save the original expressions in the corresponding text file named `util/regexp-assemble/regexp-<em>ruleid</em>.data` where you replace `<em>ruleid</em>` by the rule number.

Finally, add a comment to the rule explaining how to re-assemble the expression from the source expressions. See [rule 942480](https://github.com/coreruleset/coreruleset/blob/v3.2/dev/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf#L1152) for an example.

*This blog was republished with permission from Ofer Shezaf ([original version](https://web.archive.org/web/20180822205124/http://blog.modsecurity.org/2007/06/optimizing-regu.html)) and modified to add our assemble script and notes for contributors.*
