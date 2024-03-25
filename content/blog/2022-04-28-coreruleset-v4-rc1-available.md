---
author: lifeforms
categories:
  - Blog
date: '2022-04-28T21:20:10+02:00'
title: Core Rule Set v4.0.0 Release Candidate 1 available
url: /2022/04/28/coreruleset-v4-rc1-available/
---


The OWASP ModSecurity Core Rule Set team is proud to announce the Release Candidate 1 for the upcoming CRS v4.0.0 release. The release candidate is available from our [installation page](https://coreruleset.org/installation/); see also the upgrade notes on that page.

**CRS 4 contains many important changes, such as:**

- A plugin architecture for extending CRS and minimizing attack surface. Application exclusion sets and less-used functionality have been migrated from the CRS to [plugins](https://coreruleset.org/docs/concepts/plugins/). (See our [plugin registry](https://github.com/coreruleset/plugin-registry) for the extensive list of existing plugins.)
- [Early blocking](https://coreruleset.org/20220302/the-case-for-early-blocking/)
- <span style="color: var(--ast-global-color-3); font-size: 1rem;">Granular control over reporting levels</span>
- All formerly PCRE-only regular expressions have been updated to be compatible with Re2/Hyperscan WAF engines
- We now publish [nightly packages](https://github.com/coreruleset/coreruleset/releases) of the development branch
- We refactored and renamed the anomaly scoring variables and paranoia level definitions
- HTTP/0.9 support has been dropped to resolve false positives.

**CRS 4 contains many new detections:**

- Detect Log4j / Log4Shell
- Detect Spring4Shell
- Detect JavaScript prototype pollution
- Detect common webshells by inspecting response
- Detect path traversal in file upload
- Detect common IP-based SSRF targets
- Detect email protocol attacks
- Improved RCE detection
- Improved SQLi detection
- Expanded blocklists to prevent access to AWS cli files, /proc and /sys files, and many other sensitive files
- Detect many new scanners and bots

CRS 4 also contains many improvements to lower the amount of false alarms. Also, we fixed a number of bypasses in existing rules. We also addressed various performance and ReDoS issues.

A lot of effort also went into improving our test suite, so that 100% of our rules are now covered by tests!

Finally, we have worked on creating extensive documentation about all aspects of the CRS. You can find it under the [Documentation](https://coreruleset.org/docs/) section of our website. If you would like to make improvements, please go to the [repository](https://github.com/coreruleset/documentation/) and submit your pull request!

For those wanting to try CRS 4, it is important to quickly touch upon the new plugin architecture. Some parts of CRS 3, such as the application exclusion rules (WordPress, Drupal, etc.), were split off into "plugins". As an admin, you can choose to install plugins or leave them out. In this way, we can more swiftly update plugins (for instance to deal with application updates), and we decrease the attack surface for admins who are not interested in their functionality. If you used the application exclusions in CRS 3, you will need to download the relevant plugin files and put them in your `plugins` subdirectory in CRS 4. [See here for extended information about working with plugins.](https://coreruleset.org/docs/configuring/plugins/)

Please see the [CHANGES.md](https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md) file for a full list of the more than 200 changes, improvements and fixes. Each CHANGES entry links to the relevant pull requests, so you can dive into the specifics of a certain change.

If you try out our release candidate, we will be very eager to receive your feedback. You can [report any issues on GitHub](https://github.com/coreruleset/coreruleset/issues/new/choose). Be sure to mention the CRS version, so we can handle RC issues as quickly as possible. Depending on the feedback, we will possibly release more Release Candidates, while we get a firmer picture and finalize our schedule for the final release.

If you have questions, the quickest way to get in touch with us directly is to [join the #coreruleset channel on the OWASP Slack](https://coreruleset.org/20181003/owasp-crs-slack/).

I want to thank all our [developers and outside contributors](https://github.com/coreruleset/coreruleset/blob/v4.0/main/CONTRIBUTORS.md) for helping us make the best CRS version yet!

Kind regards,  
Walter Hop  
Core Rule Set Co-Lead
