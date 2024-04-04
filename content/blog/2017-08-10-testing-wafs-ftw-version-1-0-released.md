---
author: csanders-git
categories:
  - Blog
date: '2017-08-10T21:28:14+02:00'
title: Testing WAFs, FTW Version 1.0 released
url: /2017/08/10/testing-wafs-ftw-version-1-0-released/
---


The OWASP Project maintains an open source set of rules known as the the OWASP Core Rule Set (CRS). The CRS implements protections for the well known, broad classes of web application vulnerabilities identified by OWASP. Over time, this set of rules has become the most popular ruleset for ModSecurity and also found its way into many other popular WAFs.

During this same timeframe we have seen Quality Assurance (QA)/DevOps techniques adjust to new Agile development methodologies. To a large extent this Agile pattern matches the historical development practices of CRS. As a result, during the development of the latest CRS version 3.0, the development team decided that a serious overhaul of the regression/unit tests was overdue. While some existing Perl regression tests existed, these were incomplete and considered difficult for the average user to run. The CRS development team also concluded that a more refined testing methodology commits to a higher quality product and allows for a demonstration of the effectiveness of OWASP CRS compared to many other rule sets and WAFs.

{{< figure src="images/2017/08/FTW1.png" >}}

As a result of extensive regression test development we are hoping to address a frequent user request to provide a capability to compare the effectiveness of various WAFs. Such comparisons can be tricky as they often attempt to compare varying features. In many situations OWASP CRS comes out favorably as can be seen in the latest Gartner report ([https://www.gartner.com/doc/reprints?id=1-3C4V1AS&amp;ct=160721&amp;st=sb](https://www.gartner.com/doc/reprints?id=1-3C4V1AS&ct=160721&st=sb)), where ModSecurity with CRS effectively acts as a baseline. However comparisons such as these have historically put very little work on testing overall WAF effectiveness. Our hope is to provide a set of tests that will act as a minimum benchmark between WAFs.

To accomplish this goal we started work on a project dubbed the Framework for Testing WAFs (FTW). This project, jointly developed by the OWASP Core Rule Set community along with security researchers from Fastly, was designed to extend far beyond regression testing for OWASP CRS. The following are just some of the design criteria for this project

- Support the creation of HTTP requests both compliant with the HTTP specification and non-compliant with it
- Be modular enough that any WAF could easily tested
- Be able to pass malicious requests that often violate HTTP spec
- Be user friendly and easy to write test cases
- Provide a programmatic interface for more advance test cases
- Use an existing heavily used scripting language
- Use existing existing libraries and code where possible
- Serve as a regression testing framework for the OWASP CRS 3.0
- Provide the capability to run tests against other WAFs to compare effectiveness
- Provide modular support for logging endpoints
- Build a continuous integration platform to insert security and regression testing behind deploying a WAF

As the first milestone in this project, we are proud to announce the release of FTW version 1.0. This project is available at <https://github.com/coreruleset/ftw> or via pypi. The framework is written in Python, leveraging the existing pytest framework which many developers will be familiar with. It will accept tests in either YAML format or via its programmatic interface and is designed to be modular enough to support multiple WAFs and complicated multi-stage requests.

To aid the developer, tests are designed to only require minimal effort to design, where many defaults are provided automatically in a similar manner to how the Scapy project generates packets. Below we provide an example of a simple test file. Of course, more complicated examples involving aspects such as storing cookies and submitting multipart forms are also possible as can be seen in the documentation (<https://github.com/coreruleset/ftw/tree/master/docs>).

```yaml
---
  meta:
    author: "csanders-git"
    enabled: true
    name: "Example_Tests"
    description: "This file contains example tests."
  tests:
    -
      test_title: example_1
      stages:
        -
          stage:
            input:
              dest_addr: "127.0.0.1"
              uri: "/"
              headers:
                  User-Agent: "An example test using FTW"
                  Host: "localhost"
            output:
              status: 200
```

FTW follows the same extendible concept as ModSecurity. While the project provides the capability to develop extremely flexible web based testing, the core project is provided with only limited tests files itself. The CRS team provides a continuously expanding corpus of tests designed for OWASP CRS 3 within their repo at: <https://github.com/coreruleset/coreruleset/tree/v3.0/dev/util/regression-tests>. While these tests were designed with CRS in mind, they provide a set of web-based attacks to test security features of any WAF against the OWASP CRS Top 10 web attacks. Such testing has already uncovered several underperforming rules such as can be seen in Github issue #480 (<https://github.com/coreruleset/coreruleset/pull/480>), as well as providing a methodical way to develop and test more complex functionality, such as the revamped RCE rules in CRS 3 (<https://github.com/coreruleset/coreruleset/pull/430>).

{{< figure src="images/2017/08/FTW2.png" >}}

At this point the CRS regressions has over 1500 test cases designed for it and this number is growing daily. To utilize such extensive tests we plan to enforce the use of [Travis-CI](https://travis-ci.org/) starting with the promotion of OWASP CRS 3.0 to the master branch. It is our sincere hope that an increased reliance on testing and automation will vastly increase the quality of both the CRS ruleset and WAFs as a whole.
