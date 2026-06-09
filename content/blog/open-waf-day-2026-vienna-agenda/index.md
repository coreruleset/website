---
author: fzipi
categories:
  - Blog
date: '2026-06-03T10:00:00+01:00'
title: 'Open WAF Day Vienna 2026 – Full Agenda Announced'
slug: 'open-waf-day-2026-vienna-agenda'
---

We are happy to share the full agenda for **Open WAF Day Vienna 2026**, taking place on **Wednesday, June 24, 2026** at the Austria Center in Vienna. Five talks, two connectors, one adaptive honeypot, and a day full of WAF discussions await you.

## Schedule

All times are local (CEST).

| Time | Speaker(s) | Title |
|------|------------|-------|
| 09:45 – 10:00 | — | Registration & Welcome |
| 10:00 – 10:45 | Matteo Pace | Embracing Envoy's Dynamic Modules: Meet the new Coraza connector |
| 10:45 – 11:00 | — | Coffee break |
| 11:00 – 11:45 | Ervin Hegedüs | WAF error log analysis at the highest level: ultra-fast filtering and multi-level aggregation with minimal resources |
| 11:45 – 12:45 | — | Lunch break |
| 12:45 – 13:30 | Juan Pablo Tosso | Coraza Center: bringing your WAF closer to GitOps |
| 13:30 – 13:45 | — | Coffee break |
| 13:45 – 14:30 | Lukas Funk | Ingress NGINX is retired – now what about my WAF rules?! |
| 14:30 – 14:45 | — | Coffee break |
| 14:45 – 15:30 | Adrian Winckles & Gautam Juvarajiya | CHAMELEON-REN: Instrumenting Adaptive Honeypots with CRS for Education-Sector Threat Intelligence |
| 15:30 – 16:00 | — | Closing & Networking |

## Talks

### Embracing Envoy's Dynamic Modules: Meet the new Coraza connector

**Matteo Pace**

A deep dive into the new Coraza connector built on Envoy's Dynamic Modules API — what it is, how it works, and what it means for teams running CRS on Envoy-based infrastructure.

---

### WAF error log analysis at the highest level: ultra-fast filtering and multi-level aggregation with minimal resources

**Ervin Hegedüs**

The biggest challenge when using a WAF is still knowing what is happening in the traffic passing through the firewall. Many have already built dashboards for analysing logs, but the universal "perfect" log analyzer remains a dream: every WAF administrator approaches the challenge differently, and the needs vary from application to application.

This talk presents a command-line solution that is fast — comparable to the runtime of collected and indexed databases — yet capable of arbitrary, even multi-level aggregation. The program, written in C, currently processes a row in 1 μs on average, regardless of what aggregation is extracted from the log. The tool is useful for quickly processing daily files or preparing indexes for larger databases.

---

### Coraza Center: bringing your WAF closer to GitOps

**Juan Pablo Tosso**

Details to be announced.

---

### Ingress NGINX is retired – now what about my WAF rules?!

**Lukas Funk** · Security Solution Architect, United Security Providers

With the retirement of Ingress NGINX, many teams face a double challenge: finding a new ingress controller, and preserving their hard-earned WAF rules built on OWASP ModSecurity and OWASP CRS. Lukas will walk through the available options and make the case for the best open-source alternative: Envoy Gateway combined with the OWASP Coraza WAF Envoy go-filter. He will show how to achieve the migration and share the techniques and tools that make day-two operations — tuning rules in production — manageable for a seasoned WAF operator.

*Lukas brings 10+ years of hands-on experience designing, integrating, and operating web application firewalls at scale. He specialises in OWASP-aligned controls, policy-as-code, and GitOps for Kubernetes.*

---

### CHAMELEON-REN: Instrumenting Adaptive Honeypots with CRS for Education-Sector Threat Intelligence

**Adrian Winckles & Gautam Juvarajiya**

The OWASP CRS is widely deployed as a defensive layer protecting web applications from known attack patterns — but what happens when CRS is turned outward, configured not to block, but to listen, log, and learn?

CHAMELEON-REN is an in-progress research project that investigates whether adaptive, stimulus-driven honeypots can generate higher-fidelity, education-specific attack intelligence and whether CRS, operating in a capture-first detection-only configuration, is the right instrument to collect it. CRS anomaly scoring and rule-match data are used to characterise and classify inbound interactions, distinguishing opportunistic scanning from targeted probing and mapping which rule groups are most frequently triggered against different simulated personas — virtual learning environments, student record systems, ERP and finance portals, and research data platforms.

The talk will share early architectural decisions, initial telemetry findings, and the practical realities of running CRS in a passive intelligence-collection role in cloud-hosted environments: stability, log volume management, and the limits of what CRS alone can tell us about attacker intent. Attendees will leave with a concrete perspective on using CRS beyond its defensive role and an invitation to contribute to an open discussion on sector-specific deployment scenarios and the role of WAF telemetry in broader threat intelligence workflows.

---

## Event Details

- **Date:** Wednesday, June 24, 2026
- **Time:** 09:45 – 16:00 (CEST)
- **Venue:** Austria Center · Bruno-Kreisky-Platz 1 · 1220 Wien · Austria
- **Cost:** Free

{{< button link="/register/open-waf-day-2026-vienna" text="Register now!" >}}

See you in Vienna!

Felipe Zipitría for the CRS team
