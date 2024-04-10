---
author: dune73
categories:
  - Blog
date: '2020-05-13T22:12:06+02:00'
title: CRS Repository at New Location
---

We have successfully migrated our GitHub repository to a new location at  
  
<https://github.com/coreruleset/coreruleset>  
  
Trustwave SpiderLabs hosted the OWASP ModSecurity Core Rule Set project under their umbrella for many years. They acted as stewards of our project and also directed it via the former lead Ryan Barnett. Yet as a formally independent OWASP project, it is a bit odd to dwell under a commercial entity and for a commercial entity like Trustwave SpiderLabs, it is a bit odd to host a project that they do not control.  
  
So Trustwave and CRS came to the conclusion it is time we learn to walk on our own and we started the migration process. Migrating a GitHub project is a tedious task unless you are willing to transfer it completely (with old links going dead). Instead we decided to clone the repo and migrate all the issues, wiki, project history, etc.  
  
The tricky bit is the issues. There is a lot of information in the discussions in the issues and losing that history was non-option. Unfortunately, GitHub is not very helpful in this regard and we had to do some heavy lifting via the official API to get this off the ground. Entering the CRS Migration Bot: <https://github.com/CRS-migration-bot>  
This neat agent reads an issue via API, reproduces it a new location with his account, but referencing the original reporter and placing a link to the original issue. And here comes the best part: The CRS Migration bot uses the same issue number. E.g. :  
  
<https://github.com/SpiderLabs/owasp-modsecurity-crs/issues/1337>  
has become  
<https://github.com/coreruleset/coreruleset/issues/1337>

The CRS Migration Bot has been created by CRS developer [Felipe Zipitría](https://www.fing.edu.uy/~fzipi/). It is of course free and you should be able to re-use it for your own repo migration needs.

We have tested the migration and the newly created issues, merging pull requests works with the full support of CI/CD. So we think we are done. But what is of course not done is updating the several thousands of links to our old repository. If you come across such a link and you think it can be updated, you could do us a favor by informing the respective owner to please link to <https://github.com/coreruleset/coreruleset>.  
  
*Christian Folini, on behalf of the CRS team*
