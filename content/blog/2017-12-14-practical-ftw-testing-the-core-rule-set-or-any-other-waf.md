---
author: Christian Folini
categories:
  - Blog
date: '2017-12-14T09:40:01+01:00'
guid: https://coreruleset.org/?p=616
id: 616
permalink: /20171214/practical-ftw-testing-the-core-rule-set-or-any-other-waf/
site-content-layout:
  - default
site-sidebar-layout:
  - default
tags:
  - ftw
  - testing
theme-transparent-header-meta:
  - default
title: 'Practical FTW: Testing the Core Rule Set or Any Other WAF'
url: /2017/12/14/practical-ftw-testing-the-core-rule-set-or-any-other-waf/
---


Back in August and September, Chaim Sanders [introduced](https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released/) [FTW](https://coreruleset.org/20170915/writing-ftw-test-cases-for-owasp-crs/), a Framework to Test WAFs via two blost posts. Existing unit testing frameworks are not really suitable for this purpose as they do not grant you enough control over the requests and the ability to look at the WAF log that needs to be bolted on. Chaim teamed with Zack Allen and Christian Peron from Fastly to create this. So FTW was developed with exactly our use case in mind. Time to really understand this and to start using it.

Chaim's two blog posts address the inner working of the software. He described the YAML format used to define the tests, but I somehow missed the user perspective: How do I install and run this? So that's the goal of this blog post.

### Installation and First Call

We will be working with virtualenv and so you need to install this as a pre-requisite. I did a standard

```
sudo apt-get install virtualenv
```

to settle this. Then you are ready for ftw. You can install ftw via pypi / pip or clone it from github. But that is only when you want to develop FTW yourself. If you just want to run the tests for CRS, it is all there included with the 3.1 development tree (the 3.0 release line does not have the tests, better work on the dev tree instead).

So here is what works for me:

```
$> git clone https://github.com/coreruleset/coreruleset.git
...
$> cd owasp-modsecurity-crs
$> git checkout v3.1/dev
Branch v3.1/dev set up to track remote branch v3.1/dev from origin.
Switched to a new branch 'v3.1/dev'
$> cd util/regression-tests/
$> virtualenv env && source env/bin/activate
Running virtualenv with interpreter /usr/bin/python2
New python executable in /tmp/owasp-modsecurity-crs/env/bin/python2
Also creating executable in /tmp/owasp-modsecurity-crs/env/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
```

```
(env) $> pip install -r requirements.txt
Collecting ftw==1.1.0 (from -r requirements.txt (line 1))
Collecting python-dateutil==2.6.0 (from ftw==1.1.0->-r requirements.txt (line 1))
Using cached python_dateutil-2.6.0-py2.py3-none-any.whl
Collecting pytest==2.9.1 (from ftw==1.1.0->-r requirements.txt (line 1))
Using cached pytest-2.9.1-py2.py3-none-any.whl
Collecting PyYAML (from ftw==1.1.0->-r requirements.txt (line 1))
Collecting IPy (from ftw==1.1.0->-r requirements.txt (line 1))
Collecting six>=1.5 (from python-dateutil==2.6.0->ftw==1.1.0->-r requirements.txt (line 1))
Using cached six-1.11.0-py2.py3-none-any.whl
Collecting py>=1.4.29 (from pytest==2.9.1->ftw==1.1.0->-r requirements.txt (line 1))
Using cached py-1.4.34-py2.py3-none-any.whl
Installing collected packages: six, python-dateutil, py, pytest, PyYAML, IPy, ftw
Successfully installed IPy-0.83 PyYAML-3.12 ftw-1.1.0 py-1.4.34 pytest-2.9.1 python-dateutil-2.6.0 six-1.11.0
```

The first few commands are used to get the right CRS source code tree. FTW starts with the virtualenv directive. This step plays around with your paths and environment to make sure you can run this project without any python / library / package / path hassles. The activate file that we source has more of this and also a deactivate shell function that allows us to quit the environment again (Just type deactivate at the prompt and you leave the virtual environment).

The next line from above brings the pip command to install the required packages into the local file tree. This will blow it up to over 20 megabytes. We're almost there now, but let's review the config.py file to make sure the base configuration is OK. The default installation is assumes the server error log at /var/log/httpd/error\_log and the default time stamp in that log. If that is not the case, you need to adopt it. Here is my config.py that expects the log at /apache/logs/error.log (I am allowed to this, it's a lab setup :)) and a reverse order timestamp format as introduced in my [tutorial over at netnea.com](https://www.netnea.com/cms/apache-tutorial-2_minimal-apache-configuration/). We'll come back to this further down below.

And then we start the CRS equipped webserver on localhost and call FTW for the first time!

```
(env) $> py.test CRS_Tests.py --ruledir=tests

===================================================================== test session starts =====================================================================
 platform linux2 -- Python 2.7.12+, pytest-2.9.1, py-1.4.34, pluggy-0.3.1
 rootdir: /tmp/owasp-modsecurity-crs/util/regression-tests, inifile:
 plugins: ftw-1.1.0
 collected 1 items

CRS_Tests.py .

================================================================== 1 passed in 0.43 seconds ===================================================================
```

py.test is the main call to the pytest unit testing framework. So ftw is based on this standard software. The script CRS\_Tests.py is the test-runner that tells pytest how to deal with our CRS tests. This is thus the piece that coordinates and orchestrates ftw. And then we pass the directory with the tests (the latter parameter can be passed only once, in case you were wondering).

### The YAML Test File

Right beneath tests, there is a file test.yaml. It contains an example test:

```
(env) $> cat tests/test.yaml
 ---
 meta:
 author: "csanders-git"
 enabled: true
 name: "Example_Tests"
 description: "This file contains example tests."
 tests:
 -
 test_title: 920272-3
 stages:
 -
 stage:
 input:
 dest_addr: "127.0.0.1"
 port: 80
 uri: "/?test=test%FF1"
 headers:
 User-Agent: "ModSecurity CRS 3 Tests"
 Host: "localhost"
 output:
 log_contains: "id \"920272\""
```

This test tells ftw to make a call to a webserver / ModSecurity / CRS installation on localhost, port 80. Apparently, this service needs to run before you are good to go.

The output we have seen above was a bit sparse. Let's add verbosity with a "-v" flag. And then we should also add the "-s" flag that instructs pytest to hide shell STDOUT and STDERR. So let's add this to our standard call:

```
(env) $> py.test -sv CRS_Tests.py --ruledir=tests
 ===================================================================== test session starts =====================================================================
 platform linux2 -- Python 2.7.12+, pytest-2.9.1, py-1.4.34, pluggy-0.3.1 -- /tmp/owasp-modsecurity-crs/util/regression-tests/env/bin/python2
 cachedir: .cache
 rootdir: /tmp/owasp-modsecurity-crs/util/regression-tests, inifile:
 plugins: ftw-1.1.0
 collected 1 items

CRS_Tests.py::test_crs[ruleset0-Example_Tests -- 920272-3] PASSED

================================================================== 1 passed in 0.42 seconds ===================================================================
```

So now we received an additional line of output telling us that the test 920273-3 has passed. This name corresponds with the "test\_title" field in the yaml file pesented above. As we have seen in said yaml file, there is an option log\_contains. This points to FTW scanning the apache error log looking for alert message for the request in question.

The path to the error log is defined in config.py. Let's take a look at this file:

```
(env) $> cat config.py
# Location of Apache Error Log
log_location_linux = '/apache/logs/error.log'
log_location_windows = 'C:\Apache24\logs\error.log'

# Regular expression to filter for timestamp in Apache Error Log
#
# Default timestamp format: (example: [Thu Nov 09 09:04:38.912314 2017])
#log_date_regex = "\[([A-Z][a-z]{2} [A-z][a-z]{2} \d{1,2} \d{1,2}\:\d{1,2}\:\d{1,2}\.\d+? \d{4})\]"
#
# Reverse format: (example: [2017-11-09 08:25:03.002312])
log_date_regex = "\[([0-9-]{10} [0-9:.]{15})\]"

# Date format matching the timestamp format used by Apache 
# in order to generate matching timestamp ourself
#
# Default timestamp format: (example: see above)
#log_date_format = "%a %b %d %H:%M:%S.%f %Y"
#
# Reverse format: (example: see above)
log_date_format = "%Y-%m-%d %H:%M:%S.%f"
```

So you can adjust your path right in this file. Outside of the path to the error log there are two additional values. This is because FTW filters the logfile with the help of the timestamp. In order to do so it must know the timestamp format, first in the form of a regular expression and secondly as a format string so it can generate a timestamp itself. This is done via the two values log\_date\_regex and log\_date\_format.

If you have followed the [Apache Tutorials at netnea.com](https://www.netnea.com/cms/apache-tutorials/) and if you have thus adopted the reverse timestamp used in the minimal config lesson, then you will find the corresponding values for that format in the comments of config.py. Just enable them to make it work in a compatible way with said tutorials at netnea.com.

That much on the configuration. Now let's look at more tests.

### More Command Line Options

In fact the CRS development tree we are using comes with over 400 test calls. That's far from enough, but it's a good start.

The test requests are organised in a file tree by their rule id. We can call them one after the other, but we can also instruct ftw to load all tests from a file tree recursively:

```
(env) $> py.test -sv CRS_Tests.py --ruledir=tests/REQUEST-941-APPLICATION-ATTACK-XSS
 ===================================================================== test session starts =====================================================================
 platform linux2 -- Python 2.7.12+, pytest-2.9.1, py-1.4.34, pluggy-0.3.1 -- /tmp/owasp-modsecurity-crs/util/regression-tests/env/bin/python2
 cachedir: .cache
 rootdir: /tmp/owasp-modsecurity-crs/util/regression-tests, inifile:
 plugins: ftw-1.1.0
 collected 43 items

CRS_Tests.py::test_crs[ruleset0-941320.yaml -- 941320-1] PASSED
 CRS_Tests.py::test_crs[ruleset1-941150.yaml -- 941150-1] PASSED
 CRS_Tests.py::test_crs[ruleset2-941270.yaml -- 941270-1] PASSED
 CRS_Tests.py::test_crs[ruleset3-941100.yaml -- 941100-1FN] PASSED
 CRS_Tests.py::test_crs[ruleset4-941100.yaml -- 941100-2] PASSED
 CRS_Tests.py::test_crs[ruleset5-941100.yaml -- 941100-3] PASSED
 CRS_Tests.py::test_crs[ruleset6-941100.yaml -- 941100-4] PASSED
 CRS_Tests.py::test_crs[ruleset7-941100.yaml -- 941100-5FN] PASSED
 CRS_Tests.py::test_crs[ruleset8-941290.yaml -- 941290-1] PASSED
 CRS_Tests.py::test_crs[ruleset9-941140.yaml -- 941140-1] PASSED
 CRS_Tests.py::test_crs[ruleset10-941140.yaml -- 941140-2] PASSED
 CRS_Tests.py::test_crs[ruleset11-941140.yaml -- 941140-3] PASSED
 CRS_Tests.py::test_crs[ruleset12-941340.yaml -- 941340-1] PASSED
 CRS_Tests.py::test_crs[ruleset13-941110.yaml -- 941110-1] PASSED
 CRS_Tests.py::test_crs[ruleset14-941110.yaml -- 941110-2] PASSED
 CRS_Tests.py::test_crs[ruleset15-941110.yaml -- 941110-3] PASSED
 CRS_Tests.py::test_crs[ruleset16-941110.yaml -- 941110-4] PASSED
 CRS_Tests.py::test_crs[ruleset17-941240.yaml -- 941240-1] PASSED
 CRS_Tests.py::test_crs[ruleset18-941130.yaml -- 941130-1] PASSED
 CRS_Tests.py::test_crs[ruleset19-941280.yaml -- 941280-1] PASSED
 CRS_Tests.py::test_crs[ruleset20-941300.yaml -- 941300-1] PASSED
 CRS_Tests.py::test_crs[ruleset21-941200.yaml -- 941200-1] PASSED
 CRS_Tests.py::test_crs[ruleset22-941200.yaml -- 941200-2] PASSED
 CRS_Tests.py::test_crs[ruleset23-941200.yaml -- 941200-3] PASSED
 CRS_Tests.py::test_crs[ruleset24-941190.yaml -- 941190-1] PASSED
 CRS_Tests.py::test_crs[ruleset25-941190.yaml -- 941190-2] PASSED
 CRS_Tests.py::test_crs[ruleset26-941190.yaml -- 941190-3] PASSED
 CRS_Tests.py::test_crs[ruleset27-941230.yaml -- 941230-1] PASSED
 CRS_Tests.py::test_crs[ruleset28-941330.yaml -- 941330-1] PASSED
 CRS_Tests.py::test_crs[ruleset29-941250.yaml -- 941250-1] PASSED
 CRS_Tests.py::test_crs[ruleset30-941220.yaml -- 941220-1] PASSED
 CRS_Tests.py::test_crs[ruleset31-941180.yaml -- 941180-1] PASSED
 CRS_Tests.py::test_crs[ruleset32-941180.yaml -- 941180-2] PASSED
 CRS_Tests.py::test_crs[ruleset33-941180.yaml -- 941180-3] PASSED
 CRS_Tests.py::test_crs[ruleset34-941120.yaml -- 941120-1] PASSED
 CRS_Tests.py::test_crs[ruleset35-941210.yaml -- 941210-1] PASSED
 CRS_Tests.py::test_crs[ruleset36-941210.yaml -- 941210-2] PASSED
 CRS_Tests.py::test_crs[ruleset37-941210.yaml -- 941210-3] PASSED
 CRS_Tests.py::test_crs[ruleset38-941170.yaml -- 941170-1] PASSED
 CRS_Tests.py::test_crs[ruleset39-941310.yaml -- 941310-1] PASSED
 CRS_Tests.py::test_crs[ruleset40-941160.yaml -- 941160-1FN] PASSED
 CRS_Tests.py::test_crs[ruleset41-941160.yaml -- 941160-2] PASSED
 CRS_Tests.py::test_crs[ruleset42-941260.yaml -- 941260-1] PASSED
================================================================= 43 passed in 16.55 seconds ==================================================================
 ...
```

That's a lot of requests. And an odd way of ordering numbers. You should also note that the prefix to the filename with the tests (-&gt; rulesetXX) is a consolidated version of the tests that FTW generates prior to running them. So it kind of loads all the tests, consolidates them into single batch and then runs them one after the other.

There is another command line option that may come in handy: running individual tests selectively: -k

```
(env) $> py.test -sv CRS_Tests.py --ruledir=tests/REQUEST-941-APPLICATION-ATTACK-XSS -k 941100
 ===================================================================== test session starts =====================================================================
 platform linux2 -- Python 2.7.12+, pytest-2.9.1, py-1.4.34, pluggy-0.3.1 -- /tmp/owasp-modsecurity-crs/util/regression-tests/env/bin/python2
 cachedir: .cache
 rootdir: /tmp/owasp-modsecurity-crs/util/regression-tests, inifile:
 plugins: ftw-1.1.0
 collected 43 items

CRS_Tests.py::test_crs[ruleset3-941100.yaml -- 941100-1FN] PASSED
 CRS_Tests.py::test_crs[ruleset4-941100.yaml -- 941100-2] PASSED
 CRS_Tests.py::test_crs[ruleset5-941100.yaml -- 941100-3] PASSED
 CRS_Tests.py::test_crs[ruleset6-941100.yaml -- 941100-4] PASSED
 CRS_Tests.py::test_crs[ruleset7-941100.yaml -- 941100-5FN] PASSED

============================================================== 38 tests deselected by '-k941100' ==============================================================
 =========================================================== 5 passed, 38 deselected in 2.06 seconds ===========================================================
```

Note the new line near the bottom where ftw explains how it filtered the tests.

And finally, there is an option to run the tests not only from one folder, but from a complete file tree in a recursive way.

```
(env) $> py.test -sv CRS_Tests.py --ruledir_recurse=tests
 ===================================================================== test session starts =====================================================================
 platform linux2 -- Python 2.7.12+, pytest-2.9.1, py-1.4.34, pluggy-0.3.1 -- /tmp/owasp-modsecurity-crs/util/regression-tests/env/bin/python2
 cachedir: .cache
 rootdir: /tmp/owasp-modsecurity-crs/util/regression-tests, inifile:
 plugins: ftw-1.1.0
 collected 440 items

CRS_Tests.py::test_crs[ruleset0-Example_Tests -- 920272-3] PASSED
 CRS_Tests.py::test_crs[ruleset1-932100.yaml -- 932100-1] FAILED
 CRS_Tests.py::test_crs[ruleset2-932100.yaml -- 932100-2] PASSED
 CRS_Tests.py::test_crs[ruleset3-932100.yaml -- 932100-3] FAILED
 CRS_Tests.py::test_crs[ruleset4-931110.yaml -- 931110-1] FAILED
 CRS_Tests.py::test_crs[ruleset5-931110.yaml -- 931110-2] FAILED
 CRS_Tests.py::test_crs[ruleset6-931110.yaml -- 931110-3] FAILED
 CRS_Tests.py::test_crs[ruleset7-931100.yaml -- 931100-1] PASSED
 CRS_Tests.py::test_crs[ruleset8-931120.yaml -- 931120-1] FAILED
 CRS_Tests.py::test_crs[ruleset9-931120.yaml -- 931120-2] FAILED
 CRS_Tests.py::test_crs[ruleset10-931120.yaml -- 931120-3] FAILED
 CRS_Tests.py::test_crs[ruleset11-931130.yaml -- 931130-1] FAILED
 CRS_Tests.py::test_crs[ruleset12-931130.yaml -- 931130-2] FAILED
 CRS_Tests.py::test_crs[ruleset13-931130.yaml -- 931130-3] FAILED
 CRS_Tests.py::test_crs[ruleset14-930110.yaml -- 930110-1] PASSED
 CRS_Tests.py::test_crs[ruleset15-930110.yaml -- 930110-2] PASSED
 CRS_Tests.py::test_crs[ruleset16-930110.yaml -- 930110-3] PASSED
 CRS_Tests.py::test_crs[ruleset17-930100.yaml -- 930100-1] PASSED
 CRS_Tests.py::test_crs[ruleset18-930120.yaml -- 930120-1] PASSED
 CRS_Tests.py::test_crs[ruleset19-930120.yaml -- 930120-2] PASSED
 CRS_Tests.py::test_crs[ruleset20-930120.yaml -- 930120-3] PASSED
 CRS_Tests.py::test_crs[ruleset21-930120.yaml -- 930120-4] PASSED
```

We are now seeing quite a few failed tests. This has nothing to do with ftw or the CRS, it's the tests that are not yet written correctly. User [@azhao155](https://github.com/azhao155) is very active with fixing these to give us better coverage (and he could use some help with this task). Because of these errors, our continuos integration setup on github does not call all the tests. Instead, Travis only covers those we known to be working:

<figure aria-describedby="caption-attachment-618" class="wp-caption aligncenter" id="attachment_618" style="width: 967px">[![](/images/2017/12/tmp.png)](/images/2017/12/tmp.png)<figcaption class="wp-caption-text" id="caption-attachment-618">Not all tests are executed by Travis so far. The 920xxx rules are skipped as of this writing.</figcaption></figure>

As soon as we have all of them sorted out, we can get include all of them and start to cover those rules where a test is not yet in place.

But regardless of this, ftw is now ready to be used for CRS development and in order to see if your ruleset is behaving as it should:

- You can design a new rule by writing test cases first and then develop the rule to implement the desired functionality; tweaking it until it passes all the tests.
- You can edit an existing rule while continually running the tests to make sure you are not breaking any functionality.
- You can take an existing false positive or false negative, write new tests and then tweak the rule until it passes all use cases.

Ideally, new rules will come with their own complete set of ftw tests in the future.

It is obviously that complete coverage of all the rules with a decent set of tests will take a while. And there are a few things we need to get sorted out along the way.

I would like to have some documentation on how to install this in order to run without virtualenv (I fought python and python won).

And I get the feeling we need a concept on how to write and organize the tests. We have a lot of them already, but I somehow lack the overview and the guideline for a best practice. Maybe a table would be enough for the overview, but how many tests do we need per rule? How do we name them consistently? So maybe it takes more experience and more thinking. And finally, we need to make sure all the existing tests really work. It is namely the latter part where the community could step in and give us a hand. With the information found above and the previous blog posts about test writing, the information is now all in place and you could get hacking immediately.

![](/assets/uploads/2017/08/christian-folini-2017-450x450.png) Christian Folini / [@ChrFolini](https://twitter.com/ChrFolini)