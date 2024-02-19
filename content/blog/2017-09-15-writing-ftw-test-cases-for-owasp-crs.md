---
author: Chaim Sanders
categories:
  - Blog
date: '2017-09-15T03:10:31+02:00'
guid: https://coreruleset.org/?p=522
id: 522
permalink: /20170915/writing-ftw-test-cases-for-owasp-crs/
site-content-layout:
  - default
site-sidebar-layout:
  - default
title: Writing FTW test cases for OWASP CRS
url: /2017/09/15/writing-ftw-test-cases-for-owasp-crs/
---


## <span style="font-weight: 400;">A little background</span>

<span style="font-weight: 400;">Last month we announced the general availability of the Framework for Testing WAFs (FTW) version 1.0. You can read the whole post </span>[**here**](https://coreruleset.org/20170810/testing-wafs-ftw-version-1-0-released/)<span style="font-weight: 400;">, But this is only the beginning of the story. With the release of OWASP CRS v3.0 </span><span style="font-weight: 400;">we started integrating a more agile, test driven development methodology that we believe has resulted in better quality output.</span>

<span style="font-weight: 400;">As of the OWASP CRS 3.0 release, all new rules and most modifications to the rules undertaken will require accompanying unit tests. But how does one use the FTW framework in order to write these tests?</span>

## <span style="font-weight: 400;">CRS Test Cases</span>

<span style="font-weight: 400;">Test cases for CRS 3.0 and beyond are stored in a separate directory in the OWASP-CRS repository. This directory can be found under util/regression-tests within the OWASP-CRS repository (</span>[<span style="font-weight: 400;">https://github.com/coreruleset/coreruleset/tree/v3.0/dev/util/regression-tests</span>](https://github.com/coreruleset/coreruleset/tree/v3.0/dev/util/regression-tests)<span style="font-weight: 400;">). Within this repository you’ll find that there are various types of tests including ones that are broken down by rule ID. These tests are meant to trigger the the given rule to ensure it still functions as expected. These rule named </span>*<span style="font-weight: 400;">\[ruleid\].yaml</span>*<span style="font-weight: 400;"> all residing within folders named after the CRS configuration file that the rule is present within in. When adding tests one should extend or add files based on the aforementioned pattern.</span>

## <span style="font-weight: 400;">Writing Test Cases</span>

<span style="font-weight: 400;">FTW is designed to be easy to use. Using the YAML format, one can construct tests that form a transaction between a web client and server. In order to adhere to the goals of test driven development, we wanted a way for implementers to be able to run hundreds if not thousands of tests with the ability to quickly identify issues, whether it’s a broken test or a regression. Due to this goal, tests are structured as follows:</span>

- <span style="font-weight: 400;">Each .YAML file may have many tests</span>
- <span style="font-weight: 400;">Each test may have many stages</span>
- <span style="font-weight: 400;">Each stage has 1 input (client writes on socket), and 1 output (client reads from socket)</span>

<span style="font-weight: 400;">An input is a set of configuration options for an HTTP transaction. This can include things like URI path, POST data and headers. An output is an </span>*<span style="font-weight: 400;">expected</span>*<span style="font-weight: 400;"> response from a server once given an input. A test fails when a given input results in an actual output that </span>*<span style="font-weight: 400;">fails</span>*<span style="font-weight: 400;"> to match the expected output of the transaction. Since a test can have many stages, this means that one can construct multiple stages of a web transaction and test every response along the way. This is particularly useful in testing cases where you require state, such as accessing an authenticated portion of a site or delivering a multi-stage web attack. The YAML files themselves provide a vehicle to logically group tests. So for example, a YAML file called </span>*<span style="font-weight: 400;">FORUM-XSS.yaml</span>*<span style="font-weight: 400;"> can contain tests to verify XSS protections against the forum portion of your website. This can provide valuable information later on. For instance, when a regression is introduced in your WAF deployment, FTW will provide the exact test-id and YAML file that failed.</span>

<span style="font-weight: 400;">Now that we have covered how the YAML tests are designed at a high level, let’s look at how to write an FTW test. FTW has a number of logical defaults that can be overwritten if more functionality is needed. The default is an HTTP request on port 80 to localhost that looks as follows:</span>

```
<span style="font-weight: 400;">GET / HTTP/1.1</span>
<span style="font-weight: 400;">Host: localhost</span>
```

<span style="font-weight: 400;">A minimum test file requires a little bit detail to get started, but not much. We need some metadata about the tests being undertaken. We decided to mandate the presence of such metadata in the interest of future manageability. A minimal test file is below</span>

```
---
  <strong><span style="color: #0000ff;">meta:</span>
	<span style="color: #0000ff;">author:</span></strong> csanders-git
	<span style="color: #0000ff;"><strong>enabled:</strong></span> true
	<span style="color: #0000ff;"><strong>name:</strong></span> example test1
	<span style="color: #0000ff;"><strong>description:</strong></span> A fairly minimal test file
  <span style="color: #0000ff;"><strong>tests:</strong></span>
	-
  	<span style="color: #0000ff;"><strong>test_title:</strong></span> example-test1
  	<span style="color: #0000ff;"><strong>stages:</strong>
    	<strong>-</strong>
      	<strong>stage:</strong>
        	<strong>input:
</strong></span>                 <strong><span style="color: #0000ff;"> dest_addr:</span></strong> localhost
        	<strong><span style="color: #0000ff;">output:</span></strong>
          	 <strong><span style="color: #0000ff;"> status:</span></strong> 200
```

<span style="font-weight: 400;">This test sends the basic request described above and expects a ‘200 OK’ response. Notice that the included test will use our defaults to generate this request. We can also explicitly call those out if desired as demonstrated in the following example test file:</span>

```
<span style="color: #0000ff;"><strong>---</strong></span>
  <span style="color: #0000ff;"><strong>meta:</strong>
	<strong>author:</strong></span> csanders-git
	<strong><span style="color: #0000ff;">enabled:</span></strong> true
	<span style="color: #0000ff;"><strong>name:</strong></span> example test2
	<strong><span style="color: #0000ff;">description:</span></strong> An expanded test file
  <span style="color: #0000ff;"><strong>tests:</strong></span>
	<strong><span style="color: #0000ff;">-</span></strong>
  	<strong><span style="color: #0000ff;">test_title:</span></strong> example-test2
        <span style="color: #0000ff;"><strong>stages:</strong>
    	<strong>-</strong>
          	<strong>stage:</strong></span>
        	<strong><span style="color: #0000ff;">input:</span>
          	<span style="color: #0000ff;">protocol:</span></strong> http
          	<strong><span style="color: #0000ff;">dest_addr:</span></strong> localhost
          	<span style="color: #0000ff;"><strong>port:</strong></span> 80
          	<strong><span style="color: #0000ff;">method:</span></strong> GET
          	<strong><span style="color: #0000ff;">uri:</span></strong> /
          	<span style="color: #0000ff;"><strong>version:</strong></span> HTTP/1.1
          	<span style="color: #0000ff;"><strong>headers:</strong>
   	          <strong>Host:</strong></span> localhost
        	<strong><span style="color: #0000ff;">output:</span>
                  <span style="color: #0000ff;">status:</span></strong> 200

```

At this point the general approach should be pretty clear. We can easily combine these two tests into one file, which is how we end up structuring our regression tests for OWASP-CRS. Below is an example of a combined test file. There is no limit on the amount of tests that can be placed here.

```
<span style="color: #0000ff;"><strong>---</strong></span>
 <span style="color: #0000ff;"> <strong>meta:</strong>
	<strong>author:</strong></span> csanders-git
	<strong><span style="color: #0000ff;">enabled:</span></strong> true
	<strong><span style="color: #0000ff;">name:</span></strong> example test
	<strong><span style="color: #0000ff;">description:</span></strong> A fairly minimal test file
  <strong><span style="color: #0000ff;">tests:</span>
	<span style="color: #0000ff;">-</span>
  	<span style="color: #0000ff;">test_title:</span></strong> example-test1
  	<strong><span style="color: #0000ff;">stages:</span>
    	<span style="color: #0000ff;">-</span>
      	        <span style="color: #0000ff;">stage:</span></strong>
        	<span style="color: #0000ff;"><strong>input:</strong>
          	<strong>dest_addr:</strong></span> localhost
        	<span style="color: #0000ff;"><strong>output:</strong>
          	<strong>status:</strong></span> 200   	
	<strong><span style="color: #0000ff;">-</span></strong>
  	<strong><span style="color: #0000ff;">test_title:</span></strong> example-test2
  	<strong><span style="color: #0000ff;">stages:</span></strong>
    	-
      	       <span style="color: #0000ff;"><strong> stage:</strong>
        	<strong>input:</strong>
        	  <strong>protocol:</strong></span> http
          	<strong><span style="color: #0000ff;">dest_addr:</span></strong> localhost
          	<strong><span style="color: #0000ff;">port:</span></strong> 80
          	<strong><span style="color: #0000ff;">method:</span></strong> GET
          	<strong><span style="color: #0000ff;">uri:</span></strong> /
          	<span style="color: #0000ff;"><strong>version:</strong></span> HTTP/1.1
          	<strong><span style="color: #0000ff;">headers:</span></strong>
            	   <strong><span style="color: #0000ff;"> Host:</span></strong> localhost
        	<span style="color: #0000ff;"><strong>output:</strong></span>
          	<strong><span style="color: #0000ff;">status:</span></strong> 200
```

We are not forced to use only only check status codes, FTW supports a modular design that allows for checking various WAFs. The OWASP-CRS regression tests currently only feature support for reading ModSecurity 2.x logs (the location of which is defined in settings.ini). However we are able to supply a regex that is used to check the result of a request (using response\_contains) or if a value is either present or not present in the WAF logs (using log\_contains or no\_log\_contains respectively). An example test to see if an XSS rule triggered is below:

```
<span style="color: #0000ff;"><strong>-</strong></span>
  <strong><span style="color: #0000ff;">test_title:</span></strong> 941100-1
  <span style="color: #0000ff;"><strong>desc:</strong></span> Test as described in http://www.client9.com/article/five-interesting-injection-attacks/
  <span style="color: #0000ff;"><strong>stages:</strong>
 <strong> -</strong>
	<strong>stage:</strong></span>
  	<strong><span style="color: #0000ff;">input:</span></strong>
    	<span style="color: #0000ff;"><strong>dest_addr:</strong> </span>127.0.0.1
    	<strong><span style="color: #0000ff;">method:</span></strong> GET
    	<strong><span style="color: #0000ff;">port:</span></strong> 80
    	<strong><span style="color: #0000ff;">uri:</span></strong> '/demo/xss/xml/vuln.xml.php?input=<script xmlns="http://www.w3.org/1999/xhtml">setTimeout("top.frame2.location=\"javascript:(function () {var x = document.createElement(\\\"script\\\");x.src = \\\"//sdl.me/popup.js?//\\\";document.childNodes\[0\].appendChild(x);}());\"",1000)</script>&//'
    	<span style="color: #0000ff;"><strong>headers:</strong>
      	    <strong>User-Agent:</strong></span> ModSecurity CRS 3 Tests
      	    <span style="color: #0000ff;"><strong>Host:</strong></span> localhost
  	<span style="color: #0000ff;"><strong>output:</strong></span>
    	<strong><span style="color: #0000ff;">log_contains:</span></strong> id "941100" 
```

Some things most people don’t want to do automatically, like content-length calculations. To that end there are some things that are, by default, automagically done for the user, such as encoding and content-length calculations. This makes sending POST request easier as can be seen in the example below:

```
-
  <span style="color: #0000ff;"><strong>test_title:</strong></span> 920170-1
 <span style="color: #0000ff;"><strong> stages:</strong></span>
	<strong><span style="color: #0000ff;">-</span></strong>
  	<span style="color: #0000ff;"><strong>stage:</strong>
    	<strong>input:</strong>
      	        <strong>method:</strong> </span>"POST"
      	        <strong><span style="color: #0000ff;">headers:</span>
          	<span style="color: #0000ff;">User-Agent:</span></strong> "ModSecurity CRS 3 Tests"          	
          	<span style="color: #0000ff;"><strong>Host:</strong></span> "localhost"
          	<span style="color: #0000ff;"><strong>Content-Type:</strong></span> "application/x-www-form-urlencoded"
      	        <span style="color: #0000ff;"><strong>data:</strong></span> "hi=test"
    	<span style="color: #0000ff;"><strong>output:</strong>
      	        <strong>no_log_contains:</strong></span> "id \"920170\""

```

Users sometimes really don’t want magic, especially when writing more complex tests. To this end magic can be turned off using stop\_magic. This enables users to make tests such as sending requests without content-lengths.

Probably one of the more complicated items that can be done with HTTP is multi-part requests To this end the data directive can also be passed as a list. An example of such a format is below:

```
<strong><span style="color: #0000ff;">-</span></strong>
  <span style="color: #0000ff;"><strong>test_title:</strong></span> "Multi-Part-Pretty"
  <strong><span style="color: #0000ff;">stages:</span>
	<span style="color: #0000ff;">-</span>
  	<span style="color: #0000ff;">stage:</span>
    	<span style="color: #0000ff;">input:</span></strong>
      	    <span style="color: #0000ff;"><strong>method:</strong></span> POST
      	    <strong><span style="color: #0000ff;">headers:</span>        	
          	<span style="color: #0000ff;">Host:</span></strong> localhost
          	<span style="color: #0000ff;"><strong>Content-Type:</strong></span> "multipart/form-data; boundary=--------397236876"
               	<strong><span style="color: #0000ff;">data:</span></strong>
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
    	<strong><span style="color: #0000ff;">output:</span></strong>
      	        <span style="color: #0000ff;"><strong>status:</strong></span> 200

```

Of course in some cases you really just want a RAW request. To this end there is support for both raw requests and base64 encoded raw requests. Such as this request that needs to deal with sending escape sequences.

```
<strong><span style="color: #0000ff;">-</span>
  <span style="color: #0000ff;">test_title:</span></strong> 920460-1
 <span style="color: #0000ff;"><strong> stages:</strong></span>
	<strong><span style="color: #0000ff;">-</span></strong>
  	<span style="color: #0000ff;"><strong>stage:</strong></span>
    	<strong><span style="color: #0000ff;">input:</span></strong>
      	   <span style="color: #0000ff;"><strong> encoded_request:</strong></span> "UE9TVCAvIEhUVFAvMS4xCkhvc3Q6IGxvY2FsaG9zdApVc2VyLUFnZW50OiBNb2RTZWN1cml0eSBDUlMgMyBUZXN0cwpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZApDb250ZW50LUxlbmd0aDogMjIKCmZpbGU9Y2F0Ky9ldGMvcGFcc3N3XGQ="
    	<strong><span style="color: #0000ff;">output:</span></strong>
      	   <span style="color: #0000ff;"><strong> log_contains:</strong></span> "id \"920460\""

```

Hopefully given these examples even the most novice developer will feel a little more comfortable and confident with the usage and creation of even the most complicated test for OWASP CRS. Good luck and happy testing!