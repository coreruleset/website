---
author: dune73
categories:
  - Blog
date: '2021-01-06T12:25:13+01:00'
excerpt: This blog post is about msc_retest, a small family of tools that let you performance test the regular expression engine used inside various ModSecurity versions. As of this writing, the engine is PCRE, but we expect more options in the future.
tags:
  - Ervin Hegedüs
  - msc_retest
  - performance
title: Introducing msc_retest
---

Debugging CRS and more generally debugging ModSecurity can be nasty. False Positives are the worst, but also nagging performance problems can spoil the fun. Sometimes you have network problems or the whole architecture is botched. But equally often it's simply your server or ModSecurity that's misbehaving.

This blog post is about msc\_retest, a small family of tools that lets you performance test the regular expression engine used inside various ModSecurity versions. As of this writing, the engine is PCRE everywhere, but we expect more options in the future.

## What is the problem?

In my [tutorials over at netnea.com](https://www.netnea.com/cms/apache-tutorials/) I am advocating adding performance data to the access log in order to do proper statistics and to get data on the performance of individual requests over time ([Tutorial 5: Extending and Analyzing the Access Log](https://www.netnea.com/cms/apache-tutorials/apache-tutorial-5_extending-access-log/)). That is the macro view if you will. The micro view is the performance of an individual regular expression against a single payload or a series of parameters.

The ModSecurity debug log, namely the one for ModSecurity 2.x, brings detailed performance information for an individual execution. That can be put to good use, but it's a bit cumbersome to extract the information and also slowing down production servers.

With ModSecurity, there is a compile time option that lets you instruct the binary to execute every regular expression n times in series. This is very neat when you want to compare different scenarios or test regular expressions on a dev machine, but it's still cumbersome to perform such a test. See the [ModSecurity Handbook, 2ed](https://www.feistyduck.com/books/modsecurity-handbook/), p. 202f for more infos.

## What is the solution?

A more handy alternative comes in the form of a family of scripts by CRS developer [Ervin Hegedüs](https://twitter.com/IamAirWeen) from Hungarian [digitalwave](https://www.digitalwave.hu/en/services/modsecurity), who has delivered [msc\_pyparser](https://coreruleset.org/20200901/introducing-msc_pyparser/) before.

The script or rather two scripts come in a repository anmed [msc\_retest](https://github.com/digitalwave/msc_retest). They mimic the regular expression behavior of ModSecurity2 and - 2nd script - the behavior of ModSecurity3. This lets you assess the performance of regular expressions. It is particularly interesting, when you want to compare different versions of the same regular expression. This is about questions such as "Which version is faster?" and "How does it play out across different payloads?"

### How do you install the package?

Here is how I installed it:

Download:

```sh
$> git clone https://github.com/digitalwave/msc_retest.git
```

Prepare configure:

```sh
$> autoreconf --install
```

Run configure:

```sh
$> configure
```

Compilation:

```sh
$> make
```

Installation:

```sh
$> sudo make install
```

### How do you use it?

As previously mentioned, there are two tools, pcre4msc2 and pcre4msc3 in this package. One is used to assess regular expression performance of the stable ModSecurity 2.9.x implementation. The other one imitates the newer ModSecurity 3.x / libModSecurity 3.x.

Here is a basic call with the ModSec2 variant:

```sh
$> echo "foo" > pattern.txt
$> echo "hello fool" | pcre4msc2 pattern.txtpattern.txt - time elapsed: 0.000012, match value: SUBJECT MATCHED 1 TIME
```

So the execution of the regular expression took 12 microseconds and brought one match.

This is really simple.

There are a few command line options for both variants. With pcre4msc2, the use of the PCRE JIT compiler is off by default. Enable it with `-j` to make use of it, if you have it available. In pcre4msc3, this is on by default.

In fact the PCRE JIT compiler makes quite a different for raw regular expression execution. It is not enabled in most Linux distribution packages, but if you compile ModSecurity 2.9.x yourself, then the configure option --enable-pcre-jit is worth a try. With JIT, ModSecurity will study the regular expression at config time of the server. That is surprisingly useful in terms of performance.

The script pcre4msc3 has a flag -f that behaves like the off the shelf versions of ModSecurity 3.0.0 - 3.0.4. The problem is these version suffer from a bad implementation of the regular expression operator that leads to a big Denial of Service problem: [CVE-2020-15598](https://coreruleset.org/20200914/cve-2020-15598/). When we released this advisory, we advocated to patch ModSecurity 3 in order to fix the problem. Several Linux distributions followed suit, but you may want to check this yourself. Unfortunately, Trustwave did not release a new version of the software themselves.

But anyways, the default for pcre4msc3 is to use a sane implementation and the broken, but official implementation, can be called via the -f flag.

Furthermore, both scripts have a -d option that brings more debug output.

```
<pre class="wp-block-preformatted">$> echo "hello fool" | pcre4msc2 -d -j pattern.txt
RAW pattern:
============
foo

ESCAPED pattern:
===============
foo

SUBJECT:
=========
hello fool

JIT:
====
available and enabled

STUDY:
=======
enabled

MATCH LIMIT:
============
1000

MATCH LIMIT RECURSION:
======================
1000

RESULT:
=======
pattern.txt - time elapsed: 0.000006, match value: SUBJECT MATCHED 1 TIME

CAPTURES:
==========
hello fool

OVECTOR:
=========
[6, 9]
```

There are various important pieces of information in this output. The match limits for example define the limits that you define in ModSecurity 2 with SecPcreMatchLimit and SecPcreMatchLimitRecursion. Also the escaped pattern can be important, since it will tell you how the tool looked at quotes and their escaping backslashes (important on the command line since you want to be sure you end up with the same RegEx as ModSecurity and also with ModSecurity v3 which has a tendency to be a bit sloppy with escapes).  
  
Finally, there is an option in both scripts that lets you execute it n times in series:

```sh
$> echo "hello fool" | pcre4msc2 -n 10 -j pattern.txt
pattern.txt - time elapsed: 0.000007, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000001, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000001, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000000, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000000, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000001, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000001, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000001, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000000, match value: SUBJECT MATCHED 1 TIME
pattern.txt - time elapsed: 0.000000, match value: SUBJECT MATCHED 1 TIME
```

As you can see, the first execution takes substantially longer than the subsequent ones. It's the same on the webserver. So if you want to have hard data, execution in a loop like this is mandatory. What is not so nice is that the calls were so fast, the elapsed time is reported as zero. That is of course not the case, but it points to the fact, that microseconds are not granular enough to measure the time, at least not on my machine. Ervin is currently adding support for timing in nanoseconds. That should definitely do the trick in this regard.

## Practical use case

Let's try to do a real world use case with this script. We're looking at the Core Rule Set pull request [1868](https://github.com/coreruleset/coreruleset/pull/1868). This pull request updates the regular expression in rule [920120](https://github.com/coreruleset/coreruleset/blob/v3.4/dev/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf#L98). The rule tries to detect a potential impedance mismatch in multipart file uploads. In the filename field of the upload to be exact. (In WAF speak, an *impedance mismatch* is the WAF parsing a payload differently from the backend. It's a way to steer around the WAF and still exploit the backend.)

We used to do this rule with a nifty negative-look-behind regular expression. Unfortunately, look-around regexes are PCRE specific. So when you look into replacing PCRE for your WAF engine, then this is a potential roadblock. We are thus in a process to replace all regexes that make use of this specialty. Now look-around is here for a reason of course. It allows us to express something in a simple way and if we can no longer express this, we need to run a far more complicated alternative regular expression.

Adding to the paradox: Replacing PCRE with an alternative rule engine like RE2 or Hyperscan is far and foremost a performance thing. PCRE is relatively slow, the alternatives are faster. However, when it comes to look-around it's the other way around. Look-around is a faster way of expressing something on PCRE.

To sum this up: We are looking to replace a look-around dialect expression so people can use a faster regular expression engine (the WAF permitting), but we do not want to cripple the PCRE use case with a slow regular expression. And on top, the new regular expression should cover the same exploits.

Let me sum this up. Here is the old regular expression:

```
(?<!&(?:[aAoOuUyY]uml)|&(?:[aAeEiIoOuU]circ)|&(?:[eEiIoOuUyY]acute)|&(?:[aAeEiIoOuU]grave)|&(?:[cC]cedil)|&(?:[aAnNoO]tilde)|&(?:amp)|&(?:apos));|['\"=]
```

This uses a negative-look-behind (-&gt; see the *?&lt;!* at the beginning of the regex) that we want to avoid.

And we here is the new rule proposed in the pull request:

```
(?:(?:^|[^lceps])|(?:^|[^mi])l|(?:^|[^r])c|(?:^|[^tvd])e|(?:^|[^m])p|(?:^|[ô])s|(?:^|[û])ml|(?:^|[î])rc|(?:^|[û])te|(?:^|[â])ve|(?:^|[^d])il|(?:^|[^l])de|(?:^|[â])mp|(?:^|[^p])os|(?:^|[âAoOuUyY])uml|(?:^|[^c])irc|(?:^|[^c])ute|(?:^|[^r])ave|(?:^|[ê])dil|(?:^|[î])lde|(?:^|[^&])amp|(?:^|[â])pos|(?:^|[^&])[aAoOuUyY]uml|(?:^|[âAeEiIoOuU])circ|(?:^|[â])cute|(?:^|[^g])rave|(?:^|[^c])edil|(?:^|[^t])ilde|(?:^|[^&])apos|(?:^|[^&])[aAeEiIoOuU]circ|(?:^|[êEiIoOuUyY])acute|(?:^|[âAeEiIoOuU])grave|(?:^|[^cC])cedil|(?:^|[âAnNoO])tilde|(?:^|[^&])[eEiIoOuUyY]acute|(?:^|[^&])[aAeEiIoOuU]grave|(?:^|[^&])[cC]cedil|(?:^|[^&])[aAnNoO]tilde);|['\"=]
```

That does more or less the same thing, but it's substantially more complex.

Our job is now to check out the performance of the two variants. And since this is a blog post and I want to do this in a clean way, we are going to check against ModSec2 with JIT, ModSec2 without JIT and the patched ModSec3. You can argue that I should test against the broken but widespread ModSec3 too, but that's not worth it, since any difference very much depends on the payload and we have already established the fact, that the stock ModSec3 is affected by the severe vulnerability CVE-2020-15598.

I want to run a few thousands of matches with this. To get some close-to-real-world data, I am going to use the following file names; all found on my local machine with the exception of the last one. The last one is meant to trigger the rule. It's taken from the unit tests of the rule.

```
525-190160_Example_Offerte_11-02-2019.docx
Rahmenvertrag ZZZ 2015-2017.pdf
Eintragung der Übertragung.pdf
Sammelbestellung Example - Tranche 2.xlsx
20160504Contract_Abcdef_FooBar_Challenge_Abcede (mit 1 Signatur).pdf
Analysis-and-Architecture.odt
Cybersecurity-Book-full-book.pdf
IdNumbering.csv
ZZZ_Kommunikationsvorgehen_V.02.docx
zzz&auml;zzz
```

Here is my script to execute the tests. It runs 10 times 100K requests for every parameter with every invocation of the script. I think this is better than doing a single run with 1M calls, since it balances out the execution on a multi-user system with a ton of tasks in the background (and you never know what the host is doing).

```sh
for I in {1..10}; do
  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc2 -n 100000 old-regex.txt; done >> modsec2-nojit-old-pattern.txt
  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc2 -n 100000 new-regex.txt; done >> modsec2-nojit-new-pattern.txt
  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc2 -n 100000 -j old-regex.txt; done >> modsec2-withjit-old-pattern.txt
  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc2 -n 100000 -j new-regex.txt; done >> modsec2-withjit-new-pattern.txt

  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc3 -n 100000 old-regex.txt; done >> modsec3-withjit-old-pattern.txt
  cat filenames.txt | while read FILENAME; do echo "$FILENAME" | pcre4msc3 -n 100000 new-regex.txt; done >> modsec3-withjit-new-pattern.txt
done
```

This results in a file with 10 million executions each. For the analysis, I am simply summing up the elapsed time. You could argue, that mean or median would be more useful, but the numbers can be very small, and they are easier to read without dividing them by one million.

Here you are:

```bash-session
$> ls modsec2-nojit-old-pattern.txt modsec2-nojit-new-pattern.txt modsec2-withjit-old-pattern.txt modsec2-withjit-new-pattern.txt modsec3-withjit-old-pattern.txt modsec3-withjit-new-pattern.txt | while read F; do printf "%32s : %f\n" "$F" $(egrep -o "[0-9]+\.[0-9]{6}" $F | awk "{ SUM += \$1 } END { print SUM }"); done

   modsec2-nojit-new-pattern.txt : 630.129000
   modsec2-nojit-old-pattern.txt : 1.014460
 modsec2-withjit-new-pattern.txt : 38.511100
 modsec2-withjit-old-pattern.txt : 0.937687
 modsec3-withjit-new-pattern.txt : 56.225600
 modsec3-withjit-old-pattern.txt : 5.979850
```

Let's put this in a more comprehensive form:

```
                                OLD REGEX    NEW REGEX
   modsec2-nojit-pattern.txt :   1.014460   630.129000
 modsec2-withjit-pattern.txt :   0.937687    38.511100
 modsec3-withjit-pattern.txt :   5.979850    56.225600
```

I am astonished by the difference that JIT is making on ModSec2. Not so much with the old pattern. But with the more complex new pattern, it's quite staggering. I have to admit that I underestimated the big role JIT is playing. The fact that ModSec3 is nowhere near ModSec2 in terms of throughput is no surprise though. [We have been aware of this for several years.](https://github.com/SpiderLabs/ModSecurity/issues/1734) The good news here is that the difference between the old and the new regex is not so big on ModSec3.

The biggest difference is between the old and the new pattern though. It's a huge difference for this particular use case. But we also need to put it in perspective. It's one of the last cases of PCRE dialect in CRS. So getting rid of the old pattern would be really welcome. It's also only one of 200 rules, so it's being leveled out with the other rules. The big factor, however, is the rarity of this regular expression being invoked. In fact, this is only applied on the ModSecurity collections FILES and FILES\_NAMES. These variables are only filled for multipart file uploads. On almost all servers, this is only a small fraction of requests, since most requests will always be GET requests on a standard web server. So despite the big performance difference when putting the regular expressions side by side, there is not much change for the entire WAF. But it's good to know it nevertheless. Thanks to msc\_retest.

A happy new year to you!

Christian Folini with a lot of support by Ervin Hegedüs
