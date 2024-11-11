---
author: dune73
categories:
  - Blog
date: '2024-11-06T10:52:50+01:00'
title: Securing the Maintenance of a CRS 4 LTS release
slug: 'securing-the-maintenance-of-a-crs-4-lts-release'
---


OWASP CRS is a cornerstone in the cybersecurity landscape, providing essential protection against web application attacks. With the release of CRS 4 earlier this year, the project has reached new heights in terms of rules and functionality. As the project continues to evolve, the need for long-term support (LTS) becomes crucial to ensure its sustainability and effectiveness. Many organizations are planning a migration of their extensive CRS 3.3 setups to the stronger CRS 4, but they are waiting for an LTS release as a signal that CRS 4 has reached the stability they are seeking for their installation. In this blog post, we explore the significance of CRS 4 LTS and the call for sponsorship to support this essential initiative.

## CRS 4: A Milestone in Web Application Security

CRS 4 has been a game-changer since its release, offering enhanced rules and a new plugin functionality that facilitates integrations and extensions to the rule set. The stability of the new rules has been proven and the optimized CI/CD pipeline has stabilized in recent months. Several big players are betting on CRS and new ones are joining.

## The Importance of Long-Term Support (LTS)

Long-term support ensures that critical security updates and bug fixes are provided for an extended period. This will guarantee the longevity and reliability of the project. For the CRS project, LTS will enable users to continue benefiting from the advanced protections offered by CRS 4, without the risk of our fast development cycle forcing them into costly updates with the extensive testing that is needed.

## The Costs of Doing an LTS

Maintaining a Long-Term Support (LTS) version of a software project like OWASP CRS comes with its costs, namely the time-consuming process of backporting critical changes, updating and maintaining testing infrastructure to ensure the stability of the LTS version, and configuring the CI/CD pipeline to automate the testing and deployment processes. We overhauled the CI/CD completely between CRS 3 and CRS 4 and we also changed the format of the test files. Our roadmap sees more changes in this regard, but new releases in a CRS 4 LTS release line would demand that the currently existing CI/CD pipeline is maintained in parallel. And there is another significant challenge that arises: the potential drain on developer mindshare, as resources are diverted from working on new features or improvements to focus on LTS maintenance. This would impact overall productivity and innovation within the team - the reason we have been postponing a CRS 4 LTS so far.

## The Dev-On-Duty Program: A Model to Follow

With the [Dev-on-Duty program]({{< ref "blog/2021-04-14-introducing-the-dev-on-duty-program.md" >}}), we guarantee responses for support questions around CRS via multiple channels. We can guarantee this, because we are paying CRS developers a weekly fee to cover this service. And the fee is paid out of the funds that our existing sponsors contribute to CRS. This benefits the community and the project in an extraordinary way: the community can seek assistance on the preferred channel, GitHub issues are addressed and cleaned away, the development of the project is not dragged down by the influx of support calls, the developers stay in touch with the problems of ordinary users, and the developers in the Dev-on-Duty program earn a bit of money on the side and the sponsors are contributing substantially to the well-being of the project.

We are now seeking a similar model for the maintenance of an LTS release: we want to bring an LTS to our users without dragging down overall development.

## Call for Sponsorship: Ensuring the Future of CRS 4 LTS

To support the CRS 4 LTS initiative, the project is calling for sponsorship from organizations that value web application security and are committed to ensuring the sustainability of open-source projects as part of their supply chain. The sponsorship can take two forms: collaborating with the project team to provide long-term maintenance of the release line directly. That means a commercial partner takes over the maintenance of the LTS on our behalf by becoming the sponsor providing the LTS releases based on a long term agreement. Or one or multiple sponsors help us finance the LTS and we commission the maintenance of the release line from a company within the CRS developer community, thus indirect support via financial means.

Both forms, the direct and the indirect support, are equally interesting for us.

If you think you want to be that LTS sponsor or if you want to contribute to LTS as a sponsor, then please get in touch:  *felipe \[dot\] zipitria \[at\] owasp \[dot\] org*