---
author: fzipi
categories:
  - Blog
date: '2026-03-30T09:00:00-03:00'
tags:
  - CRS-News
  - Migration
  - CRS-v4
images:
  - /images/2026/04/pexels-toulouse-18332033.jpg
title: 'Migrating from CRS 3.3 to CRS 4.25 LTS — Part 1: Overview'
slug: 'migrating-crs-3-to-4-part-1-overview'
---

The release of [CRS v4.25.0 LTS]({{< ref "blog/2026-03-28-announcing-crs-v4-25-lts.md" >}}) marks the moment the CRS 4 generation has its long-term support anchor. If you have been running CRS 3.3.x — waiting for stability before committing to an upgrade — that moment is now.

This is the first post in a series walking through everything you need to know to migrate from CRS 3.3.9 (the last CRS 3 LTS release) to CRS 4.25.0 LTS. The series is not a quick upgrade guide. It is a deliberate, post-by-post treatment of each dimension of the migration so that you can plan and execute without surprises.

{{< figure src="/images/2026/04/pexels-toulouse-18332033.jpg" caption="Charting the path from CRS 3 to CRS 4" attr="Maël BALLAND on Pexels" attrlink="https://www.pexels.com" >}}

## Why Migrate?

CRS 3.3.x is in security-only maintenance. It receives backports for confirmed security vulnerabilities but nothing else: no false positive fixes, no new detections, no engine compatibility improvements. Every month you stay on CRS 3.3.x, the gap between your deployment and the state of the art widens.

CRS 4.25.0 LTS closes that gap and gives you a new stability baseline. Its [backport policy](https://github.com/coreruleset/coreruleset/blob/lts/v4.25.x/BACKPORT_POLICY.md) is explicit about what goes in (security fixes, regressions, critical false positive fixes) and what does not (new features, refactoring, toolchain changes). You get meaningful improvements without being forced to track monthly releases.

## What Changed at a Glance

CRS 4 is not a drop-in replacement for CRS 3. There are roughly 500 changes between the two release lines. The ones that matter most for migration fall into a handful of categories:

**Plugin architecture.** This is the biggest structural change. Application-specific rule exclusion packages — previously shipped as optional files inside the CRS release tarball — are no longer part of the core rule set. They are now separate plugins, installed independently. If you use any application exclusion package (WordPress, Nextcloud, phpBB, phpMyAdmin, or others), you will need to install the corresponding plugin before your existing exclusion coverage is restored.

**Configuration file changes.** The `crs-setup.conf` file has new variables, renamed variables, and removed variables. You cannot simply drop your old `crs-setup.conf` into a CRS 4 installation and expect things to work. Anomaly scoring variables were renamed for consistency, and several new options were added.

**Rule-level changes.** Hundreds of rules were modified, reorganized, or removed. Many rules moved between paranoia levels as part of a broad effort to spread detection better across PL1–PL4. New rule categories were added (notably, response-phase web shell detection). Some HTTP behaviours that were tolerated in CRS 3 (HTTP/0.9) were dropped, and new ones were added (HTTP/3, RE2/Hyperscan compatibility).

**Anomaly scoring and reporting.** The variables used to accumulate and report anomaly scores were refactored. The old `980xxx` reporting rules were replaced with new, granular reporting logic. A new `blocking_early` option allows anomaly evaluation at the end of phase 1 (in addition to phase 2) and at the end of phase 3 (in addition to phase 4).

**Engine compatibility.** All formerly PCRE-only regular expressions are now compatible with the RE2 and Hyperscan engines. ModSecurity v2, ModSecurity v3 (libmodsecurity), and Coraza are all supported, though with differences in capability.

## What This Migration Is Not

It is worth being direct about what this migration is not.

**It is not a drop-in upgrade.** Running `cp -r crs4/ crs3/` and reloading your WAF will cause problems. Your old `crs-setup.conf` has variables that no longer exist in CRS 4 and is missing variables that CRS 4 requires. Your old exclusion rules may reference rule IDs that have changed. Your application exclusion packages will simply be absent until you install their plugin replacements.

**It does not preserve your false positive tuning automatically.** Rules have moved between paranoia levels. Rule IDs have changed or been removed. Exclusions you wrote against specific rule IDs in CRS 3 need to be reviewed against the CRS 4 rule set before you go live.

**It does not require starting from scratch.** A systematic approach — covered in detail in Part 6 of this series — lets you carry forward your existing tuning with a clear mapping between old and new rule IDs.

## What to Expect From Each Post in the Series

The series covers the migration in six more posts after this one:

- **Part 2: Configuration** — A side-by-side walk through the `crs-setup.conf` changes, including every renamed and new variable. Includes a migration checklist.
- **Part 3: Plugin Architecture** — The conceptual model, how to install plugins, the official plugin registry, and a mapping from every CRS 3 application exclusion package to its CRS 4 plugin equivalent.
- **Part 4: Anomaly Scoring and Reporting** — The renamed scoring variables, the new reporting model, early blocking, and how paranoia level redistribution affects your anomaly score baseline.
- **Part 5: Rule Changes** — New rule categories, removed and reorganized rules, RE2/Hyperscan compatibility, and how to audit your existing `SecRuleRemoveById` and exclusion rules against the new rule set.
- **Part 6: False Positive Tuning** — Two migration strategies (start fresh vs. carry over), a step-by-step method for mapping old exclusions to new rule IDs, and how to run a production migration in shadow mode.
- **Part 7: Engine-Specific Notes** — The CRS 4 engine support matrix, differences between ModSecurity v2, ModSecurity v3, and Coraza, and the container image tagging scheme.

## Before You Start

Before reading the rest of this series, do two things.

First, download CRS v4.25.0 and open the `crs-setup.conf.example` alongside your existing `crs-setup.conf`. Having both files open makes the configuration changes in Part 2 immediately concrete.

Second, open the [CRS 4.0 CHANGES.md](https://github.com/coreruleset/coreruleset/blob/v4.0/dev/CHANGES.md) on GitHub. It is a long file, but it is the authoritative record of what changed. You do not need to read it end to end now — the series will reference specific entries — but knowing it exists and how to search it will be useful throughout.

The next post covers the configuration file changes in detail.

{{< related-pages "Migration" "CRS-v4">}}
