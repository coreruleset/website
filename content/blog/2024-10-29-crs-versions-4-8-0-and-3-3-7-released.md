---
author: RedXanadu
categories:
  - Blog
date: '2024-10-29T18:59:58+00:00'
title: CRS versions 4.8.0 and 3.3.7 released
slug: 'crs-versions-4-8-0-and-3-3-7-released'
---

The OWASP ModSecurity Core Rule Set (CRS) team is pleased to announce the release of two new CRS versions: v4.8.0 and v3.3.7.

For downloads and installation instructions, please refer to the [Installation](https://coreruleset.org/docs/deployment/install/) page.

These are security releases which fix a recently discovered partial request body bypass of CRS. On some platforms running CRS v3.3.6 and earlier on the v3 release line or v4.7.0 and earlier on the v4 release line, it is possible to submit a specially crafted multipart or JSON request whose body content will bypass the inspection of the majority of CRS rules on a default installation. CRS users are strongly encouraged to update to a fixed version to resolve this issue.

#### Bypass details

This bypass was possible due to the fact that the default list of allowed request content types in CRS (both v3 and v4) included the content type `multipart/related`, which cannot be processed by current free & open-source WAF engine implementations, and the content types `application/cloudevents+json` and `application/cloudevents-batch+json`, which are not processed by default. This created a situation where a request with body content would be allowed by CRS but the request body could not, or would not, be processed by the engine. Many CRS rules thus lost the ability to perform meaningful inspection of such requests, in the absence of processed and parsed request body content. In particular, the `ARGS` collection (and related collections) was not populated by the engine: many CRS rules rely on inspecting the contents of this important collection.

The newly released fixed versions remove the offending content types from the default list of allowed request content types. New advice is also provided on how to handle additional JSON content types beyond the standard `application/json` content type.

Users making use of additional JSON content types, for example `application/cloudevents+json`, should follow the new advice and ensure that an appropriate rule is in place to enable JSON request body processing for these content types. Most affected users can uncomment and use optional rule 200006 in the file “modsecurity.conf-recommended” to achieve this.

Note that the [official CRS Docker container images](https://github.com/coreruleset/modsecurity-crs-docker), by default, already correctly handle extended JSON types and are therefore not affected by the JSON part of this problem.

#### For users unable to update

Any users unable to update to a fixed version of CRS are strongly encouraged to implement the fix steps themselves by removing the content types `multipart/related`, `application/cloudevents+json`, and `application/cloudevents-batch+json` from the variable `tx.allowed_request_content_type` as set in the files `crs-setup.conf` and `REQUEST-901-INITIALIZATION.conf`. The advice on JSON processing should also be followed.

#### Other release changes

Aside from the security fix, the v4.8.0 release also includes a few other minor changes and improvements as part of the normal release cycle for CRS v4. The full changes included in v4.8.0 can be found on the [GitHub release page](https://github.com/coreruleset/coreruleset/releases/tag/v4.8.0).

Please feel free to contact us with any questions or concerns about this release via the usual channels: directly via the [CRS GitHub repository](https://github.com/coreruleset/coreruleset), in our Slack channel (#coreruleset on [owasp.slack.com](https://owasp.slack.com/)), or on our [mailing list](https://groups.google.com/a/owasp.org/g/modsecurity-core-rule-set-project).

Sincerely,  
Andrew Howe on behalf of the Core Rule Set development team
