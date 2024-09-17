---
author: dune73
categories:
  - Blog
date: '2018-09-27T07:01:35+02:00'
tags:
  - CRS-News
title: CRS Project News September 2018
---


We skipped the monthly news in August as the 3.1-RC release had been delayed into September. But here we go again with the mostly monthly newsletter of the CRS project.

The most important news is the publication of the release candidate 1 for CRS 3.1.

### **What has happened in recent weeks**

- CRS 3.1 RC1 has been released. The most important changes:  
  - Protections against common Java attacks  
  - Support for blocking in one paranoia level while logging in a higher level.  
  - More pre-made exclusion packs for popular web applications  
  - Reconstructed and improved SQL injections protections  
  - Various bug fixes and optimizations  
    Announcement: <http://web.archive.org/web/20230830054004/https://lists.owasp.org/pipermail/owasp-modsecurity-core-rule-set/2018-September/002586>
    Download: <https://github.com/coreruleset/coreruleset/releases/tag/v3.1.0-rc1>
- The development has been moved to the 3.2/dev branch, some changes will be backported to 3.1.
    Link: <https://github.com/coreruleset/coreruleset>
- Interview with CRS project co-lead Christian Folini on the AppSec podcast  
    Link: <https://coreruleset.org/20180809/appsec-podcast-interviewing-crs-project-co-lead-christian-folini/>
- Webinar on ModSecurity and CRS3 with Owen Garett, Head of Products at NGINX: The webinar covered installation of ModSec3 and CRS3, but also integration and tuning for false positives and performance. It can be watched on demand after registration (link no longer available)
- There is a missing feature in ModSecurity 3.0.x that makes it choke on the upcoming CRS 3.1 release. There is an official patch available and the development tree of ModSecurity has the fix. But Trustwave has not yet released the ModSecurity with the fix anew. This may mean that users of the officially release ModSecurity 3 software will fail to run CRS 3.1 after our release.
    Link: <https://github.com/SpiderLabs/ModSecurity/issues/1797>
- Maxmind, the company behind the popular GeoIP database used by ModSecurity ceased to release the legacy format of the database. ModSec 2.9 only supports this legacy version, so users are in a bad position. CRS developer Christoph Hansen posted on the ModSec mailinglist he was able to transpose the new GeoIP database into the old format so he could continue to use it. A blog post is in the making.
    Link: <https://github.com/SpiderLabs/ModSecurity/issues/1727#issuecomment-423612546>
- The OWASP slack changed the place to get invites. If you want to join us, please get in touch via mail and we'll send you the link. OWASP says the are overhauling the setup.

### Significant pull requests that were merged

- Development has been shifted to the new 3.2 branch, that has been declared master
- Walter Hop contributed 2 new strings to the list of Java Struts namespaces for use in the new 944130 rule  
    Link: <https://github.com/coreruleset/coreruleset/pull/1177>
- Other than that, everybody is waiting for new issues popping up with the 3.1-RC release but it has been quiet on that front so far.

### Things that are meant to happen in the coming weeks

- We plan to release CRS 3.1 in October unless we see any road blockers.
- There is a strange bug that a PL2 rule among the new Java rules in CRS 3.1-RC1 triggers. If it is a bug, it's rather a ModSecurity bug, but it's completely unclear how this is happening as reproduction has been very cumbersome so far. What is clear it happens in connection with chunked transfer encoding of JSON payloads at PL2 and higher. So it is a rather peculiar situation that is relatively rare.  
    Link: <https://github.com/coreruleset/coreruleset/issues/1185>

### Important pull requests in the queue

- Victor Hora discovered typos in CRS variable names and a discussion about streamlining lower- and uppercase variable names evolved.
    Link: <https://github.com/coreruleset/coreruleset/pull/1187>
- Franziska Bühler has fixed a relatively annoying bug in the docker image of CRS.
    Link: <https://github.com/coreruleset/coreruleset/pull/1168>
- TheMiddleBlue suggests to add additional PHP wrappers to our data file.  
    Link: <https://github.com/coreruleset/coreruleset/pull/1172>
