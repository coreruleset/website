---
author: amonachesi
categories:
  - Blog
date: '2024-02-14T19:46:50+01:00'
tags:
  - CRS-News
  - Plugins
  - Release
title: Let CRS 4 be your valentine!
url: /2024/02/14/let-crs-4-be-your-valentine/
---


What a Valentine’s Day present we have got for you: today, the Core Rule Set project is releasing CRS 4!

Finally, you may say – and would be absolutely right: it took us a long time to get there. But we wanted to do it right, especially after the bug bounty program we took part in left us with over 500 individual findings in roughly 180 reports. Fixing all these needed more time than we originally thought. But the result is a CRS that has never been more secure.

{{< figure src="images/2024/02/pexels-rdne-stock-project-7755146.png" >}}*© RDNE Stock project (pexels.com)*

And the focus on quality we put in this release is visible in other areas as well, e.g. work on our new quantitative testing framework, extended automation, and the integration of more tests. But we also did a lot of maintenance and cleaning, e.g. breaking up old regular expression patterns and putting them into clean and maintainable formats.

#### New features: Plug-in architecture, early blocking, and more

But apart from work on quality improvements, what novel features does CRS 4 bring? We think, the most exciting is the new **plug-in architecture**. It allows extending your CRS installation with additional functions and thus minimizing your attack surface (for more details see pull requests #[2038](https://github.com/coreruleset/coreruleset/pull/2038), #[2448](https://github.com/coreruleset/coreruleset/pull/2448), #[2404](https://github.com/coreruleset/coreruleset/pull/2404)). And it has allowed us to migrate our pre-made application rule exclusions and less-used functionality to plug-ins. But best of all: the architecture is open to third parties. This means that anybody can build and publish their own plug-in to add the functions they need to their CRS installation.

To be able to coordinate the rule ID namespace (the ID range from 9,500,000–9,999,999 is reserved for CRS plug-ins), we have opened a registry on GitHub that serves as the official place to register plugins and reserve rule ID ranges. So far, the CRS project has published three "official" plug-ins for CRS 4 that are tested and seven that are in the process of being tested while another nine are either yet untested, or still in draft status.

Among the extensions still being tested is an [**antivirus plug-in**](https://github.com/coreruleset/antivirus-plugin) that scans the uploaded file (enabled by default) and the body (disabled by default) of a request. Currently, the plug-in only works with ClamAV but we plan to support other antivirus providers in the future. The plug-in communicates with the antivirus software using a bundled Lua script. No external programs or tools are executed, and there is no need for the antivirus software to run with extended permissions to access scanned data. If the plug-in detects a virus, it will not raise the anomaly score, but block the request immediately.

Another great addition is the **[fake-bot plug-in](https://github.com/coreruleset/fake-bot-plugin)**. This extension adds blocking of bots and impersonators faking well known user-agents in their HTTP requests to CRS. It detects bots pretending to be from Amazon, Apple, Bing, Facebook, Google, LinkedIn, and Twitter. The detection is done using DNS PTR records. Once a fake bot is successfully detected, CRS blocks the requests depending on its configuration. To use the fake-bot plug-in ModSecurity must be compiled with Lua support.

The following official CRS plug-ins are tested and available now: [template](https://github.com/coreruleset/template-plugin), [wordpress-rule-exclusions](https://github.com/coreruleset/wordpress-rule-exclusions-plugin), [nextcloud-rule-exclusions](https://github.com/coreruleset/nextcloud-rule-exclusions-plugin). Still being tested are (besides antivirus and fake-bot): [body-decompress](https://github.com/coreruleset/body-decompress-plugin), [google-oauth2](https://github.com/coreruleset/google-oauth2-plugin), [xenforo-rule-exclusions](https://github.com/coreruleset/xenforo-rule-exclusions-plugin), [phpbb-rule-exclusions](https://github.com/coreruleset/phpbb-rule-exclusions-plugin), [phpmyadmin-rule-exclusions](https://github.com/coreruleset/phpmyadmin-rule-exclusions-plugin). In addition, there are already three tested plug-ins available from third party developers: [roundcube-rule-exclusions-plugin](https://github.com/EsadCetiner/roundcube-rule-exclusions-plugin), [sogo-rule-exclusions-plugin](https://github.com/EsadCetiner/sogo-rule-exclusions-plugin), and [iredadmin-rule-exclusions-plugin](https://github.com/EsadCetiner/iredadmin-rule-exclusions-plugin).

You can find them all (together with the untested ones) in the [plug-in registry](https://github.com/coreruleset/plugin-registry).

Other new features and important fixes in CRS 4 include:

**Early blocking:** Another important new functionality in CRS 4 is the early blocking option (#[1955](https://github.com/coreruleset/coreruleset/pull/1955)). This feature allows the evaluation of anomaly scores at the end of phase 1 (in addition to phase 2) and at the end of phase 3 (in addition to phase 4) when enabled in the new config item `tx.blocking_early`.

**Granular reporting:** We have never been very happy with the redundant 980xxx reporting rules. With CRS 4 you now have granular control over reporting levels (#[2482](https://github.com/coreruleset/coreruleset/pull/2482), #[2488](https://github.com/coreruleset/coreruleset/pull/2488)). There is only one reporting action but there is new and complicated logic with additional rules which decide whether the reporting action runs.

**Collections initialization flag:** Because the newly introduced plug-ins may need collections while the core rules usually don’t, CRS 4 provides a centralized option to initialize and populate collections. This is done through the addition of an `enable_default_collections` flag (#[3141](https://github.com/coreruleset/coreruleset/pull/3141)) to initialize collections for the plug-ins. This way, the global and IP collections (see rule 901320) aren’t initialized by default, as they’re not used by any core (i.e. non-plugin) rules.

**Anomaly score and paranoia levels:** With CRS 4, we have refactored and renamed the anomaly scoring variables and paranoia level definitions (#[2417](https://github.com/coreruleset/coreruleset/pull/2417)). The variables used to count the anomaly score suffered from inconsistencies in naming and use that made it difficult to understand how they work and even led to problems in some cases.

**Compatibility with RE2/Hyperscan:** All formerly PCRE-only regular expressions are now compatible with the RE2 and Hyperscan regular expression engines (#[1868](https://github.com/coreruleset/coreruleset/pull/1868), #[2356](https://github.com/coreruleset/coreruleset/pull/2356), #[2425](https://github.com/coreruleset/coreruleset/pull/2425), #[2426](https://github.com/coreruleset/coreruleset/pull/2426), #[2371](https://github.com/coreruleset/coreruleset/pull/2371), #[2372](https://github.com/coreruleset/coreruleset/pull/2372)). This contributes to CRS portability and gives the WAF engines more space for innovation.

**A better spread:** CRS 4 rules are now better spread over paranoia levels.

#### But wait, there’s more!

Here are a few more interesting updates included in CRS 4:

- New category of rules that detect common web shells in HTTP responses (#[1962](https://github.com/coreruleset/coreruleset/pull/1962), #[2039](https://github.com/coreruleset/coreruleset/pull/2039), #[2116](https://github.com/coreruleset/coreruleset/pull/2116))
- Support for HTTP/3 (#[3218](https://github.com/coreruleset/coreruleset/pull/3218))
- Nightly packages published regularly (#[2207](https://github.com/coreruleset/coreruleset/pull/2207))
- Extended definition of restricted headers to include `Content-Encoding` and `Accept-Charset `by default (#[2780](https://github.com/coreruleset/coreruleset/pull/2780), #[2782](https://github.com/coreruleset/coreruleset/pull/2782))
- Switch to using WordNet instead of ‘spell’ command for finding English words in spell.sh (#[3242](https://github.com/coreruleset/coreruleset/pull/3242))
- Drop HTTP/0.9 support to resolve false positive (#[1966](https://github.com/coreruleset/coreruleset/pull/1966))

In total, there are about 500 changes in CRS 4. This shows what a huge step forward the new release is for CRS.

#### A word on migration

Moving from CRS 3.x to CRS 4.0 is a big step. There are brand new rules and many existing rules have been modified, reorganized, or in some cases removed. Most important: In CRS 4, exclusion rules packages for applications are no longer part of the rule set! They are now dealt with within the plug-in architecture. So, if you’re currently using these rule exclusion packages with CRS 3.x, after the update to 4.0 you will find the packages removed. Instead, you will have to install the respective plug-ins to keep the functionality.

Starting over from scratch in terms of false positive tuning is one way to go about the migration. Another option is to look up the rules you have excluded in the change log and see if there are other rules you need to cover as well. Please check the new `crs-setup.conf` and make sure you are up to date with variable names and formats. We will also follow up with blog posts that give more hands-on advice on the migration for more complex setups.

#### Adopting a new release schedule

CRS 4.0 is the last release following our traditional and very slow release schedule. For the future, we plan to run with a monthly release (so you can expect 4.1 in March 2024). We plan to declare an individual release as long-term support and to continue to update it beyond the release of the next few monthly releases.

#### Change log

You can find all the changes in CRS 4.0 in the change log: <https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md>

#### Thank you, sponsors

*This work would not have been possible without our Gold Sponsors **Google** (<https://www.google.com/>) and **United Security Providers** (<https://united-security-providers.com/>) and our Silver Sponsor **Swiss Post** (<https://www.post.ch/en/about-us/responsibility/information-security-at-swiss-post>). Thank you for supporting CRS!*

*If you think your organization is profiting from CRS so much, you want to become a sponsor too, then please get in touch. Sponsoring is essential for quality open source software.*
