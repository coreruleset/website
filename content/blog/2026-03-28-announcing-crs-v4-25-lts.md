---
author: fzipi
categories:
  - Blog
date: '2026-03-21T12:00:00-03:00'
title: 'Announcing CRS v4.25.0 LTS: Long-Term Support for CRS 4'
slug: 'announcing-crs-v4-25-lts'
---

We are excited to announce that CRS v4.25.0 is the first Long-Term Support (LTS) release for the CRS 4 series. This is a milestone we have been working towards for over two years, and it marks the point where organizations waiting for a stability commitment can confidently deploy CRS 4 in their production environments.

## What This Means for Users

If you are currently running CRS 4.x, the v4.25.0 LTS gives you a stable foundation that will receive security patches and critical bug fixes for an extended period — without being forced to track our rapid development cycle. You get the protection, without the churn.

If you are still running CRS 3.3.x and have been waiting for an LTS signal to migrate, this is it. CRS v4.25.0 LTS is the release to migrate to.

The v4.25.x LTS release line will receive security fixes until **Q3 2027**. After that date, no further releases will be made on this branch, and users will be directed to upgrade to the current stable or a future LTS release.

## What Gets Backported to the LTS

We have published a formal [Backport Policy](https://github.com/coreruleset/coreruleset/blob/lts/v4.25.x/BACKPORT_POLICY.md) that defines exactly what goes into the LTS branch. In short:

**Always backported**: security fixes (CVEs and bypass advisories), regression fixes, critical false positive fixes affecting common deployments at PL1, and engine compatibility fixes.

**Never backported**: new rules, new features, paranoia level changes, refactoring, toolchain upgrades, or cosmetic changes.

This policy exists to protect LTS users from surprises. Every change that lands on `lts/v4.25.x` has already been tested on our `main` development branch and is cherry-picked with care.

## Lessons from CRS 3.3

Those who followed our CRS 3.3 maintenance will know that backporting is not without risk. In 2022, a backport from our development branch introduced a regression where some Paranoia Level 2 rules activated in PL1. The rules did not harm security, but they introduced unexpected false positives for PL1 users.

We have applied the lessons from that experience to the v4.25.x LTS process:

- **Single branch, no dev/master split.** The CRS 3.3 line used separate `v3.3/dev` and `v3.3/master` branches, which added complexity with limited benefit. The LTS uses a single `lts/v4.25.x` branch that is always in a releasable state.

- **Strict cherry-pick discipline.** Every backport is done with `git cherry-pick -x` to preserve traceability, and every cherry-pick commit references the original PR. Any adaptation required (version strings, variable names) is documented in the commit message.

- **Frozen CI pipeline.** The CI/CD configuration on the LTS branch is pinned at the time of the fork. We do not upgrade go-ftw, Docker images, or GitHub Actions versions on the LTS branch unless strictly necessary. Boring CI is good CI for an LTS.

- **Mandatory review.** Every backport PR requires review from a core developer who did not author the cherry-pick.

## Release Cadence

LTS point releases (v4.25.1, v4.25.2, etc.) will follow a **quarterly** schedule, unless a security fix demands an out-of-band release. Quarterly releases batch all accumulated backports and are announced through our standard channels: this blog, the mailing list, and Twitter/X.

Security-only out-of-band releases are published as soon as the fix is ready and tested, accompanied by a security advisory.

## Branch and Tagging Structure

For those who want the technical details:

```
main              ──────────────────────────────────────► (v4.26.0-dev, v4.27.0, ...)
                         │
                         └── lts/v4.25.x  ──────────────► (v4.25.1, v4.25.2, ...)
                              (forked at v4.25.0 tag)
```

Development of new rules, features, and improvements continues on `main`. The `lts/v4.25.x` branch is a long-lived branch that receives only targeted backports. PRs that qualify for backport are labeled `backport:lts-4.25` on GitHub, so contributors can see at a glance which changes are destined for the LTS.

Docker container images for the LTS will be published with tags `4.25-lts` (floating, always points to latest point release) and `4.25.N-lts` (pinned to a specific point release) for both the ModSecurity and Coraza container images.

## Updated Security Policy

We have updated our [Security Policy](https://github.com/coreruleset/coreruleset/blob/main/SECURITY.md) to reflect the LTS support commitment. The supported versions table now includes v4.25.x LTS alongside the two latest stable releases. Security vulnerabilities affecting the LTS will be patched with the same priority as vulnerabilities affecting the current stable line.

## Documentation

The full LTS maintenance documentation is available in the repository:

- [BACKPORT_POLICY.md](https://github.com/coreruleset/coreruleset/blob/lts/v4.25.x/BACKPORT_POLICY.md) — defines what is and is not backported.
- [LTS Release Procedure](https://github.com/coreruleset/coreruleset/wiki/LTS-Release-Procedure) — the step-by-step process for LTS point releases.
- [SECURITY.md](https://github.com/coreruleset/coreruleset/blob/main/SECURITY.md) — updated supported versions and reporting instructions.

## Thank You to Our Sponsors

As we discussed in our [earlier blog post]({{< ref "blog/2024-11-04-securing-the-maintenance-of-a-crs-4-lts-release.md" >}}), maintaining an LTS release line is a significant investment for an open-source project. The time spent on backporting, testing, and releasing LTS point releases is time not spent on new features. We are grateful to our sponsors who make this possible.

We continue to welcome sponsorship for the LTS initiative. If your organization depends on OWASP CRS and values the stability of an LTS release, please consider supporting us. Sponsorship can take the form of direct maintenance contributions or financial support — both are equally valuable. Reach out to *felipe \[dot\] zipitria \[at\] owasp \[dot\] org* if you are interested.

## How to Get Started

If you are deploying CRS for the first time or migrating from CRS 3.3, start with v4.25.0:

```bash
# Download
wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v4.25.0.tar.gz

# Verify (import our GPG key first — see SECURITY.md)
wget https://github.com/coreruleset/coreruleset/releases/download/v4.25.0/coreruleset-4.25.0.tar.gz.asc
gpg --verify coreruleset-4.25.0.tar.gz.asc v4.25.0.tar.gz
```

Or use our Docker images:

```bash
# ModSecurity + Apache
docker pull owasp/modsecurity-crs:4.25-lts-apache

# ModSecurity + Nginx
docker pull owasp/modsecurity-crs:4.25-lts-nginx

# Coraza + Caddy
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-caddy

# Coraza + Nginx (experimental)
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-nginx

# Coraza + Apache (experimental)
docker pull ghcr.io/coreruleset/coraza-crs:4.25-lts-apache
```

For installation and configuration instructions, see our [documentation](https://coreruleset.org/docs/).

## What Comes Next

Development on `main` continues at full speed. New rules, new detection categories, toolchain improvements, and engine integrations will keep landing on `main` and shipping in regular stable releases. The LTS gives you the option to stay on a known-good baseline while we push the boundaries forward.

We are soon migrating to `crslang` in our rules: this will start the process for our next major release. I'll write a new post intrucing this change, what it implies, and how it will affect your daily life.

We are committed to making OWASP CRS the best open-source WAF rule set available. The v4.25.0 LTS is a key part of that commitment — stability for those who need it, innovation for those who want it.

*The OWASP CRS Team*
