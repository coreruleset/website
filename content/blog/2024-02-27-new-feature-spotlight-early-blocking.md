---
title: 'New feature spotlight: Early Blocking'
date: '2024-02-27T09:00:00+01:00'
author: dune73
url: /2024/02/27/new-feature-spotlight-early-blocking/
categories:
    - Blog
tags:
    - CRS4
---

One of the new features added in CRS 4 is *Early Blocking*. This optional new setting allows blocking decisions to be made earlier than usual.

#### How it works

CRS request detection rules take place in two phases. The rules of the **first phase** are executed after the server has received the HTTP *request line* and the *request headers*. The rules of the **second phase** are executed once the *request body* has been received and parsed.

The new *Early Blocking* feature introduced with CRS 4 means that the anomaly score of a request is checked at the end of phase 1. If a request has *already reached the score threshold* by this point then the server will block it without ever executing phase 2. (Previously, the first anomaly score check only took place at the end of *phase 2*.)

You can control this early blocking behavior by setting the `tx.early_blocking` variable in crs-setup.conf. By default, early blocking is disabled. Uncomment rule 900120 in the setup file to enable early blocking mode.

Early blocking is also implemented for *responses*, but it has less of an effect there, admittedly.

{{< figure src="images/2024/02/pexels-rdne-stock-project-7755146.png" caption="© RDNE Stock project (pexels.com)" >}}

#### The performance

You would think that CRS has implemented this new feature for performance reasons, but that's actually not the case. Let me show you why.

Let's assume you have 95 % benign traffic and 5 % attack traffic. The benign traffic will always run through *all* the CRS rules, whether early blocking is enabled or not. It is only the attack traffic that gets blocked earlier if it violates one or more of the phase 1 rules, depending on the anomaly threshold.

What early blocking does is it speeds up the response for some of the attackers. If we assume that the server identifies 50% of the attacks during the first phase (the header phase) then we save the CPU time used to execute the body rules for half of the attack traffic. That's half of 5% of traffic, and in most cases that isn't much, honestly.

#### Alert fatigue

The real benefit of early blocking is its affect on *alert fatigue*. Alert fatigue describes the avalanche of alerts that fill your logs when operating CRS and how you cannot cope with the sheer mass of messages.

Let's assume you've tuned down your service to have very few false positives. What you see now is still a lot of alerts because of all the attacks taking place. And you *do* kind of need to look through them, or at least do proper reporting, because there might still be false positives hiding in the logs. That's a lot of work and it's day to day pain.

With early blocking there are far fewer alerts. It's like you carry out an inspection and you stop in the middle because you've already made up your mind. Why carry on and do more paperwork when you already know that you're going to block this request?

The result is less noise in the logs, less noise in the dashboard, less noise in the reporting. Additional alerts for the same attacks would be redundant, anyways.

So alert fatigue is reduced by early blocking. You get the minimum needed to identify the attackers and that's it.

#### Beware of hidden false positives in certain cases

It's important to be aware of an operational issue that comes with early blocking in some cases. Imagine a false positive that blocks a benign, genuine user in phase 1. You get a call, you tune away the false positive, and you ask the user to try again. If early blocking is in use, there is a chance that a new, *phase 2* false positive will now pop up: a false positive that was not visible before because you only ran the phase 1 rules and blocked them immediately.

So if a user is blocked in phase 1 and you solve *that* problem, you need to bear in mind that there's a non-zero chance of an identical request being blocked in phase 2.

#### Less pain with a minor caveat

The new *Early Blocking* feature adds another tool to the CRS toolbox. It's an interesting new option that can reduce the day to day burden of alert fatigue on CRS operators. It can also potentially save a few CPU cycles.

Early blocking comes with the caveat of potentially hiding false positives in some situations, but you may find that easing the pain of alert fatigue is worth a little extra work to squash false positives every now and then.