---
title: 'Announcing CRS 4 LTS Release Timeline - Moving Forward Despite Sponsorship Challenges'
date: '2025-12-14'
author: fzipi
description: "The CRS project announces its Long-Term Support release timeline for CRS 4, committing to one-year LTS cycles starting Q1 2026 despite the absence of dedicated corporate sponsorship."
categories:
  - Blog
---

During our recent developer retreat in Bern, the CRS core team made important decisions about the future of Long-Term Support for CRS 4. Today, we're announcing our LTS release timeline and sharing an honest update about the challenges we face in securing dedicated sponsorship for this critical work.

## Why We're Rethinking LTS Duration

Consider this: would you trust an antivirus with signatures that are five years old? Of course not. Yet that's essentially what extended LTS periods can create in web application security.

Five years is an eternity in web and API security. Attack techniques evolve, new vulnerabilities emerge, and threat landscapes shift dramatically. While maintaining old rules provides some protection, it also creates a dangerous false sense of security — organizations may believe they're fully protected when they're actually missing defenses against modern attack vectors.

This is why CRS is moving away from the extended LTS model we used for CRS 3.3, which was maintained for nearly five years. Our commitment to protecting our user base means providing security rules that remain effective against contemporary threats, not just legacy attack patterns. We also work incredibly hard with each release to lower our false positive ratio, continuously refining rules based on real-world traffic patterns and feedback. These improvements don't just make CRS easier to use, they make it more effective by allowing organizations to run at stricter paranoia levels without operational disruption.

Annual LTS releases strike the right balance: stable enough for production deployments requiring predictability, recent enough to maintain effective protection against modern threats, and sustainable enough for our volunteer-driven development team to maintain properly.

## Our LTS Release Plan

After extensive discussions at the Dev Retreat 2025, we've committed to the following LTS strategy:

* **One-year LTS release cycles**: We will target annual Long-Term Support releases to provide stability while maintaining our development momentum.
* **First CRS 4 LTS in Q1 2026**: The inaugural LTS release for CRS 4 will arrive in the first quarter of 2026, giving organizations the stability signal many have been waiting for.
* **Support timeline**: Each LTS version will be supported until the release of the next LTS, with previous LTS support ending Q3 following the new LTS release.
* **CRS 3.3.x end-of-life**: Following this timeline, CRS 3.3.x support will officially expire in Q3 2026.

This approach balances the needs of organizations requiring stability with our commitment to continuous security improvement and innovation.

## The Sponsorship Challenge

In November 2024, we [made a public call for sponsorship](https://coreruleset.org/20241106/securing-the-maintenance-of-a-crs-4-lts-release/) to support the maintenance of CRS 4 LTS releases. We outlined two paths forward: direct support through corporate partners taking over LTS maintenance, or indirect support through financial sponsorship allowing us to commission this work from within our developer community.

We were transparent about the costs involved. Maintaining an LTS version requires substantial ongoing work including backporting critical changes, maintaining parallel testing infrastructure, managing CI/CD pipelines for older codebases, and the inevitable drain on developer mindshare as resources split between new development and maintenance of stable releases.

The reality we face today is that **we still do not have dedicated corporate supporters for LTS releases**. Despite CRS being deployed by major organizations worldwide, and despite the clear value an LTS provides to these organizations planning their migration from CRS 3.3, our call for sponsorship has not materialized into the commitments we need.

## Moving Forward Anyway

Here's what sets the CRS project apart: **we're doing it anyway**.

The CRS team understands in the importance of Long-Term Support releases for the security community. Organizations need stable, well-maintained versions they can depend on for extended periods. Security infrastructure demands predictability and reliability. The absence of corporate sponsorship won't stop us from delivering on this commitment.

This decision comes at a cost, however. Our developers will balance LTS maintenance with ongoing development, new feature work, and the innovation that keeps CRS at the cutting edge of web application security. We'll manage parallel CI/CD pipelines and testing infrastructure from our existing resources. The work will be harder, and progress on new features may be slower, but we're committed to serving the community that depends on us.

A major change in our approach is the significantly shortened LTS cycle. Previous releases like CRS 3.3 have been maintained for nearly five years - an extraordinarily long support period that, while valuable to users, proved unsustainable for the development team. Our new model commits to a fixed one-year support period for each LTS release, plus an additional six months of overlap after the next LTS arrives. This 18-month window gives downstream providers and organizations ample time to plan and execute migrations while keeping the maintenance burden manageable for our volunteer-driven project.

## A Call to Action

While we're moving forward with our LTS plan regardless of sponsorship, this doesn't mean the need for support has disappeared. Organizations benefiting from CRS 4 LTS can still make a difference:

* **Financial sponsorship** helps us dedicate developer time specifically to LTS maintenance without compromising new development.
* **Direct involvement** from companies willing to contribute engineering resources to LTS maintenance work.
* **General project support** through our existing [sponsorship programs](https://owasp.org/donate/?reponame=www-project-modsecurity-core-rule-set&title=OWASP+ModSecurity+Core+Rule+Set).

Organizations using CRS to protect their applications have a vested interest in ensuring the project's long-term health. Every contribution, whether financial or through developer time, helps us deliver better security for everyone.

## Looking Ahead

The CRS 4 LTS release in Q1 2026 will represent a major milestone for organizations planning their migration from CRS 3.3. It signals that CRS 4 has reached the stability and maturity needed for production deployments requiring long-term support.

We encourage organizations currently running CRS 3.3 to begin planning their migration. With Q3 2026 marking the end of CRS 3.3 support, and Q1 2026 bringing the first CRS 4 LTS, the migration window is clear. 

We'll be sharing more details about the CRS 4 LTS release as we approach Q1 2026, including specific version numbers, migration guides, and technical details about the LTS support model.

The CRS project has always been driven by community commitment and the shared goal of making the web more secure. Our decision to proceed with LTS despite sponsorship challenges reflects these core values. We're here for the long term, supporting the security community that depends on us.

## Get Involved

If your organization benefits from CRS and wants to support the LTS effort, please reach out: **sponsoring@coreruleset.org**

### Individual Users Can Make a Difference

Even if you're not in a position to make organizational decisions, you can still help. If you're an end user whose infrastructure depends on CRS — whether through cloud providers, managed security services, CDN providers, or other platforms — reach out to them. Ask them to contribute to or get involved with the CRS project. Many providers benefit enormously from CRS but may not realize their users value and depend on this contribution to the open source security ecosystem.

Your voice matters. When providers hear from their customers that CRS support is important, it strengthens the case for their involvement. We're also working with OWASP Headquarters to establish additional donation pathways throughout 2026, making it easier for organizations of all sizes to support this critical infrastructure.

For questions about CRS 4, migration planning, or general support, connect with us through our usual channels.

Together, we're building a more secure web—one rule at a time.
