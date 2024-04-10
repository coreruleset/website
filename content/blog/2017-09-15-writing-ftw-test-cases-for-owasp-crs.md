---
author: csanders-git
categories:
  - Blog
date: '2017-09-15T03:10:31+02:00'
title: Writing FTW test cases for OWASP CRS
---


## A little background

Last month we announced the general availability of the Framework for Testing WAFs (FTW) version 1.0. You can read the whole post [**here**](https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released/), but this is only the beginning of the story. With the release of OWASP CRS v3.0 we started integrating a more agile, test driven development methodology that we believe has resulted in better quality output.

As of the OWASP CRS 3.0 release, all new rules and most modifications to the rules undertaken will require accompanying unit tests. But how does one use the FTW framework in order to write these tests?

## CRS Test Cases

Test cases for CRS 3.0 and beyond are stored in a separate directory in the OWASP-CRS repository. This directory can be found under util/regression-tests within the OWASP-CRS repository https://github.com/coreruleset/coreruleset/tree/v3.0/dev/util/regression-tests. Within this repository you’ll find that there are various types of tests including ones that are broken down by rule ID. These tests are meant to trigger the the given rule to ensure it still functions as expected. These rule named `*[ruleid].yaml*` all residing within folders named after the CRS configuration file that the rule is present within in. When adding tests one should extend or add files based on the aforementioned pattern.

## Writing Test Cases

FTW is designed to be easy to use. Using the YAML format, one can construct tests that form a transaction between a web client and server. In order to adhere to the goals of test driven development, we wanted a way for implementers to be able to run hundreds if not thousands of tests with the ability to quickly identify issues, whether it’s a broken test or a regression. Due to this goal, tests are structured as follows:

- Each .YAML file may have many tests
- Each test may have many stages
- Each stage has 1 input (client writes on socket), and 1 output (client reads from socket)

An input is a set of configuration options for an HTTP transaction. This can include things like URI path, POST data and headers. An output is an *expected* response from a server once given an input. A test fails when a given input results in an actual output that *fails* to match the expected output of the transaction. Since a test can have many stages, this means that one can construct multiple stages of a web transaction and test every response along the way. This is particularly useful in testing cases where you require state, such as accessing an authenticated portion of a site or delivering a multi-stage web attack. The YAML files themselves provide a vehicle to logically group tests. So for example, a YAML file called *FORUM-XSS.yaml* can contain tests to verify XSS protections against the forum portion of your website. This can provide valuable information later on. For instance, when a regression is introduced in your WAF deployment, FTW will provide the exact test-id and YAML file that failed.

Now that we have covered how the YAML tests are designed at a high level, let’s look at how to write an FTW test. FTW has a number of logical defaults that can be overwritten if more functionality is needed. The default is an HTTP request on port 80 to localhost that looks as follows:

```http
GET / HTTP/1.1
Host: localhost
```

A minimum test file requires a little bit detail to get started, but not much. We need some metadata about the tests being undertaken. We decided to mandate the presence of such metadata in the interest of future manageability. A minimal test file is below

```yaml
---
meta:
  author: csanders-git
  enabled: true
  name: example test1
  description: A fairly minimal test file
  tests:
    -
      test_title: example-test1
      stages:
      -
        stage:
          input:
          dest_addr: localhost
        output:
            status: 200
```

This test sends the basic request described above and expects a ‘200 OK’ response. Notice that the included test will use our defaults to generate this request. We can also explicitly call those out if desired as demonstrated in the following example test file:

```yaml
---
meta:
    author: csanders-git
    enabled: true
    name: example test2
    description: An expanded test file
    tests:
    -
        test_title: example-test2
        stages:
        -
            stage:
                input:
                    protocol: http
                    dest_addr: localhost
                    port: 80
                    method: GET
                    uri: /
                    version: HTTP/1.1
                    headers:
                        Host: localhost
                output:
                        status: 200
```

At this point the general approach should be pretty clear. We can easily combine these two tests into one file, which is how we end up structuring our regression tests for OWASP-CRS. Below is an example of a combined test file. There is no limit on the amount of tests that can be placed here.

```yaml
---
meta:
    author: csanders-git
    enabled: true
    name: example test
    description: A fairly minimal test file
  tests:
    -
      test_title: example-test1
      stages:
        -
        stage:
            input:
              dest_addr: localhost
            output:
              status: 200
    -
      test_title: example-test2
      stages:
        -
        stage:
            input:
              protocol: http
              dest_addr: localhost
              port: 80
              method: GET
              uri: /
              version: HTTP/1.1
              headers:
                    Host: localhost
            output:
              status: 200
```

We are not forced to use only only check status codes, FTW supports a modular design that allows for checking various WAFs. The OWASP-CRS regression tests currently only feature support for reading ModSecurity 2.x logs (the location of which is defined in settings.ini). However we are able to supply a regex that is used to check the result of a request (using `response_contains`) or if a value is either present or not present in the WAF logs (using `log_contains` or `no_log_contains` respectively). An example test to see if an XSS rule triggered is below:

```yaml
-
  test_title: 941100-1
  desc: Test as described in http://www.client9.com/article/five-interesting-injection-attacks/
  stages:
  -
    stage:
      input:
        dest_addr: 127.0.0.1
        method: GET
        port: 80
        uri: '/demo/xss/xml/vuln.xml.php?input=setTimeout("top.frame2.location=\"javascript:(function () {var x = document.createElement(\\\"script\\\");x.src = \\\"//sdl.me/popup.js?//\\\";document.childNodes\[0\].appendChild(x);}());\"",1000)&//'
        headers:
            User-Agent: ModSecurity CRS 3 Tests
            Host: localhost
      output:
        log_contains: id "941100" 
```

Some things most people don’t want to do automatically, like content-length calculations. To that end there are some things that are, by default, automagically done for the user, such as encoding and content-length calculations. This makes sending POST request easier as can be seen in the example below:

```yaml
-
  test_title: 920170-1
  stages:
    -
      stage:
        input:
            method: "POST"
            headers:
                User-Agent: "ModSecurity CRS 3 Tests"	
                Host: "localhost"
                Content-Type: "application/x-www-form-urlencoded"
            data: "hi=test"
        output:
                  no_log_contains: "id \"920170\""

```

Users sometimes really don’t want magic, especially when writing more complex tests. To this end magic can be turned off using stop\_magic. This enables users to make tests such as sending requests without content-lengths.

Probably one of the more complicated items that can be done with HTTP is multi-part requests To this end the data directive can also be passed as a list. An example of such a format is below:

```yaml
-
  test_title: "Multi-Part-Pretty"
  stages:
    -
      stage:
        input:
            method: POST
            headers:
                Host: localhost
                Content-Type: "multipart/form-data; boundary=--------397236876"
            data:
                - "----------397236876"
                - "Content-Disposition: form-data; name=\"text\";"
                - ""
                - "test default"
                - "----------397236876"
                - "Content-Disposition: form-data; name=\"file1\"; filename=\"a.txt\""
                - "Content-Type: text/plain"
                - ""
                - "Content of a.txt."
                - ""
                - "----------397236876--"
        output:
            status: 200
```

Of course in some cases you really just want a RAW request. To this end there is support for both raw requests and base64 encoded raw requests. Such as this request that needs to deal with sending escape sequences.

```yaml
-
  test_title: 920460-1
  stages:
    -
      stage:
        input:
            encoded_request: "UE9TVCAvIEhUVFAvMS4xCkhvc3Q6IGxvY2FsaG9zdApVc2VyLUFnZW50OiBNb2RTZWN1cml0eSBDUlMgMyBUZXN0cwpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZApDb250ZW50LUxlbmd0aDogMjIKCmZpbGU9Y2F0Ky9ldGMvcGFcc3N3XGQ="
        output:
            log_contains: "id \"920460\""
```

Hopefully given these examples even the most novice developer will feel a little more comfortable and confident with the usage and creation of even the most complicated test for OWASP CRS. Good luck and happy testing!
