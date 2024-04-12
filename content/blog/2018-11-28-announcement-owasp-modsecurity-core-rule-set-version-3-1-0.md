---
author: dune73
categories:
  - Blog
date: '2018-11-28T23:08:03+01:00'
title: 'Announcement: OWASP ModSecurity Core Rule Set Version 3.1.0'
slug: 'announcement-owasp-modsecurity-core-rule-set-version-3-1-0'
---


The OWASP Core Rule Set team is happy to announce the CRS release v3.1.0 at last.

A wee bit over 2 years in the making, this major release represents a big step forward in terms of capabilities, usability and protection.

Key features include:

* A new set of rules defending against Java injections  
* Initial set of file upload checks  
* Add built-in exceptions for Dokuwiki, Owncloud, Nextcloud and CPanel  
* Easier handling of the paranoia mode  
* Many false positives fixed  
* Successful source code archaeology with regular expressions  
* Detailed rule cleanup for easier maintenance  
* Speed improvements via the removal of unneeded regex capture groups  
* Regression tests for rules, Travis support  
* CRS docker image based on Ubuntu

For a complete list of new features and the changes in this release, see the CHANGES document:  
<https://github.com/coreruleset/coreruleset/blob/v3.1/dev/CHANGES>

CRS 3.1 is the best stable release of the OWASP ModSecurity Core Rule Set. We advise all users and providers of boxed CRS versions to update their setups. CRS 3.0 won't see any future updates and we recommend you to migrate onto our new release.

CRS 3.1 requires an Apache/IIS/NGINX web server with ModSecurity 2.8.0 or higher. CRS 3.1 will run on libModSecurity 3.0 on NGINX.

Our GitHub repository is the preferred way to download and update CRS:

```bash
$> wget https://github.com/coreruleset/coreruleset/archive/v3.1.0.tar.gz
```

For detailed installation instructions, see the INSTALL document:

<https://github.com/coreruleset/coreruleset/blob/v3.1/dev/INSTALL>

Our desire is to see the Core Rules project as a simple baseline security feature, effectively fighting OWASP TOP 10 weaknesses with few side effects. We are committed to cut down on false positives as much as possible in the default install. We welcome reports of false positives on github.

Sincerely,

Chaim Sanders, Walter Hop and Christian Folini on behalf of the Core Rule Set development team
