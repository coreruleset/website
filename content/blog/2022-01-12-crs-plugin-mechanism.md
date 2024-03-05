---
author: dune73
categories:
  - Blog
date: '2022-01-12T09:32:49+01:00'
permalink: /20220112/crs-plugin-mechanism/
tags:
  - ModSecurity
  - Plugins
title: The CRS Plugin Mechanism
url: /2022/01/12/crs-plugin-mechanism/
---


***Plugins are not part of the CRS 3.3.x release line. They will be released officially with the next major CRS release 4.x. In the meantime, you can use them with one of the stable releases by following the instructions below.***

#### What are Plugins?

Plugins are sets of additional rules that you can plug in to your web application firewall in order to expand CRS with complementary functionality or to interact with CRS. Rule exclusion plugins are a special case: these are plugins that disable certain rules to integrate CRS into a context that is otherwise likely to trigger certain false alarms.

#### Why do we Need Plugins?

Installing only a minimal set of rules is desirable from a security perspective. A term often used is "minimizing the attack window". For CRS, this means that by having fewer rules, it is less likely to deploy a bug. In fact, CRS had a major bug in one of the rule exclusion packages which affected every standard CRS installation (see [CVE-2021-41773](https://coreruleset.org/20210630/cve-2021-35368-crs-request-body-bypass/)). By moving all rule exclusion packages into optional plugins, we will reduce the risk in this regard. So security is a prime driver for the introduction of plugins.

A second driver is the need for certain functionality that we do not want to have in mainline CRS releases. Typical candidates include the following:

- ModSecurity features that we deem too exotic for mainline, like the use of Lua scripting
- New rules that we do not yet trust enough to integrate into the mainline
- Specialized functionality with a very limited audience

A plugin might also evolve quicker than the slow release cycle of stable CRS releases. That way, a new and perhaps experimental plugin can be updated quickly.

Finally, we want to allow you and other third parties to write plugins that interact with CRS. Until now, this has been very difficult to manage, but with plugins everybody gets the red carpet rolled out in order to allow them to write anomaly scoring rules.

#### How do Plugins Work Conceptually?

Plugins are a set of rules. These rules can run in any phase, but in practice we expect most of them to run in phase 1 and, especially, in phase 2, just like the rules in CRS. The rules of a plugin are separated into a rule file that is loaded *before* the CRS rules are loaded and a rule file with rules to be executed *after* the CRS rules are executed.

Optionally, a plugin can also have a separate configuration file with rules that configure the plugin, just like the crs-setup.conf configuration file.

The order of execution is thus:

- CRS configuration
- Plugin configuration
- Plugin rules before CRS rules
- CRS rules
- Plugin rules after CRS rules

This can be mapped almost 1:1 to the *Includes* involved:

```
Include crs/crs-setup.conf
 
Include crs/plugins/*-config.conf
Include crs/plugins/*-before.conf
 
Include crs/rules/*.conf
 
Include crs/plugins/*-after.conf
```

As you can see, the two existing CRS `Include` statements are complemented with three additional generic plugin *Includes*. This means CRS is configured first, then the plugins are configured (if any), then the first batch of plugin rules are executed, followed by the main CRS rules, and finally the second batch of plugin rules run, after CRS.

#### How to Install a Plugin

Let's prepare the plugin folder first.

Future CRS releases will come with a plugins folder next to the rules folder. If you do not have that yet then create it and place three empty config files in it (Shell command `touch` is your friend):

```
crs/plugins/empty-config.conf
crs/plugins/empty-before.conf
crs/plugins/empty-after.conf
```

These empty rule files make sure that the web server does not fail when including `*.conf` if there are no plugins present. (We're aware that Apache supports the `IncludeOptional` directive, but that is not available on all web servers, so we prefer to use `Include` for documentation purposes.)

For the installation, there are two methods:

##### Method 1: Copying the plugin files

This is the simple way. You download or copy the plugin files, likely rules and data files, and put them in the plugins folder of your CRS installation, as prepared above.

There is a chance that a plugin configuration file comes with a `.example` suffix in the filename, just like the `crs-setup.conf.example` configuration file in the CRS release. If that's the case then rename the plugin configuration file by removing the suffix.

Be sure to look at the configuration file and see if there is anything you need to configure.

Finally, reload your WAF and the plugin should be active.

##### Method 2: Placing symlinks to your separate plugin files downloaded elsewhere

This is the more advanced setup and the one that is in sync with many Linux distributions.

With this approach, you download the plugin to a separate location and put a symlink to each individual file in the plugins folder. If the plugin's configuration file comes with a `.example` suffix then you need to rename that file first.

With this approach it is easier to upgrade and downgrade a plugin by simply changing the symlink to point to a different version of the plugin. You can also `git checkout` the plugin and pull the latest version when there is an update. It is not possible to do this in the plugins folder itself, namely when you want to install multiple plugins side by side.

This symlink setup also allows you to `git clone` the latest version of a plugin and therefore update without further ado (pay attention to updates in the config file, though!).

If you update plugins this way, there is a certain chance that you don't get a new variable that is being defined in the latest version's config file of the plugin. If you as a plugin author want to make sure, this is not happening to your users, then add a rule that checks for the existence of all config variables in your *Before-File*. Look at the examples in CRS `REQUEST-901-INITIALIZATION.conf`.

#### How to Disable a Plugin

Disabling a plugin is really simple. You can simply remove the plugin files in the plugins folder, or the symlinks to the real files if you used the symlink method. It is probably a cleaner approach to work with symlinks since the plugin files remain available to re-enable in the future.

Alternatively, you could also rename a plugin file from `plugin-before.conf` to `plugin-before.conf.disabled`.

#### What Plugins are Available?

As of this writing, there are several plugins available. They are all listed on GitHub in the CRS plugin registry repository: <https://github.com/coreruleset/plugin-registry>

- Dummy Plugin: This is the example plugin to get you started
- Auto-Decoding Plugin: This uses ModSecurity transformations to decode encoded payloads before applying CRS rules at PL3 and double-decode payloads at PL4.
- Antivirus Plugin: This helps you to integrate an antivirus scanner into CRS
- Body-Decompress Plugin: This decompresses/unzips the response body for inspection by CRS
- Incubator Plugin: This plugin allows us to test non-scoring rules in production before pushing them into the mainline

More plugins are in the making, like the aforementioned shift of all rule exclusion packages into rule exclusion plugins that will happen before the next major release.

#### How to Write Your Own Plugin

Before we discuss the creation of your own plugins, let's first look at the question of whether a plugin is the right approach for your rule problem.

CRS is a generic rule set. We do not really know your setup, so we write our rules with caution and we allow you to steer the behavior of CRS by setting the anomaly threshold accordingly. When you write your own rules, you know a lot more about your setup and there is probably no need to be as cautious. It's probably futile to write anomaly scoring rules in your situation. Why bother with anomaly scoring when you know that everybody issuing a request to `/no-access` is an attacker?

In such a situation, it is better to write a simple deny-rule that blocks said requests. There's no need for a plugin in most situations. However, when you really *do* have a use case for a plugin, I suggest you start with a clone of the dummy plugin. It is well documented and a good place to start from.

Plugins are a new idea for CRS as well, so we do not really have strict rules about what a plugin is and isn't allowed to do. There are definitely fewer rules and restrictions for writing plugin rules than for writing a mainline CRS rule, where we are becoming stricter and stricter as the project evolves. This means that you can basically do anything, especially if you are not planning to contribute your plugin to the CRS project. If you *do* plan to contribute back, here is some guidance to help:

- Try to keep plugins separate. Try not to interfere with other plugins and make sure that any other plugin can run next to yours.
- Be careful when you interfere with CRS. You can disrupt CRS easily by excluding essential rules or by messing with variables.
- Keep an eye on performance and think of use cases.

##### Anomaly Scoring: Get the Phases Right 

The anomaly scores are only initialized in the CRS rules file `REQUEST-901-INITIALIZATION.conf`. This happens in phase 1, but it still happens after your plugin's `*-before.conf` file has been executed for phase 1. So if you set anomaly scores there, it will be overwritten in CRS phase 1.  
The effect for phase 2 anomaly scoring in the plugin's `*-after.conf` file is similar. It happens after the CRS request blocking happens in phase 2. This can mean you raise the anomaly score after the blocking decision. You might end up with a higher anomaly score in your log file and you will wonder why the request has not been blocked.

Here is what do do:

- Scoring in phase 1: Put in the plugin's *After-File* (and be aware that *early blocking* won't work)
- Scoring in phase 2: Put in the plugin's *Before-File*

#### Quality Guarantee

We separate the official CRS plugins from third party plugins. The idea is to keep the official plugins on par with the quality of the CRS project. We cannot guarantee the quality of third party plugins because we do not control their code repositories, so once third party plugins start to appear, you will have to look at them separately and decide whether their quality is good enough for your production site.

#### How to Integrate Your Plugin into the Official Registry

Please polish your plugin until you think it is ready. Then open a pull request at the plugin registry. Feel free to use any free rule ID range for your new plugin. We will then review the plugin and assign you a block of rule IDs for your plugin. Afterwards, your plugin will be listed as a new third party plugin.

Christian Folini, CRS Co-Lead
