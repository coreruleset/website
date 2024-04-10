---
author: dune73
categories:
  - Blog
date: '2021-05-19T09:24:47+02:00'
tags:
  - AI
  - machinelearning
  - ML
title: A new attempt to combine the CRS with machine learning
---

*The following is a contributing blog post by Floriane Gilliéron. You can reach Floriane via firstname dot lastname at gmail.com.*

My Master Thesis from [EPFL](https://www.epfl.ch) tackled the challenge of using machine learning to improve the performance of a ModSecurity web application firewall, used with the [OWASP Core Rule Set](https://coreruleset.org). The initiators of the project were concerned about the high number of false alerts (around 90 per day) issued by their WAF, which from a business point of view did not allow the use of blocking mode. The project was also motivated by the fact that it’s now a common thing to rely on machine learning in web application security, like big WAF vendors such as F5 or Fortinet do.

The idea was therefore to add machine learning as a second layer of detection after the CRS, to check the requests flagged by the CRS and only block those that are classified as an attack by both the CRS and machine learning. Another important design choice was to add ML inside ModSecurity to benefit from its parsing and logging capabilities. This architecture allows for easier access to the results of the CRS evaluation of the request. It also makes it cleaner to remove machine learning from the request processing pipeline.

### Adding ML to ModSecurity

To add machine learning to ModSecurity, the approach taken was to run the machine learning model as a server in another container/pod. This obviously adds latency due to communication overhead but has the advantage of only loading and instantiating the ML model once at server start and not for each incoming request. This can be significant in the event that complex deep learning models are used.

Machine learning was integrated in the request processing flow by modifying rule 949110 (the one comparing the inbound anomaly score to the desired threshold), chaining it to a “SecRuleScript'' executing a Lua script. When the Lua script is triggered, the following actions are performed:

1. The Lua script first retrieves the useful information about the request being processed using the ModSecurity variables, creates a POST request containing these pieces of information in the body and sends it to the ML server.
2. The ML server retrieves the information in the body, creates the features and passes them to the pre-trained ML model. The binary decision outputted by the model is then returned to the Lua script using the status code of the HTTP Response: 200 for normal requests and 401 for attacks.
3. The Lua script then forwards this decision to the request processing flow by returning either *nil* or an error message.

The chaining of the ML rule (i.e “SecRuleScript”) to the one originally present in rule 949110 (i.e. “SecRule”) ensures that only requests that exceed the inbound anomaly score trigger the ML server, and that only requests that are classified as an attack by both rules trigger the “deny” action.

This project was obviously not the first one aiming at combining ModSecurity and machine learning. The work of Rodrigo Martinez and Juan Diego Campo [cited during the first CRS Community Summit in London](https://coreruleset.org/20180712/reporting-from-the-first-crs-community-summit-in-london/) in 2018 was very helpful for writing the Lua script, especially in understanding how to retrieve the ModSecurity variables. Their repo can be found at <https://gitlab.fing.edu.uy/gsi/modsec-ml/-/tree/master>.

```
SecRule TX:ANOMALY_SCORE "@ge %{tx.inbound_anomaly_score_threshold}" \`  
 "id:949110,\  
 phase:2,\  
 deny,\  
 t:none,\  
 msg:'Inbound Anomaly Score Exceeded (Total Score: %{TX.ANOMALY\_SCORE})',\  
 tag:'application-multi',\  
 tag:'language-multi',\  
 tag:'platform-multi',\  
 tag:'attack-generic',\  
 ver:'OWASP\_CRS/3.3.0',\  
 severity:'CRITICAL',\  
 setvar:'tx.inbound\_anomaly\_score=%{tx.anomaly\_score}', \  
 chain"  
 SecRuleScript /path/to/script.lua
```

### The ML methodology

#### Type of ML model

In such a problem, relying on the classical “cat/dog” classification techniques is definitely not the best option, for two reasons. First, examples of attacks are (hopefully!) much rarer than examples of normal traffic, which makes the dataset unsuitable for supervised classification algorithms. Secondly, as attacks are constantly evolving, learning what attacks look like based on past traffic is inefficient against new attacks. It makes more sense to define what normal traffic looks like, and to block anything that doesn't resemble the learned behavior.

Considering this, the type of machine learning techniques to use for this problem is anomaly detection. Anomaly detection techniques work by first learning what the normal class looks like based on normal examples. Once trained, the model can give a normality score to never-seen samples. By applying a threshold on this normality score, a binary classification decision normal/attack can be obtained. For instance, with a threshold of 0.5, a normality score of 0.1 will indicate an attack while a normality score of 0.8 will indicate a normal sample. Both normal and attack samples are used to tune the threshold and to evaluate the model.

The ML model chosen for this project was the Isolation Forest, which had better and more stable performances than the other tested ones, among which the One Class SVM. It works by randomly building multiple decision trees and is well suited for mixed types of data (continuous/discrete/boolean).

### Data collection and processing

The ML model was trained using real-world traffic recorded on the production environment of a web application over a period of two weeks. As the WAF was set in non-blocking mode, only warnings were issued by the CRS. These warnings were manually sorted between actual attacks and false alerts. Most of the false alerts came from encrypted/encoded payloads such as SAML that triggered pattern match rules. The normal examples used to train the anomaly detection ML model were thus made of requests that didn’t result in a warning from the CRS and of warnings that were actually false alerts.

Data had to be transformed to be used by the Isolation Forest model. To this end, 26 numerical features were extracted such as the hour of the day, the length of the path/arguments, the percentage of uppercase/digits/special characters in the arguments, the entropy, the presence of keywords often used for injections.

### Results

Unfortunately, the ML model developed for this project was not able to do better than the classical way of dealing with false alerts when using the CRS: rule exclusion/tuning. By disabling just one of the rules, 95% of the false alerts that worried so much the initiators of the project could be removed. While ML was also able to correctly detect these false alerts, it was not able to detect the remaining 5%. Furthermore, ML missed many attacks, around a third of those present in the evaluation set, while the rule disabling did not reduce the number of detected attacks in the evaluation set. Further considering the time and efforts needed to build, deploy and maintain a machine learning model, this leaves no argument in favor of ML.

### Conclusion

The mitigated results of machine learning in reducing the false alerts of the CRS could be explained by the simplicity of the model used. Using only 26 numerical features may not allow to characterize a request well enough to grasp the difference between a normal request and an attack. Using deep learning methods such as an auto-encoder, that can take as input the whole request, could be an option to explore. Nevertheless, one should keep in mind that machine learning (even if it’s trendy) is not always the answer, and that simpler solutions such as rule exclusion/tuning can also get the job done.

The final words of the project were that machine learning should be used to detect new, more complex attacks missed by the CRS instead of reducing the false alerts, which can successfully be done by rule exclusion/tuning. An example of complex attacks could be the ones consisting of more than one request. Indeed, so far, attacks were defined by considering and classifying only a single request. However, some attacks can take the form of a sequence of normal-looking requests, which together form an attack. Thus, it could be interesting to work with sequential anomaly detection ML models.

The proposed architecture to add machine learning to ModSecurity may not be the fastest one but offers flexibility and ease. It was conceived with the idea of one day being able to build an automated pipeline for machine learning with performance monitoring, new data collection and re-training. Having a separate environment for ML makes these tasks easier. An idea to decrease the latency induced by the ML part could be to call it at the beginning of phase 2, so that it runs simultaneously with the rules evaluation. But that is a mission for the next person who will be up for the challenge of combining ML and CRS!

*The work presented by Floriane above is now being made into a [ML plugin for CRS](https://github.com/coreruleset/coreruleset/pull/2067). This will settle the ML integration into CRS and allow future work to concentrate on the ML part.*
