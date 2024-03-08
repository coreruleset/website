---
author: amonachesi
categories:
  - Blog
date: '2022-12-01T08:13:00+01:00'
permalink: /20221201/the-crs-developer-retreat-2022/
title: The CRS Developer Retreat 2022
url: /2022/12/01/the-crs-developer-retreat-2022/
---


Pizza, pasta, pesto ... pineapple? This was one of the many important topics (and one of the most controversial) discussed at the [CRS developer retreat 2022](https://github.com/coreruleset/coreruleset/wiki/Dev-Retreat-2022) in Italy. The annual CRS developer team retreat is always a highlight of the year, finally meeting face-to-face again and not just via chat.

This time, the backdrop for the meeting from October 29 to November 5 was the southern foothills of the Alps near Lake Varese, close to the Swiss border. Here, in [Villa Cagnola](https://villacagnola.com), there was not only good food and drink – there was also [a lot of work](https://github.com/coreruleset/coreruleset/wiki/Dev-Retreat-2022-Topics). The focus was on two items: preparing the rule set for the CRS v4 release and defining a strategy for the future of the project.

{{< figure src="images/2022/11/Developer_Retreat_2022_Garden-1024x594.jpeg" caption="The CRS core team is meeting in the garden of Villa Cagnola for the roadmap discussion" >}}
#### Working Off All Bug Bounty Findings

A private bug bounty in Spring had delayed the preparation for the CRS v4 release and we were still trying to get over that hill. The policy clearly is that we will not release v4 without being sure we closed the 150 or bug bounty findings that had been reported to us. Additionally, there was also a separate submission with several dozens of SQLi bypasses that [will have to be fixed as well](https://github.com/coreruleset/coreruleset/issues?q=Shivam+is%3Aissue+author%3Afranbuehler+label%3Asqli-bypass-bathla). We started the week with 38 open issues and finished with a single tricky finding we had not solved. So this was highly successful, [but still not quite done](https://github.com/coreruleset/coreruleset/wiki/DevRetreat22ProjectBugBounty).

#### The Future of ModSecurity and Coraza

For the big [roadmap discussion](https://github.com/coreruleset/coreruleset/wiki/DevRetreat22WorkshopRoadmap) the developer team and two guests met on Monday morning in the spacious garden of the villa. Between hedges, flowerbeds and statues, we discussed how to proceed with the project. The uncertain future of ModSecurity after the official EOL also came up. CRS is still unwilling to fork ModSecurity, but we are confident somebody will keep the ModSecurity project running after EOL.

Due to the uncertainty of ModSecurity, the Coraza WAF is becoming more and more important for the CRS. Coraza is now also an OWASP project and is currently being ported to NGINX. However, it will be some time before it can be used in production. The CRS project is considering supporting the work on the NGINX port to help it being stabilized. If this approach proves to be successful, the same would be considered for a future port to Apache.

In contrast to this, the project as a whole will not commit to help with libinjection. Libinjection is considered a major pain point, but CRS can not really agree what to do with the library to ease the situation and we are rather staying absent than tear our project apart over this question.

{{< figure src="images/2022/11/Developer_Retreat_2022_Milano-1024x576.jpg" caption="Peak performance: On the roof of Milan's cathedral" >}}
#### Organizing the CRS Project

Another central point of discussion concerned organization of the project. In recent years, the project has grown enormously and beyond just the ruleset. It was therefore necessary to discuss how to deal with the resulting increase in complexity.

For the future organization of the CRS project with all its different areas and subprojects, the core team members argued against the creation of a hierarchically structured organization of overall lead, subproject lead, and developer. Instead, the subprojects should organize themselves without formal leaders. This is to ensure cohesion within the larger CRS project and the identification of team members with the goals of the overarching CRS. This reorganization will have an impact on the monthly meeting: Subprojects will provide a brief statement on their current status, which will be reflected in the agenda for all to see, but it will not be discussed in the meeting itself. CRS rules and discussions about pull requests will also be given less space in the future. What is not urgent will be discussed outside the general meeting.

The workshop identified the following subprojects. Which team members are involved in which projects can be found [in the wiki](https://github.com/coreruleset/coreruleset/wiki/DevRetreat22WorkshopRoadmap).

• Rules  
• Containers  
• CRS Bug Bounty and Security  
• CRS Sandbox  
• CRS Status Page  
• Documentation and Public Relations  
• Plugins  
• Project Administration and Sponsor relationships  
• Testing  
• Tools

{{< figure src="images/2022/11/Developer_Retreat_2022_Italians-768x1024.jpeg" caption="Can you spot the real Italians?" >}}
#### Other Projects: Keyword Lists, Status Page and Milan

Other projects of the retreat included an update of all keyword lists and tools in preparation for the 4.0 release, fixing bugs in Regexp-Assemble and [continuing work on the status page](https://github.com/coreruleset/coreruleset/wiki/DevRetreat22ProjectStatusPage) where we want to test CRS integrations like Azure, AWS or Cloudflare with our test suite.

With so much mental peak performance, relaxation was not to be neglected. This was ensured by an excursion to nearby Milan, where we were given a guided tour of the magnificent cathedral, including a climb to the rooftop. And afterwards, in the [second-best pizzeria](https://www.dazero.org) of the Lombard metropolis, we were finally able to enjoy a pizza as it should be – [without pineapple](https://www.youtube.com/watch?v=EDUy3Y_w9Tk).
