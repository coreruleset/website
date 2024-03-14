---
author: dune73
categories:
  - Blog
date: '2020-09-01T13:35:59+02:00'
title: Introducing msc_pyparser
url: /2020/09/01/introducing-msc_pyparser/
---


Let us present `msc_pyparser` to you. It is a python library that lets you manipulate ModSecurity rules configuration files.

ModSecurity has decent capabilities to manipulate rules at runtime, but `msc_parser` lets you manipulate the config files themselves. This is useful in many situations and the longer we use it, the more use cases pop up.

We will walk you through four example use cases in this blog post. This is enough to get you inspiration and help you get started.

What is the library and does it work?

[`msc_parser`](https://github.com/digitalwave/msc_pyparser/blob/master/README.md) has been written by CRS developer [Ervin Hegedüs](https://twitter.com/IamAirWeen) from Hungarian company [Digitalwave](https://www.digitalwave.hu/en/services/modsecurity). The core of the library is an import function that parses a rule set and transforms it into a custom YAML or JSON representation. If you are interested in the details, it's a python list containing dictionaries. You can manipulate this representation of the rule set and export it into the ModSecurity rule language again when you are done.

The neat thing: If you import a rule set and export it without further manipulation you end up with exactly the same rule set as before, byte by byte. This works, because Ervin did a very good job and paid attention to whitespace and everything.

One word of caution, the concept of `msc_parser` is generic, but it is not able to read / write all rule sets as of this writing. It works fine with CRS, but it chokes on the Atomicorp rules. Ervin is working on a fix on that front but don't hold your breath.

### Installation

The `msc_parser` github describes several installation options and dependencies (debian family: `python3-ply python3-yaml python3-ubjson`).

The systemwide pip option works as follows:

```sh
pip3 install msc-pyparser==0.3
```

This gives you the `msc_parser` library for use in python script in the version 0.3.

To get started it's useful to also grab crs\_read.py and crs\_write.py from the examples folder of the `msc_parser` github:

- [https://raw.githubusercontent.com/digitalwave/`msc_parser`/master/examples/crs\_read.py](https://raw.githubusercontent.com/digitalwave/msc_pyparser/master/examples/crs_read.py)
- [https://raw.githubusercontent.com/digitalwave/`msc_parser`/master/examples/crs\_write.py](https://raw.githubusercontent.com/digitalwave/msc_pyparser/master/examples/crs_write.py)

The prefix hints at CRS, but they are generic in the way they execute.

### How to import the rule set?

The rule set is of course imported with the help of a parser, the crs\_read.py we just grabbed wraps around that parser library. Let's download the CRS rule set from github and import it into the `msc_parser`.

Here is how:

```sh
$> git clone https://github.com/coreruleset/coreruleset.git
$> mkdir coreruleset/rules-yaml
$> crs_read.py coreruleset/rules coreruleset/rules-yaml 
Parsing CRS config: coreruleset/rules/REQUEST-901-INITIALIZATION.conf
Parsing CRS config: coreruleset/rules/REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.conf
Parsing CRS config: coreruleset/rules/REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.conf
Parsing CRS config: coreruleset/rules/REQUEST-903.9003-NEXTCLOUD-EXCLUSION-RULES.conf
...
$> ls coreruleset/rules-yaml
REQUEST-901-INITIALIZATION.yaml
REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.yaml
REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.yaml
REQUEST-903.9003-NEXTCLOUD-EXCLUSION-RULES.yaml
...
```

So everything has been transformed into a YAML format that describes the content of the rules file.

### How to export the rule set?

The export is dead simple again:

```sh
$> mkdir coreruleset/rules-new
$> crs_write.py coreruleset/rules-yaml coreruleset/rules-new
Parsing CRS structure: coreruleset/rules-yaml/REQUEST-901-INITIALIZATION.yaml
Parsing CRS structure: coreruleset/rules-yaml/REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.yaml
Parsing CRS structure: coreruleset/rules-yaml/REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.yaml
Parsing CRS structure: coreruleset/rules-yaml/REQUEST-903.9003-NEXTCLOUD-EXCLUSION-RULES.yaml
...
```

And this gives you the rule set in the new folder `coreruleset/rules-new`.

If you want, you can check the original rules and the new copy is identical:

```sh
$> ls coreruleset/rules/*.conf | while read F; do diff -q coreruleset/rules/$(basename $F) coreruleset/rules-new/$(basename $F); done
```

If there is a difference, it will be reported. If there is no output, then you're OK.

CAVEAT: If you want to use the new rules with ModSecurity, make sure you copy the data files from the rules folder to the new destination too. They come with the filename suffix `.data`, so they are easy to grab.

We have now imported a rule set and we have exported it again. So the basic tooling is in place. Time to start to manipulate the rules.

### Example 1 - Suppress certain actions across all rules

There are quite a lot of CRS rules that change the audit engine with the help of the ctl-action. This is not always welcome. Let's try and remove this action, while leaving the rest of the rule functionality in place.

`msc_parser` comes with several examples. They reside in the examples folder of the [`msc_parser` git](https://github.com/digitalwave/msc_pyparser/tree/master/examples).

This script here is example 11: [https://raw.githubusercontent.com/digitalwave/`msc_parser`/master/examples/example11\_remove\_auditlog.py](https://raw.githubusercontent.com/digitalwave/msc_pyparser/master/examples/example11_remove_auditlog.py)

```python
#!/usr/bin/env python3

import sys
import yaml

class Transform(object):
    def __init__(self, data):
    self.data = data
    self.lineno = 1
    self.lineno_shift = 0

    def removeaction(self):
    for d in self.data:
        if "actions" in d:
        aidx = 0
        while aidx < len(d['actions']):
            a = d['actions'][aidx]
            if a['act_name'] == "ctl" and a['act_arg'] == "auditLogParts" and a['act_ctl_arg'] == "+E":
            d['actions'].remove(a)
            aidx += 1

if __name__ == "__main__":
    if len(sys.argv) < 3:
    print("Argument missing!")
    print("Use: %s input output" % (sys.argv[0]))
    sys.exit(-1)

    fname = sys.argv[1]
    oname = sys.argv[2]
    try:
    with open(fname, 'r') as inputfile:
        if yaml.__version__ >= "5.1":
        data = yaml.load(inputfile.read(), Loader=yaml.FullLoader)
        else:
        data = yaml.load(inputfile.read())
    except:
    print("Can't open file: %s" % (fname))
    sys.exit()

    t = Transform(data)
    t.removeaction()

    try:
    with open(oname, 'w') as outfile:
        outfile.write(yaml.dump(t.data))
    print("Transformed file written.")
    except:
    print("Can't open file: %s" % (oname))
    sys.exit()
```

The interesting part is the function removeaction with the condition that checks for the action name "ctl" (-&gt; `a['act_name']`).

Here is how to run this script:

```sh
$> ls coreruleset/rules-yaml/*.yaml | while read F; do python3 ./example11_remove_auditlog.py coreruleset/rules-yaml/$(basename $F) coreruleset/rules-yaml-new/$(basename $F); done
Transformed file written.
Transformed file written.
Transformed file written.
Transformed file written.
…
```

With the script executing successfully, you can now export the rules in rules-yaml-new folder and get the desired CRS without the extended Auditlog.

### Example 2 - Add new tags to certain rules

Maybe you have read the blog post about the plans to [introduce CAPEC tagging into CRS](https://coreruleset.org/20200608/overhauling-the-crs-tags/). We have implemented these changes (and it's already in the CRS v3.3 release) with the help of the `msc_parser`. We prepared the CAPEC tag for every rule in a seperate CSV file (-&gt; format: rule-id;tag).

Ervin has provided us with an example named [example3\_addtag.py](https://github.com/digitalwave/msc_pyparser/blob/master/examples/example3_addtag.py) that prepends tags in front of the existing tag "OWASP\_CRS". For the CAPEC tagging, we've transformed the script into appendtag.py script by replacing the while loop (`while aidx < len…`) with a separate routine and then making sure the script takes rule ids and the tag to be appended as a command line parameter.

```python
#!/usr/bin/env python3
#
# Script to append a tag to an individual rule in a rule file.
#
# Based on https://raw.githubusercontent.com/digitalwave/msc_pyparser/master/examples/example3_addtag.py
#

import sys
import yaml

class Transform(object):
    def __init__(self, data):
    self.data = data
    self.lineno = 1
    self.lineno_shift = 0

    def inserttag(self):
    for d in self.data:
        id = None
        d['lineno'] += self.lineno_shift
        if "oplineno" in d:
        d['oplineno'] += self.lineno_shift
        if "actions" in d:
        aidx = 0
        while aidx < len(d['actions']):
            a = d['actions'][aidx]
            if a['act_name'] == "id":
            id = a['act_arg']
            if id == myid and a['act_name'] == "tag" and a['act_arg'] == "OWASP_CRS":
            newtag = {'act_arg': mytag, 'act_name': "tag", 'act_quote': "quotes", 'lineno': a['lineno']+self.lineno_shift+1}
            d['actions'].insert(aidx+1, newtag)
            d['actions'][aidx]['lineno'] -= 1
            self.lineno_shift += 1
            aidx += 1
            a['lineno'] += self.lineno_shift
            aidx += 1

if __name__ == "__main__":
    if len(sys.argv) < 5:
    print("Argument missing!")
    print("Use: %s input output id tag" % (sys.argv[0]))
    sys.exit(-1)

    fname = sys.argv[1]
    oname = sys.argv[2]
    myid = sys.argv[3]
    mytag = sys.argv[4]

    try:
    with open(fname, 'r') as inputfile:
        data = inputfile.read()
    except:
    print("Can't open file: %s" % (fname))
    sys.exit()

    t = Transform(yaml.load(data, Loader = yaml.FullLoader))
    t.inserttag()

    try:
    with open(oname, 'w') as outfile:
        outfile.write(yaml.dump(t.data))
    print("Transformed file written.")
    except:
    print("Can't open file: %s" % (oname))
    sys.exit()
```

Unlike the previous example, this script does not work on the complete rules folder anymore. Instead you need to call it separately for every rule file. That's very simple with a shell wrapper script. I had prepared the new tags in a CSV file with rule-id and tag on a line.

So I got two nested loops. This is not a very efficient way of performing this update so we better restrict the inner nested loop to the relevant IDs, that we can filter with the rule id prefix (the first three digits, that are also part of the filename). That way the script becomes very simple and effective while still having acceptable performance:

`wrapper.sh`

```bash
#!/bin/bash
#
# Wrapper script to loop over ModSecurity rule files and add tags
# described in a separate CSV to the individual rules
#

if [ ! -d coreruleset/rules-yaml-new ]; then
    mkdir coreruleset/rules-yaml-new
fi
cp coreruleset/rules-yaml/*.yaml coreruleset/rules-yaml-new

ls coreruleset/rules-yaml | egrep '\S-[0-9]{3}-' | while read F; do
    ID_prefix=$(echo $F | egrep -o "[0-9]{3}")
    echo $ID_prefix
    cat capeclist.csv | egrep "^$ID_prefix" | while read LINE; do
        # format of capeclist.csv
        # ...
        # 951230 capec/1000/118/116/54
        # ...
        ID=$(echo $LINE | cut -d\  -f1)
        TAG=$(echo $LINE | cut -d\  -f2)
        appendtag.py coreruleset/rules-yaml-new/$F /tmp/append$$ "$ID" "$TAG"
        mv /tmp/append$$ coreruleset/rules-yaml-new/$F
    done
done

```

The wrapper script assumes, you have already executed crs\_read.py and the rules reside under coreruleset/rules-yaml. You will then get the new version with the additional tags in coreruleset/rules-yaml-new. Ready for the export with crs\_write.py.

### Example 3 - Remove certain rules from the rule set

The tutorials at [netnea.com](https://netnea.com/apache-tutorials) are quite extensive when it comes to writing rule exclusions. The directive `SecRuleRemoveById` lets you remove an individual rule from the rule set at startup time. But how about tailoring your rule set so the rule is removed from the file?

Here is a script that takes a rule ID as a third argument when filtering the rule:

`remove_rule_by_id.py`

```python
#!/usr/bin/env python3
#
# Script to remove a rule by id
#
# By Ervin Hegedüs
#

import yaml
import sys
from msc_pyparser import MSCUtils as u
import os

class Check(object):
    def __init__(self, data, ruleid):
    self.data = data
    self.current_ruleid = 0
    self.filtered = False
    self.curr_lineno = 0
    self.chained = False
    self.chainlevel = 0
    self.filtered_items = []
    self.offset = 0
    self.rule_ids_to_filter = [int(ruleid)]

    def filter_rules(self):
    # walk through the items
    firstline = 0
    lastline = 0
    for d in self.data:
        d['lineno'] -= self.offset
        # item contains action - so it contans `id` (the whole chain)
        if "actions" in d:
        d['oplineno'] -= self.offset
        aidx = 0
        if self.chained == True:
            self.chained = False
        while aidx < len(d['actions']):
            a = d['actions'][aidx]
            self.curr_lineno = a['lineno']

            d['actions'][aidx]['lineno'] -= self.offset

            if a['act_name'] == "id":
            self.current_ruleid = int(a['act_arg'])
            if self.current_ruleid in self.rule_ids_to_filter:
                self.filtered = True
                firstline = d['lineno']

            if a['act_name'] == "chain":
            self.chained = True
            self.chainlevel += 1

            aidx += 1

        if self.filtered == False:
            self.filtered_items.append(d)

        # need to check only if there is an action at least
        # check if the rules are chained or not, if it is, then
        # need to handle them as one
        if self.chained == False:
            lastline = self.curr_lineno
            if self.filtered == True:
            self.offset += (lastline-firstline)+1
            self.current_ruleid = 0
            self.chainlevel = 0
            self.filtered = False
        # no actions - no `id`, append the filtered list
        else:
        self.filtered_items.append(d)

        

if __name__ == "__main__":

    if len(sys.argv) < 3:
    print("Argument missing!")
    print("Use: %s /path/to/source.yaml /path/to/modified.yaml rule-id" % (sys.argv[0]))
    sys.exit(-1)

    fname = sys.argv[1]
    oname = sys.argv[2]
    ruleid = sys.argv[3]

    try:
    with open(fname) as file:
        if yaml.__version__ >= "5.1":
        data = yaml.load(file, Loader=yaml.FullLoader)
        else:
        data = yaml.load(file)
    except:
    print("Can't open file: %s" % (fname))
    sys.exit()

    c = Check(data, ruleid)
    c.filter_rules()

    try:
    with open(oname, 'w') as outfile:
        outfile.write(yaml.dump(c.filtered_items))
    print("Filtered file written.")
    except:
    print("Can't open file: %s" % (oname))
    sys.exit()

```

And here is how to call the script:

`$> remove_rule_by_id.py /tmp/coreruleset/rules-yaml/REQUEST-920-PROTOCOL-ENFORCEMENT.yaml /tmp/coreruleset/rules-yaml-new/REQUEST-920-PROTOCOL-ENFORCEMENT.yaml 920180`

Obviously, you need to wrap it again to loop over all the files. Namely when you are not quite sure in which the rule in question is residing.

Unfortunately, there is a beauty defect in the way the rule is removed: It's the fact that the comment describing the rule will still be there. Only the active rule itself is being removed. But I guess you can live with that.

### Example 4 - Filter for rules containing certain actions

Searching a rule set for rules with certain characteristics is another use case for `msc_parser`. In this example (provided by Ervin again), we search for rules containing the "capture" action in combination with the "chain" action.

`collect_rx_op.py`

```python
#!/usr/bin/env python3
#
# Script to search a rule set for rules containing
# the capture and the chain action
#
# By Ervin Hegedüs
#

import yaml
import sys
from msc_pyparser import MSCUtils as u
import os
import re

class Check(object):
    def __init__(self, src, data):
    self.source = src
    self.data = data
    self.current_ruleid = 0
    self.has_capture = False
    self.last_ruleid = 0
    self.curr_lineno = 0
    self.chained = False
    self.chainlevel = 0

    def collectrx(self):
    self.chained = False
    patterns = []
    for d in self.data:
        if d['type'].lower() != "secrule":
        continue
        if d['operator'] == "@rx":
        patterns.append(d['operator_argument'])
        if "actions" in d:
        act_idx = 0
        if self.chained == True:
            self.chained = False
        while act_idx < len(d['actions']):
            a = d['actions'][act_idx]

            self.curr_lineno = a['lineno']
            if a['act_name'] == "id":
            self.current_ruleid = int(a['act_arg'])

            if a['act_name'] == "capture":
            self.has_capture = True

            if a['act_name'] == "chain":
            self.chained = True
            self.chainlevel += 1

            act_idx += 1

        # end of (chained) rule
        if self.chained == False:
            if len(patterns) > 0:
            pi = 1
            if self.has_capture == True and len(patterns) > 0 and self.chainlevel > 0:
            print(self.current_ruleid, len(patterns), patterns)
            self.current_ruleid = 0
            self.has_capture = False
            self.chainlevel = 0
            patterns = []

if __name__ == "__main__":

    if len(sys.argv) < 2:
    print("Argument missing!")
    print("Use: %s /path/to/rules-yaml" % (sys.argv[0]))
    sys.exit(-1)

    srcobj = sys.argv[1]

    st = u.getpathtype(srcobj)
    if st == u.UNKNOWN:
    print("Unknown source path!")
    sys.exit()

    configs = []
    if st == u.IS_DIR:
    for f in os.listdir(srcobj):
        fp = os.path.join(srcobj, f)
        if os.path.isfile(fp) and os.path.basename(fp)[-5:] == ".yaml":
        configs.append(fp)
    if st == u.IS_FILE:
    configs.append(srcobj)

    configs.sort()

    for c in configs:
    try:
        with open(c) as file:
        #print("Reading file: %s" % c)
        if yaml.__version__ >= "5.1":
            data = yaml.load(file, Loader=yaml.FullLoader)
        else:
            data = yaml.load(file)
    except:
        print("Exception catched - ", sys.exc_info())
        sys.exit(-1)

    chk = Check(c.replace(".yaml", "").replace(srcobj, ""), data)
    chk.collectrx()

```

The interesting part of the script is near the use of the keywords "`capture`" and "`chain`". And then the print statement of course. You can call this script with the imported rules folder as parameter and it will loop over all the config files.

It should be easy to adopt this for your specific needs if you want to search for rules with different characteristics.

So these were four examples with different use cases for [`msc_parser`](https://github.com/digitalwave/msc_pyparser/blob/master/README.md). The [example folder](https://github.com/digitalwave/msc_pyparser/tree/master/examples) of the library's github has more than a dozen of them as of this writing. So check them out if you have an idea that is not covered in this blog post!  
  
Ervin Hegedüs &amp; Christian Folini
