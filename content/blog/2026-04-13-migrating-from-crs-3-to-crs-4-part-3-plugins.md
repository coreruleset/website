---
author: fzipi
categories:
  - Blog
date: '2026-04-13T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
  - Plugins
images:
  - /images/2026/04/pexels-markusspiske-168866.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 3: The Plugin Architecture'
slug: 'migrating-crs-3-to-4-part-3-plugins'
---

This is Part 3 of the [CRS 3.3 → 4.25 LTS migration series]({{< ref "blog/2026-03-30-migrating-from-crs-3-to-crs-4-part-1-overview.md" >}}). Part 2 covered `crs-setup.conf` changes. This post covers the plugin architecture — the most structurally significant change in CRS 4, and the one that requires the most hands-on action from operators who used application exclusion packages in CRS 3.

## The Key Change: Application Exclusions Are No Longer in Core

In CRS 3.3, the release tarball included a set of optional rule exclusion packages. If you ran WordPress, Nextcloud, phpBB, phpMyAdmin, Drupal, or a handful of other applications, you could include these files to suppress false positives specific to those applications:

```
rules/REQUEST-903.9001-WORDPRESS-EXCLUSIONS.conf
rules/REQUEST-903.9002-CPANEL-EXCLUSIONS.conf
rules/REQUEST-903.9003-NEXTCLOUD-EXCLUSIONS.conf
rules/REQUEST-903.9004-DOKUWIKI-EXCLUSIONS.conf
rules/REQUEST-903.9005-CPANEL-EXCLUSIONS.conf
rules/REQUEST-903.9006-XENFORO-EXCLUSIONS.conf
rules/REQUEST-903.9007-PHPBB-EXCLUSIONS.conf
rules/REQUEST-903.9008-PHPMYADMIN-EXCLUSIONS.conf
...
```

In CRS 4, these files are gone from the release tarball. They have been moved to independent plugin repositories. **If you relied on any of these files in CRS 3, they will simply be absent after upgrading to CRS 4 unless you explicitly install the corresponding plugins.**

This change was intentional and security-motivated. Having application exclusion rules bundled in core meant that a bug in, say, the WordPress exclusion package affected every CRS installation — including those that do not run WordPress. By moving exclusions to opt-in plugins, the default attack surface is smaller. (A previous incident where a bundled exclusion package had a critical vulnerability validated this reasoning.)

{{< figure src="/images/2026/04/pexels-markusspiske-168866.jpg" caption="Modular architecture: from monolith to plugins" attr="Markus Spiske on Pexels" attrlink="https://www.pexels.com" >}}

## What Is the Plugin Architecture?

A plugin is a set of rules packaged as three optional files:

```
plugins/<plugin-name>-config.conf   # plugin configuration
plugins/<plugin-name>-before.conf   # rules to run before CRS rules
plugins/<plugin-name>-after.conf    # rules to run after CRS rules
```

These files are loaded via three `Include` statements that must be present in your WAF configuration, positioned around the main CRS rules `Include`:

```apache
Include crs/crs-setup.conf

Include crs/plugins/*-config.conf
Include crs/plugins/*-before.conf

Include crs/rules/*.conf

Include crs/plugins/*-after.conf
```

This load order matters. Rules in `*-before.conf` run before CRS has processed the request — this is where exclusion rules go, so they can suppress matching before CRS rules fire. Rules in `*-after.conf` run after CRS — this is where scoring rules that need to know the CRS result go.

The three `Include` directives for plugins are new in CRS 4. If you are upgrading an existing installation, you must add them to your WAF configuration. The CRS release includes three empty placeholder files in the `plugins/` directory so the `Include` statements do not produce errors when no plugins are installed.

## The Plugin Registry

The [CRS Plugin Registry](https://github.com/coreruleset/plugin-registry) is the central catalogue of all known CRS plugins — official, community-contributed, and third-party. It serves two purposes:

1. **Discovery**: it lists every available plugin with a description, repository link, and quality tier.
2. **Namespace management**: it tracks which rule ID sub-range (within `9,500,000–9,999,999`) has been assigned to each plugin, preventing conflicts between plugins from different authors.

Before installing any plugin, check the registry to confirm you are using the current repository URL and to see whether the plugin is listed as tested, in-testing, or draft. Quality tiers matter: tested plugins have gone through the same review process as CRS core rules; draft plugins may have breaking changes or incomplete coverage.

When you write your own rules or custom plugins, reserve your rule ID range through the registry to avoid conflicts with plugins you may install later.

## Mapping: CRS 3 Exclusion Packages to CRS 4 Plugins

Here is the complete mapping between CRS 3 application exclusion rule files and their CRS 4 plugin equivalents, sourced directly from the registry:

| CRS 3 file | CRS 4 plugin | Rule ID range | Repository |
|---|---|---|---|
| `REQUEST-903.9001-WORDPRESS-EXCLUSIONS.conf` | `wordpress-rule-exclusions-plugin` | 9,507,000–9,507,999 | [coreruleset/wordpress-rule-exclusions-plugin](https://github.com/coreruleset/wordpress-rule-exclusions-plugin) |
| `REQUEST-903.9002-CPANEL-EXCLUSIONS.conf` | `cpanel-rule-exclusions-plugin` | 9,510,000–9,510,999 | [coreruleset/cpanel-rule-exclusions-plugin](https://github.com/coreruleset/cpanel-rule-exclusions-plugin) |
| `REQUEST-903.9003-NEXTCLOUD-EXCLUSIONS.conf` | `nextcloud-rule-exclusions-plugin` | 9,508,000–9,508,999 | [coreruleset/nextcloud-rule-exclusions-plugin](https://github.com/coreruleset/nextcloud-rule-exclusions-plugin) |
| `REQUEST-903.9004-DOKUWIKI-EXCLUSIONS.conf` | `dokuwiki-rule-exclusions-plugin` | 9,509,000–9,509,999 | [coreruleset/dokuwiki-rule-exclusions-plugin](https://github.com/coreruleset/dokuwiki-rule-exclusions-plugin) |
| `REQUEST-903.9005-DRUPAL-EXCLUSIONS.conf` | `drupal-rule-exclusions-plugin` | 9,506,000–9,506,999 | [coreruleset/drupal-rule-exclusions-plugin](https://github.com/coreruleset/drupal-rule-exclusions-plugin) |
| `REQUEST-903.9006-XENFORO-EXCLUSIONS.conf` | `xenforo-rule-exclusions-plugin` | 9,511,000–9,511,999 | [coreruleset/xenforo-rule-exclusions-plugin](https://github.com/coreruleset/xenforo-rule-exclusions-plugin) |
| `REQUEST-903.9007-PHPBB-EXCLUSIONS.conf` | `phpbb-rule-exclusions-plugin` | 9,512,000–9,512,999 | [coreruleset/phpbb-rule-exclusions-plugin](https://github.com/coreruleset/phpbb-rule-exclusions-plugin) |
| `REQUEST-903.9008-PHPMYADMIN-EXCLUSIONS.conf` | `phpmyadmin-rule-exclusions-plugin` | 9,513,000–9,513,999 | [coreruleset/phpmyadmin-rule-exclusions-plugin](https://github.com/coreruleset/phpmyadmin-rule-exclusions-plugin) |

Note that CRS 3 did not ship Drupal exclusions as a standalone numbered file in all releases — if you had a Drupal exclusion file, it maps to `drupal-rule-exclusions-plugin`. Verify your specific CRS 3.3.x tarball contents if you are unsure which files you had.

### Community-Contributed Rule Exclusion Plugins

The registry also lists third-party plugins for applications that never had CRS 3 bundled exclusions:

| Application | Rule ID range | Repository | Maintainer |
|---|---|---|---|
| Roundcube | 9,519,000–9,519,999 | [EsadCetiner/roundcube-rule-exclusions-plugin](https://github.com/EsadCetiner/roundcube-rule-exclusions-plugin) | EsadCetiner |
| SOGo | 9,520,000–9,520,999 | [EsadCetiner/sogo-rule-exclusions-plugin](https://github.com/EsadCetiner/sogo-rule-exclusions-plugin) | EsadCetiner |
| iRedAdmin | 9,521,000–9,521,999 | [EsadCetiner/iredadmin-rule-exclusions-plugin](https://github.com/EsadCetiner/iredadmin-rule-exclusions-plugin) | EsadCetiner |
| Plausible Analytics | 9,528,000–9,528,999 | [EsadCetiner/plausible-rule-exclusions-plugin](https://github.com/EsadCetiner/plausible-rule-exclusions-plugin) | EsadCetiner |

For any application not listed here, check the registry directly — it is updated as new plugins are submitted. If no plugin exists for your application, you will need to write your own or re-create the relevant exclusions manually in `REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf`.

## How to Install a Plugin

### Method 1: Copy the files (simple)

Download the plugin repository and copy the `.conf` and data files into your `plugins/` directory:

```bash
# Example: installing the WordPress exclusions plugin
git clone https://github.com/coreruleset/wordpress-rule-exclusions-plugin.git /tmp/wp-plugin
cp /tmp/wp-plugin/plugins/* /path/to/crs/plugins/

# If there is a .example config file, rename it
mv /path/to/crs/plugins/wordpress-rule-exclusions-plugin-config.conf.example \
   /path/to/crs/plugins/wordpress-rule-exclusions-plugin-config.conf
```

Review the config file for any options to set, then reload your WAF.

### Method 2: Symlinks (recommended for maintainability)

Clone the plugin to a permanent location and create symlinks in `plugins/`. This makes updates as simple as `git pull`:

```bash
git clone https://github.com/coreruleset/wordpress-rule-exclusions-plugin.git \
    /opt/crs-plugins/wordpress-rule-exclusions-plugin

# Rename the example config
cp /opt/crs-plugins/wordpress-rule-exclusions-plugin/plugins/wordpress-rule-exclusions-plugin-config.conf.example \
   /opt/crs-plugins/wordpress-rule-exclusions-plugin/plugins/wordpress-rule-exclusions-plugin-config.conf

# Symlink each file into the CRS plugins directory
for f in /opt/crs-plugins/wordpress-rule-exclusions-plugin/plugins/*; do
    ln -s "$f" /path/to/crs/plugins/
done
```

To update: `git -C /opt/crs-plugins/wordpress-rule-exclusions-plugin pull` and reload.

## Enabling Collections for Plugins

Some plugins (the fake-bot plugin, the auto-decoding plugin) need the GLOBAL and IP collections initialized before they can run. In CRS 4 these collections are not initialized by default — you must set `tx.enable_default_collections=1` in your `crs-setup.conf` to enable them.

Check each plugin's documentation for whether it needs collections. If any plugin you install requires them, enable the flag. It is safe to enable it even if only some of your plugins need it.

## Using Plugins on Multi-Application Reverse Proxies

If your WAF fronts multiple applications, you likely do not want WordPress exclusion rules to apply to requests going to your API or your phpBB forum. CRS 4 plugins support per-virtual-host scoping via `SecWebAppID` (ModSecurity) or the `Host` header (Coraza):

```apache
# ModSecurity: disable the WordPress plugin for non-WordPress virtual hosts
SecRule &TX:wordpress-rule-exclusions-plugin_enabled "@eq 0" \
    "id:9507010,phase:1,pass,nolog,chain"
    SecRule WebAppID "!@streq wordpress" \
        "t:none,setvar:'tx.wordpress-rule-exclusions-plugin_enabled=0'"
```

Most official plugins include this pattern commented out in their config file. Review each plugin's `*-config.conf` for the scoping example.

## Capability Plugins (Not in CRS 3)

Beyond rule exclusions, the registry includes capability plugins that add functionality with no CRS 3 equivalent. These are worth knowing about even if you are not migrating from an exclusion package:

| Plugin | Rule ID range | Description |
|---|---|---|
| [antivirus-plugin](https://github.com/coreruleset/antivirus-plugin) | 9,502,000–9,502,999 | Integrates ClamAV to scan uploaded files and optionally request bodies. Blocks on detection without raising the anomaly score. |
| [fake-bot-plugin](https://github.com/coreruleset/fake-bot-plugin) | 9,504,000–9,504,999 | DNS PTR verification for requests claiming to be Google, Bing, Amazon, Facebook, Apple, LinkedIn, and Twitter. Requires Lua. |
| [body-decompress-plugin](https://github.com/coreruleset/body-decompress-plugin) | 9,503,000–9,503,999 | Decompresses gzip/deflate response bodies for inspection by CRS rules. |
| [auto-decoding-plugin](https://github.com/coreruleset/auto-decoding-plugin) | 9,501,000–9,501,999 | Applies additional decode transformations at PL3/PL4 to catch evasions through double-encoding. |
| [dos-protection-modsecurity-plugin](https://github.com/coreruleset/dos-protection-modsecurity-plugin) | 9,514,000–9,514,999 | Rate-based DoS protection using ModSecurity collections. Requires `tx.enable_default_collections=1`. |
| [google-oauth2-plugin](https://github.com/coreruleset/google-oauth2-plugin) | 9,505,000–9,505,999 | Exclusions for Google OAuth2 flows. |
| [incubator-plugin](https://github.com/coreruleset/incubator-plugin) | 9,900,000–9,999,999 | Experimental rules being tested before promotion to core. Useful for running cutting-edge detections in detection-only mode. |

## Rule ID Namespace

The rule ID range `9,500,000–9,999,999` is reserved for CRS plugins. This is important if you have written any custom rules in that range — they may conflict with plugin rules. Check the [plugin registry](https://github.com/coreruleset/plugin-registry) for the assigned sub-ranges, and renumber any conflicting custom rules before installing plugins.

## What's Next

[Part 4]({{< ref "blog/2026-04-20-migrating-from-crs-3-to-crs-4-part-4-scoring.md" >}}) covers the anomaly scoring and reporting changes — including the variable renames, the new granular reporting model, early blocking, and how the redistribution of rules across paranoia levels affects your anomaly score baseline.

{{< related-pages "Migration" "CRS-v4" >}}
