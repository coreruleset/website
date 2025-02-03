---
author: RedXanadu
categories:
  - Blog
date: '2022-09-19T16:08:09+02:00'
title: CRS Version 3.3.3 and 3.2.2 (covering several CVEs)
slug: 'crs-version-3-3-3-and-3-2-2-covering-several-cves'
---


**Release announcement covering fixes for CVE-2022-39955, CVE-2022-39956, CVE-2022-39957 and CVE-2022-39958, additional security fixes and security fixes in the latest ModSecurity releases 2.9.6 and 3.0.8.**

The OWASP ModSecurity Core Rule Set (CRS) team is pleased to announce the release of two new CRS versions.
*Edit: Updated download links now to refer to the [fixed versions](https://coreruleset.org/20220920/crs-version-3-3-4-and-3-2-3/).*

Version 3.3.4 — <https://github.com/coreruleset/coreruleset/releases/tag/v3.3.4>
Version 3.2.3 — <https://github.com/coreruleset/coreruleset/releases/tag/v3.2.3>

This is a security release fixing several partial rule set bypasses with HIGH or even CRITICAL severity described in the following CVEs:

- **CVE-2022-39955 – Multiple charsets defined in Content-Type header**
- **CVE-2022-39956 – Content-Type or Content-Transfer-Encoding MIME header fields abuse**
- **CVE-2022-39957 – Charset accept header field resulting in response rule set bypass**
- **CVE-2022-39958 – Small range header leading to response rule set bypass**

This announcement is also meant to highlight the importance of the ModSecurity updates 2.9.6 and 3.0.8 from September 8, 2022.

This long message will start with an introduction to the context of all these vulnerabilities/fixes. We will then explain the CVEs affecting CRS, some minor security fixes, and then the fixes in the ModSecurity code base as far as they affect CRS and our users and integrators.  
  
The vulnerabilities we are fixing have been discovered during a limited private bug bounty program organized by Yahoo and Intigriti with our collaboration under the title *Intigriti 1337UP0522 WAF Promotion Event*. We thank Yahoo/The Paranoids wholeheartedly for their commitment to help improve the security posture of CRS and their cooperation throughout the program. The bounty hunt itself has been a big success and – you probably saw this coming – successful bug bounty programs lead to a lot of findings. CRS has been buried in findings and we are still fixing bypasses around our rules.

A small subset of the findings constitute partial rule set bypasses. We define a rule set bypass as a payload (a) that disables the rule set and allows an attacker to submit a payload (b) without the WAF detecting it. A partial rule set bypass is limited to certain parts of a request (e.g. the request body).

The partial rule set bypasses fall into two categories: the ones that can be fixed within CRS and the ones that need to be fixed in the underlying engine, usually ModSecurity. Please note that the latter category also includes vulnerabilities that have to be fixed by the so-called "ModSecurity recommended rules": a small group of rules outside CRS. The open-source Coraza engine is not affected as far as we can see and alternative WAF engines, namely the ones using CRS, will need to be checked against all the different findings.

CRS has contacted the ModSecurity developers at Trustwave SpiderLabs early on. Throughout Summer, ModSecurity lead developer Martin Vierula worked on the fixes on this side, partially with support from the bug bounty hunters and CRS developers. We thank Martin for the frank communication and for sharing early patches with our team.

We also informed our sponsors relatively early in the process and we would also like to thank them for their continuing support.

Trustwave has decided to release the updates to ModSecurity without issuing official CVEs. We have reserved four CVEs for our vulnerabilities, but we are fixing a bit more than just the issues covered by the CVEs. The fix for one of the CVEs – CVE-2022-39956 – depends on updating ModSecurity to version 2.9.6 or 3.0.8 (or an updated version with backports of the security fixes in these versions). Without the latest version of ModSecurity, CVE-2022-39956 cannot be mitigated and ModSecurity will refuse to start with the new CRS version unless you remove the new rules that make use of the new ModSecurity functionality (see below). We're mentioning this to highlight the security nature of the new ModSecurity releases, and users and integrators are strongly advised to update their setups.

### Official CVE Advisories for CRS

#### CVE-2022-39955 – Multiple charsets defined in Content-Type header

The OWASP ModSecurity Core Rule Set (CRS) is affected by a partial rule set bypass by submitting a specially crafted HTTP Content-Type header field that indicates multiple character encoding schemes. A vulnerable backend can potentially be exploited by declaring multiple Content-Type "charset" names and therefore bypassing the configurable CRS Content-Type header "charset" allow list. An encoded payload can bypass CRS detection this way and may then be decoded by the backend. The legacy CRS versions 3.0.x and 3.1.x are affected, as well as the currently supported versions 3.2.1 and 3.3.2. Integrators and users are advised to upgrade to 3.2.2 and 3.3.3 respectively.

This vulnerability was discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.

Official CVE: [CVE-2022-39955](https://www.cve.org/CVERecord?id=CVE-2022-39955)

#### CVE-2022-39956 – Content-Type or Content-Transfer-Encoding MIME header fields abuse

The OWASP ModSecurity Core Rule Set (CRS) is affected by a partial rule set bypass for HTTP multipart requests by submitting a payload that uses a character encoding scheme via the Content-Type or the deprecated Content-Transfer-Encoding multipart MIME header fields that will not be decoded and inspected by the web application firewall engine and the rule set. The multipart payload will therefore bypass detection. A vulnerable backend that supports these encoding schemes can potentially be exploited. The legacy CRS versions 3.0.x and 3.1.x are affected, as well as the currently supported versions 3.2.1 and 3.3.2. Integrators and users are advised to upgrade to 3.2.2 and 3.3.3 respectively.

**Important:** The mitigation against these vulnerabilities depends on the installation of the latest ModSecurity version ([v2.9.6](https://github.com/SpiderLabs/ModSecurity/releases/tag/v2.9.6)/[v3.0.8](https://github.com/SpiderLabs/ModSecurity/releases/tag/v3.0.8)) or an updated version with backports of the security fixes in these versions.  
If you fail to update ModSecurity, the webserver/engine will refuse to start with the following error message: `"Error creating rule: Unknown variable: MULTIPART_PART_HEADERS"`.  
You can disable/remove the rule file `REQUEST-922-MULTIPART-ATTACK.conf` from the release in order to allow you to run the latest CRS *without* a fix to CVE-2022-39956, however we advise against this workaround.

Please note that we plan to move the rules in `REQUEST-922-MULTIPART-ATTACK.conf` to the 920 or 921 rule files in the future. The rules are kept separate for the time being to accommodate users who can't update ModSecurity or where the engine does not yet support the new variables/collections.  
  
This vulnerability was discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.  
  
Official CVE: [CVE-2022-39956](https://www.cve.org/CVERecord?id=CVE-2022-39956)

#### CVE-2022-39957 – Charset accept header field resulting in response rule set bypass

The OWASP ModSecurity Core Rule Set (CRS) is affected by a response body bypass. A client can issue an HTTP "accept" header field containing an optional "charset" parameter in order to receive the response in an encoded form. Depending on the "charset", this response can not be decoded by the web application firewall. A restricted resource, access to which would ordinarily be detected, may therefore bypass detection. The legacy CRS versions 3.0.x and 3.1.x are affected, as well as the currently supported versions 3.2.1 and 3.3.2. Integrators and users are advised to upgrade to 3.2.2 and 3.3.3 respectively.

This vulnerability was discovered and reported by [@Karel\_Origin](https://twitter.com/Karel_Origin) (Karel Knibbe) during the Intigriti 1337UP0522 WAF Promotion Event.  
  
Official CVE: [CVE-2022-39957](https://www.cve.org/CVERecord?id=CVE-2022-39957)

#### CVE-2022-39958 – Small range header leading to response rule set bypass

The OWASP ModSecurity Core Rule Set (CRS) is affected by a response body bypass to sequentially exfiltrate small and undetectable sections of data by repeatedly submitting an HTTP range header field with a small byte range. A restricted resource, access to which would ordinarily be detected, may be exfiltrated from the backend, despite being protected by a web application firewall that uses CRS. Short subsections of a restricted resource may bypass pattern matching techniques and allow undetected access. The legacy CRS versions 3.0.x and 3.1.x are affected, as well as the currently supported versions 3.2.1 and 3.3.2. Integrators and users are advised to upgrade to 3.2.2 and 3.3.3 respectively and to configure a CRS paranoia level of 3 or higher.

This vulnerability was discovered and reported by [@Karel\_Origin](https://twitter.com/Karel_Origin) (Karel Knibbe) during the Intigriti 1337UP0522 WAF Promotion Event.  
  
Official CVE: [CVE-2022-39958](https://www.cve.org/CVERecord?id=CVE-2022-39958)

### Description of Additional CRS Security Fixes

#### MIME header abuse via \_charset\_ field

Beyond CVE-2022-39956 which covers the Content-Type and Content-Transfer-Encoding MIME header fields abuse, there is also a fix to prevent potential abuse of the `_charset_` MIME header field which is not covered by the CVE. We assigned this vulnerability a lower severity since we do not know of a parser implementing this field.

This vulnerability was discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.

#### Content-Encoding HTTP header with value "deflate"

ModSecurity is not able to deal with deflated request bodies. If used, the headers can lead to false positives, but also to a partial rule set bypass. Given this is rarely used in practice, CRS is now forbidding the header completely.

This vulnerability was discovered and reported by [@Karel\_Origin](https://twitter.com/Karel_Origin) (Karel Knibbe) during the Intigriti 1337UP0522 WAF Promotion Event.

#### Request body partial rule set bypass via Content-Type "text/plain"

It is possible to bypass the ModSecurity request body processor by issuing a Content-Type header field like "text/plain" or some other simple variant. Backends processing this non-standard request body are thus affected by this partial rule set bypass. We took the opportunity to remove "text/plain" and a batch of other non-standard content types from the default allow list. Please review your configuration if you changed the default value for the CRS setting `tx.allowed_request_content_type`.

This vulnerability was discovered and reported by [0xInfection](https://twitter.com/0xInfection) (Pinaki Mondal) during the Intigriti 1337UP0522 WAF Promotion Event.

#### XML body parser abuse for non-XML request bodies

It is possible to craft certain payloads in a way so that they are accepted by the ModSecurity XML body parser despite not being XML. This leads to a situation where the rule set can be bypassed. ModSecurity covers for this vulnerability with their update, but the new CRS releases also contain adjustments that make this bypass impossible.

This vulnerability was discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.

### Links to Releases, Release Notes, and Resources

- <https://github.com/coreruleset/coreruleset/releases/tag/v3.3.4> ([CHANGES](https://github.com/coreruleset/coreruleset/blob/v3.3/master/CHANGES))
- <https://github.com/coreruleset/coreruleset/releases/tag/v3.2.3> ([CHANGES](https://github.com/coreruleset/coreruleset/blob/v3.2/master/CHANGES))

### ModSecurity Engine Vulnerabilities

#### Use wrong body parser by tricking recommended rules via using bogus multipart boundary

The original ModSecurity ‘recommended rules’ 200000 and 200001 could be tricked into applying the XML or JSON body processors to a request body when the multipart boundary was set to a pattern matching an XML/Soap or JSON content type. The ‘recommended rules’ accompanying the ModSecurity 2.9.6 and 3.0.8 releases fix this problem. As such, all ModSecurity users and integrators are advised to review their ‘recommended rules’ settings and update to the new version that anchors the content type to the beginning of the regular expression.

These vulnerabilities were discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.

#### Using advanced MIME header fields to encode request bodies

CVE-2022-39956 solves the above mentioned vulnerabilities with the help of a new ModSecurity variable `MULTIPART_PART_HEADERS`. This collection, as it is called in ModSecurity parlance, gives you access to advanced MIME header fields. We are using this to deny certain rarely used field names. There is a chance that other bypasses might be discovered in this direction, so please be prepared for future updates in this direction.

Again, this vulnerability was discovered and reported by [@terjanq](https://twitter.com/terjanq) (Jan Gora) during the Intigriti 1337UP0522 WAF Promotion Event.

### Distribution Packages and Containers

We are working with GNU/Linux distributions and packagers to bring you packaged versions of CRS, namely with Debian and therefore the Ubuntu family. The latest unofficial packages are available at <https://modsecurity.digitalwave.hu/> from where they are pushed into the distros.  
The offical CRS docker container at <https://github.com/coreruleset/modsecurity-crs-docker> is being updated as we speak.

### Timeline

- 2022-04-29: Intigriti 1337UP0522 WAF Promotion Event / bug bounty started in cooperation with Yahoo/The Paranoids and OWASP CRS
- 2022-05-12: Trustwave/ModSecurity receives preliminary information of findings
- 2022-05-19: Event ended, all vulnerabilities reported prior to this date
- 2022-06-15: Trustwave/ModSecurity receives full information of findings
- 2022-07-07: CRS sponsors informed about findings (CVE level of details)
- 2022-08-26: Preliminary patches for ModSecurity 2.9.6 and 3.0.8 submitted to CRS team
- 2022-09-08: Release of ModSecurity 2.9.6 and 3.0.8
- 2022-09-19: Release of CRS 3.2.2 and 3.3.3, CVEs

The time between the first reports and the CRS releases with the fix is substantially longer than the industry practice of 90 days. You will notice that CRS took more than a month to submit full information to ModSecurity. When preparing the bug bounty program we assessed our capacity to be around two security findings per week. That would be 100 per year which is a decent number. In the three weeks of the program, we received far more than 100 findings, thus more than a year's worth of findings given our capacity estimate. This overwhelmed our processes and it took us very, very long to identify the critical rule set bypasses among the dozens and dozens of valid rule bypasses.  
Ever since, we have been grinding away with updating the CRS regular expressions to cover for the individual rule bypasses (false negatives) in parallel to fixing the high severity vulnerabilities documented above.

### Sponsors

OWASP CRS is very thankful for the continuous support of its sponsors. The following companies are currently supporting our project:

- VMWare / Avi Networks (GOLD Sponsor)
- F5/NGINX (GOLD Sponsor)
- Microsoft (GOLD Sponsor)
- Bug Bounty Switzerland (SILVER Sponsor)
- Google Cloud Armor (SILVER Sponsor)

### Updates to This Page

2022-09-19 16:08 UTC: Publication  
2022-09-20 08:23 UTC: Update links to CVE.org  
2022-09-20 12:50 UTC: CVE-2022-39958 attribution fixed: Karel Origin  
2022-09-20 16:50 UTC: The 3.3.3 and 3.2.2 releases contained a regression, so we have released 3.3.4 and 3.2.3 releases instead. Download links have been updated to the fixed versions.

This has been a long read. Thank you for your interest.

*Andrew Howe and Christian Folini for the OWASP CRS team*
