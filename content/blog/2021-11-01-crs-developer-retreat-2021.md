---
author: dune73
categories:
  - Blog
date: '2021-11-01T11:42:19+01:00'
title: CRS Developer Retreat 2021
url: /2021/11/01/crs-developer-retreat-2021/
---


The OWASP ModSecurity Core Rule Set team met for a one week developer retreat in the Swiss mountains to hack away at CRS together. We worked on several larger projects and ran seven additional workshops, all documented on our [GitHub wiki](https://github.com/coreruleset/coreruleset/wiki).

Why Switzerland? Switzerland is an expensive place, but most of our active developers live in Europe and then Switzerland becomes central. And we found the [Hacking Villa](https://ungleich.ch/u/projects/hacking-villa/) ran by local [ISP Ungleich](https://ungleich.ch). Villa is a funny description, since it's more like a very old alpine hostel equipped with the latest IPv6. But the main reason we settled on this offering was the great price that hotels in European cities could not compete with (and then of course the 10Gb/s fiber!) If you are looking for a cheap, no-bullshit offering to host a camp, then look into the Hacking Villa.

But whatever, let's look at the projects, workshops and some of the fun activities we did to entertain us for a week.

{{< figure src="images/2021/11/CRS-Summit-Group-Photo-2021-cutout-1024x979.jpg" caption="The CRS Team on site from left to right: Felipe Zipitría (@fzipi), Christian Folini (@dune73), Franziska Bühler (@franbuehler), Ervin Hegedüs (@airween), Max Leske (@theseion), Christoph Hansen (@emphazer), Andrea Menin (@theMiddle), Walter Hop (@lifeforms), guest Juan Pablo Tosso, Andrew Howe (@redXanadu), Paul Beckett (@53cur3M3)" >}}
#### Project: The Sandbox / Demo Site

We have built a demo site that allows everybody to try out CRS via an API. Various backend engines and all currently supported CRS versions are accessible. We are not fully ready to publish the service, but it's only a couple of weeks away. When it becomes public, researchers will be able to check their exploits against CRS. That means if you have a successful exploit against a service or application, you can test whether CRS would block it, and get the score and rules back.

In the past, we had researchers adding a paragraph to their publications that details if and how CRS is detecting an attack, which CRS rules are involved etc. Ideally, more people will add these sections to their publications, since the demo site makes CRS much more easy to test now. And of course it also becomes easier for people to assess whether they would profit from CRS for their local application by using the sandbox.

#### Project: The Status Page

With the strong focus on the demo page / sandbox, this one got less attention. But we sat together for a long time to think about a status page idea, since we think it will complement the demo in a perfect way. It is basically a live view how different integrations of CRS are stacked against each other and against the native CRS. It's a description of which CRS key features the integrations support, but also how many of our integration tests they pass. We know it's 100% for ModSecurity 2.9.x on Apache (our reference implementation) and 97% for ModSecurity 3.0.x on NGINX. But how much is it for SaaS CRS offerings like Google Cloud Armor, Azure and Cloudflare? Well, the plan is to make this transparent. As a sub-project, we have started expanding our integration tests: within a few weeks we aim to have 100% test coverage for all CRS detection rules.

#### Project: Documentation

We knew for quite some time that the official CRS documentation on the website sucks. The documentation within crs-setup.conf is really good, but you kind of need to know, as it's not the obvious location. During our stay, we have therefore relaunched the documentation completely via a new separate [documentation project on GitHub](https://github.com/coreruleset/documentation) and automatic deployment onto our [website under /docs](https://coreruleset.org/docs/). The old documentation has been migrated, and we started to replace it with more modern takes on the the different topics and also with completely new sections. Much more content is planned to be finalized in the near future.

#### Project: Technical Blog Posts

Technical blog posts are close to documentation, but not quite. We identified about twenty topics that should (or at least could) be covered in a blog post. One of these topics is the practical use of Paranoia Levels. I wanted to write this blog post for a long time, and staying with the other CRS developers inspired me enough to actually do it. [The blog post](https://coreruleset.org/20211028/working-with-paranoia-levels/) covers the idea and concept behind Paranoia Levels, how you pick the right Paranoia Level for your service, what it means in terms of false positives (-&gt; Higher Paranoia Level means more false alarms) and how you talk to management about this topic. And then of course the practical question of going from a low Paranoia Level to a higher one, while maintaining your blocking configuration and without locking users out because of new false positives.

#### Workshop: Rule Documentation

We want to formalize the documentation of our rules. This information is quite chaotic so far, and the quality is very heterogeneous. We want to standardize it in a YAML format so integrators can enrich their GUIs with rule documentation, and we can also display a clear and documented rule list on our website. During the week, we settled on the format, but did not take it from there. So don't hold your breath, but we have a very clear idea of how we want to go about this.

#### Workshop: How to Avoid CVEs

As you probably know, we suffered from a rule set bypass that resulted in a CRITICAL CVE ([CVE-2021-35368](https://coreruleset.org/20210630/cve-2021-35368-crs-request-body-bypass/)). During the retreat, we talked about this for a long time, since we really want to avoid this for the future. We're only an open source project, but we have hundreds of thousands of users and most big cloud providers have a CRS offering these days, so the question is essential: What can we as a project do to avoid merging such a devastating bug in the future?

#### Workshop: Request Smuggling and Server Side Request Forgery

These old exploitation techniques have made a big impact in the last 2-3 years, and we are aware that CRS is not providing enough protection. Unfortunately, the ModSecurity engine is limiting our abilities, and the way webservers have implemented HTTP 2.0 is also impacting us negatively. Therefore, we can not really cover everything. But in this workshop we investigated the various ways how we can improve our rule set, and we already have a pull request with a [new generic rule defending against SSRF](https://github.com/coreruleset/coreruleset/pull/2259).

#### Workshop: Recommended Rules

The *recommended rules* is a set of rules that the ModSecurity developers recommend when running ModSecurity. These rules interact with CRS and CRS interacts with them. We reviewed this interaction in light of recent discussions where we asked the ModSecurity developers to update their rules. The resulting update is not adequate from our perspective, so we agreed to take the next step. The next step will mean people keep the recommended ModSecurity rule file, but we will replace individual recommended rules with our own rules. That means CRS will start to overrule ModSecurity's recommendations where we see fit. Expect this for the next major release.

#### Fun Activities

It was clear from the beginning, we could not work for seven days without any breaks. So we planned for some activities outside our hostel. The proposal to visit a water fun park was quickly dismissed, so we settled on the local museum dedicated to the life and death of [Anna Göldi](https://www.annagoeldimuseum.ch) - in collaboration with Amnesty International. One night, we went to a local restaurant eating cheese fondue until we could not take any more (an essential experience when visiting Switzerland). But the highlight was a visit to [Mr. Greisinger's Tolkien Museum](https://greisinger.museum). It's built into a hill like a hobbit hole and Mr. Greisinger leads the guided tours himself. He is a somewhat over-enthusiastic collector and holds the biggest collection of memorabilia of Tolkien (-&gt; e.g. the only Spanish edition of the Hobbit with a dedication by Tolkien himself) in the world. We found it an impressive experience in every dimension. There are a ton of reviews on Tripadvisor and they are all true. Be sure to read them before you visit the museum...

{{< figure src="images/2021/11/Greisinger-Museum-1024x768.jpeg" caption="CRS entering the depths of the Tolkien Museum" >}}
If we take the time spent on fun activities out, I think we still spent about 60 working days on the project. And that's a great push for our team that will carry us very far.

Words fail to describe the experience of meeting the entire team for a week. We all work with ModSecurity and the Core Rule Set, most of us on a daily basis. But each and every one of us is a lone wolf at home. People ask for our support with their problems and we get very few people to discuss CRS on eye level. And then you meet 10 likeminded people for a whole week and it's like your mind is overflowing. We'll be back, that's for sure!
