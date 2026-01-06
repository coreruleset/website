---
title: 'CVE-2026-21876: Critical Multipart Charset Bypass Fixed in CRS 4.22.0 and 3.3.8'
date: '2026-01-06'
author: fzipi
description: "OWASP CRS addresses a critical charset validation bypass in rule 922110 affecting all supported versions. The vulnerability allowed UTF-7 and other charset-based attacks to evade detection through a chained rule processing flaw."
categories:
  - Blog
  - Security
---

We are disclosing a security bypass vulnerability in OWASP CRS that affects rule 922110, which validates charset parameters in multipart/form-data requests. This vulnerability, assigned **CVE-2026-21876**, has existed since the rule was introduced and affected all CRS supported versions.

| | |
|-|-|
| Published | January 6, 2026 |
| Reported by | some0ne (https://github.com/daytriftnewgen) |
| Fixed by | Ervin Hegedüs (airween) and Felipe Zipitría (fzipi) |
| Severity | CRITICAL (CVSS 9.3) |
| Internal ID | 9AJ-260102 |

The vulnerability allows attackers to bypass charset validation by exploiting how ModSecurity's chained rules process collections. We have developed and tested a fix that is now available in **CRS version 4.22.0** and **CRS version 3.3.8**.

## TL;DR

**What:** Rule 922110 only validates the LAST multipart part's charset, allowing malicious charsets in earlier parts to bypass detection{{< br >}}
**Impact:** UTF-7, UTF-16, and other charset-based attacks can reach backend applications{{< br >}}
**Affected:** CRS 3.3.x and 4.0.0 - 4.21.0 (all engines){{< br >}}
**Fix:** Upgrade to CRS 4.22.0 (for 4.x) or CRS 3.3.8 (for 3.3.x){{< br >}}
**CVSS:** 9.3 (CRITICAL) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N`{{< br >}}
**CWE:** CWE-794 (Incomplete Filtering of Multiple Instances of Special Elements){{< br >}}
**Internal ID:** 9AJ-260102{{< br >}}

---

## Background: What is Rule 922110?

Rule 922110 is a Paranoia Level 1 rule (enabled by default) that validates charset parameters in Content-Type headers within multipart/form-data requests. The rule is designed to block dangerous charset encodings that can be used to bypass XSS filters and other security mechanisms.

**Allowed charsets:**
- `utf-8`
- `iso-8859-1`
- `iso-8859-15`
- `windows-1252`

**Blocked charsets (attack vectors):**
- `utf-7` (UTF-7 encoded XSS)
- `utf-16`, `utf-32` (UTF-16/32 attacks)
- `shift-jis`, `euc-jp`, `gb2312` (various charset confusion attacks)
- Any other non-whitelisted charset

### Why This Matters

UTF-7 XSS is a well-documented attack technique. By encoding malicious JavaScript in UTF-7, attackers can bypass many XSS filters that expect standard ASCII or UTF-8 encoding. For example:

```
+ADw-script+AD4-alert(document.cookie)+ADw-/script+AD4-
```

This is the UTF-7 encoded version of:
```html
<script>alert(document.cookie)</script>
```

Rule 922110 was designed to detect and block these attacks at the WAF layer, before they reach the backend application.

---

## The Vulnerability

### Technical Root Cause

The vulnerability stems from a fundamental behavior in how ModSecurity processes chained rules when iterating over collections. The original rule structure was:

```apache
SecRule MULTIPART_PART_HEADERS "@rx ^content-type\s*:\s*(.*)$" \
    "id:922110,phase:2,block,capture,t:none,t:lowercase,chain"
    SecRule TX:1 "!@rx ^(?:...validation regex...)$" \
        "setvar:'tx.inbound_anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```

**The Problem:**

When ModSecurity processes this chained rule against a multipart request with multiple parts:

1. The parent rule iterates through **ALL** `MULTIPART_PART_HEADERS`
2. For each Content-Type header found, it captures the charset value to `TX:1` using the `capture` action
3. Each iteration **overwrites** the previous `TX:1` value
4. After **ALL** iterations complete, the chained rule executes **once**
5. The chained rule only sees the **last** value stored in `TX:1`

This means if an attacker places:
- **First part:** Malicious charset (`charset=utf-7`) with attack payload
- **Last part:** Legitimate charset (`charset=utf-8`)

The rule only validates the last part's charset and the attack bypasses detection.

### Proof of Concept

```http
POST /vulnerable-endpoint HTTP/1.1
Host: target.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary

------WebKitFormBoundary
Content-Disposition: form-data; name="username"
Content-Type: text/plain; charset=utf-7

+ADw-script+AD4-alert(document.cookie)+ADw-/script+AD4-
------WebKitFormBoundary
Content-Disposition: form-data; name="dummy"
Content-Type: text/plain; charset=utf-8

legitimate_data
------WebKitFormBoundary--
```

**Result:** The UTF-7 encoded XSS payload in the first part bypasses rule 922110 because the rule only checks the second part's charset (utf-8, which is legitimate).

### Why This Bug Existed

This is not a simple coding error, but rather an interaction between:

1. **ModSecurity's design:** Capture variables (`TX:0`, `TX:1`, etc.) are global within a transaction
2. **Collection iteration:** When a rule targets a collection, ModSecurity iterates through all members
3. **Chained rule execution:** The chained rule executes **once** after **all** iterations, not once per iteration
4. **Validation logic:** The rule needed to validate a captured group (`TX:1`), not the full match

This combination created a subtle but critical vulnerability that went undetected for years.

---

## Impact Assessment

### Direct Impact

- **Attack Vector:** Network (no authentication required)
- **Attack Complexity:** Low (trivial to exploit)
- **Scope:** Changed (crosses security boundary from WAF to backend)
- **Affects:** ALL CRS installations running versions 3.0.0 - 4.21.0

### Real-World Scenarios

**Scenario 1: UTF-7 XSS Bypass**
1. Application has XSS vulnerability
2. CRS rule 922110 should block UTF-7 encoded payloads
3. Attacker uses multipart bypass technique
4. UTF-7 XSS reaches backend and executes in victim's browser

**Scenario 2: Charset Confusion in APIs**
1. API accepts multipart data
2. Backend parses with charset-sensitive parser
3. Attacker sends UTF-16/UTF-32 encoded SQL injection
4. WAF bypass allows attack to reach vulnerable SQL query

### Why Score 9.3 (CRITICAL)?

We scored this vulnerability as:

**CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N = 9.3 (CRITICAL)**

The key factors:
- **Attack Vector: Network** - No special access required
- **Attack Complexity: Low** - Trivial to exploit
- **Privileges Required: None** - No authentication needed
- **User Interaction: None** - Server-side vulnerability
- **Scope: Changed** - WAF is a security boundary; bypass breaks defense-in-depth
- **Confidentiality: High** - Enables data disclosure via XSS/SQLi
- **Integrity: Low** - The bypass allows some integrity impact through charset-encoded payloads reaching the backend
- **Availability: None** - No direct DoS impact

**Why CRITICAL (9.3)?**

The score crosses into CRITICAL territory (≥9.0) because:
1. **Zero prerequisites** - No authentication, no user interaction required
2. **Trivial exploitation** - Simple multipart request construction
3. **Scope change** - Breaks security boundary with 1.08 multiplier in CVSS formula
4. **Real attack vectors** - UTF-7 XSS and charset confusion are actively used
5. **Widespread deployment** - Affects all CRS installations (default PL1 rule)
6. **Defense-in-depth failure** - WAF bypass defeats the entire purpose of the protection layer

This scoring reflects that the vulnerability enables serious attacks with minimal effort, even though full exploitation requires a backend vulnerability.

---

## The Fix

The fix uses an incremental counter to create unique TX variable keys for each captured charset value, then validates all stored values:

```apache
# Rule 922140: Initialize counter
SecRule &MULTIPART_PART_HEADERS "@gt 0" \
    "id:922140,\
    phase:2,\
    pass,\
    t:none,\
    nolog,\
    tag:'attack-multipart-header',\
    tag:'OWASP_CRS',\
    tag:'OWASP_CRS/MULTIPART-ATTACK',\
    ver:'OWASP_CRS/4.22.0-dev',\
    setvar:'tx.multipart_headers_content_counter=0'"

# Rule 922150: Capture each content-type to uniquely numbered TX variable
SecRule MULTIPART_PART_HEADERS "@rx ^content-type\s*:\s*(.*)$" \
    "id:922150,\
    phase:2,\
    pass,\
    capture,\
    t:none,t:lowercase,\
    nolog,\
    tag:'attack-multipart-header',\
    tag:'OWASP_CRS',\
    tag:'OWASP_CRS/MULTIPART-ATTACK',\
    ver:'OWASP_CRS/4.22.0-dev',\
    setvar:'tx.multipart_headers_content_types_%{tx.multipart_headers_content_counter}=%{tx.1}',\
    setvar:'tx.multipart_headers_content_counter=+1'"

# Rule 922110: Validate ALL captured charset values
SecRule TX:/MULTIPART_HEADERS_CONTENT_TYPES_*/ "!@rx ^(?:...validation regex...)$" \
    "id:922110,\
    phase:2,\
    block,\
    capture,\
    t:none,t:lowercase,\
    msg:'Illegal MIME Multipart Header content-type: charset parameter',\
    logdata:'Matched Data: %{MATCHED_VAR} found within Content-Type multipart form',\
    tag:'application-multi',\
    tag:'language-multi',\
    tag:'platform-multi',\
    tag:'attack-multipart-header',\
    tag:'attack-protocol',\
    tag:'paranoia-level/1',\
    tag:'OWASP_CRS',\
    tag:'OWASP_CRS/MULTIPART-ATTACK',\
    tag:'capec/272/220',\
    ver:'OWASP_CRS/4.22.0-dev',\
    severity:'CRITICAL',\
    setvar:'tx.inbound_anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```

**How it works:**

1. **Rule 922140** initializes a counter to 0 (only if multipart data exists)
2. **Rule 922150** iterates through all multipart headers:
   - First part: stores `tx.multipart_headers_content_types_0 = "text/plain; charset=utf-7"`
   - Second part: stores `tx.multipart_headers_content_types_1 = "text/plain; charset=utf-8"`
   - Counter increments each time
3. **Rule 922110** uses regex pattern matching `TX:/MULTIPART_HEADERS_CONTENT_TYPES_*/` to check **ALL** stored values
4. If **ANY** value has a bad charset → blocks

This solution:
- ✅ Checks ALL parts, not just the last one
- ✅ Handles duplicate part names (counter ensures uniqueness)
- ✅ No lookahead assertions (compatible with RE2/Rust regex)
- ✅ Works across ModSecurity v2, v3, and Coraza
- ✅ Minimal performance overhead

**Full implementation:** https://github.com/coreruleset/coreruleset/commit/9917985de09a6cf38b3261faf9105e909d67a7d6

---

## Affected Versions and Compatibility

### Affected CRS Versions

**Supported versions:**
- CRS 3.3.x (currently supported)
- CRS 4.0.0 - 4.21.0 (currently supported)

See the [CRS Security Policy](https://github.com/coreruleset/coreruleset/blob/main/SECURITY.md) for version support details.

### Affected Engines

The vulnerability affects rule 922110 regardless of which WAF engine is used:
- ✅ Apache ModSecurity 2.x (all versions)
- ✅ ModSecurity 3.x / libmodsecurity (all versions)
- ✅ Coraza (all versions)

The bug is in the **rule logic**, not the engine implementation.

---

## Remediation

### Option 1: Upgrade (Recommended)

Upgrade to the patched version for your branch:

**For CRS 4.x users:**
- **CRS 4.22.0** (released January 2026) - includes the fix
- Download: https://github.com/coreruleset/coreruleset/releases/tag/v4.22.0

**For CRS 3.3.x users:**
- **CRS 3.3.8** (released January 2026) - backport with the fix
- Download: https://github.com/coreruleset/coreruleset/releases/tag/v3.3.8

**Installation:**
- https://coreruleset.org/installation/

### Option 2: Apply Backport Patches

For users who cannot immediately upgrade but need the fix:

- **CRS 3.3.x users:** Upgrade to 3.3.8 (recommended over manual patching)
- **CRS 4.x users:** Upgrade to 4.22.0

### Verification

After upgrading, verify the fix is active:

```bash
# Check CRS version
grep "ver:'OWASP_CRS/" /path/to/rules/REQUEST-922-MULTIPART-ATTACK.conf

# Should show version 4.22.0 or higher

# Verify rule 922140 and 922150 exist (the new helper rules)
grep -A 2 "id:922140" /path/to/rules/REQUEST-922-MULTIPART-ATTACK.conf
grep -A 2 "id:922150" /path/to/rules/REQUEST-922-MULTIPART-ATTACK.conf

# Verify rule 922110 is updated (no longer uses 'chain' action)
grep -A 5 "id:922110" /path/to/rules/REQUEST-922-MULTIPART-ATTACK.conf | grep -q "chain" && echo "OLD VERSION" || echo "FIXED VERSION"
```

**Note on Rule IDs:** The fix introduces two new rules (922140, 922150) while modifying the existing 922110. All three rules work together to provide complete charset validation across all multipart parts.

---

## Testing

We have created a comprehensive test suite with 30 test cases covering:

- **Core bypass scenarios:** Malicious charset in first/middle/last positions
- **Edge cases:** Duplicate part names, empty multiparts, no Content-Type headers
- **Attack vectors:** UTF-7, UTF-16, UTF-32, Shift-JIS, EUC-JP
- **Legitimate traffic:** Various allowed charsets and format variations
- **Stress tests:** Up to 15 multipart parts

The test suite is available in the CRS repository at:
`tests/regression/tests/REQUEST-922-MULTIPART-ATTACK/922110.yaml`

Run tests with go-ftw:
```bash
./go-ftw run -d tests/regression/tests/REQUEST-922-MULTIPART-ATTACK/ -i "922110"
```

---

## Timeline

- **January 2, 2026:** Vulnerability discovered and reported by some0ne (https://github.com/daytriftnewgen)
- **January 2, 2026:** OWASP CRS team assigned internal tracking ID 9AJ-260102
- **January 3-5, 2026:** Fix development and testing by airween and fzipi
- **January 5, 2026:** Fix verified across ModSecurity v2, v3, and Coraza
- **January 6, 2026:** CVE-2026-21876 assigned by GitHub Security
- **January 6, 2026:** CRS 4.22.0 and CRS 3.3.8 released with fix
- **January 6, 2026:** Public disclosure (coordinated with fix availability)

---

## Technical Deep Dive

### Understanding ModSecurity Chained Rule Behavior

The core issue is how ModSecurity handles chained rules when the parent rule targets a collection variable.

**Normal single-value rule:**
```apache
SecRule ARGS:username "@rx attack" "id:1,block,capture,chain"
    SecRule TX:1 "@rx malicious"
```
This works fine - `TX:1` contains the captured value from `ARGS:username`.

**Collection-based rule (the problem):**
```apache
SecRule ARGS "@rx attack" "id:2,block,capture,chain"
    SecRule TX:1 "@rx malicious"
```

When `ARGS` contains multiple parameters (`username=foo&password=bar`):
1. Matches `ARGS:username` → captures to `TX:1 = "foo"`
2. Matches `ARGS:password` → **overwrites** `TX:1 = "bar"`
3. Chain executes **once** with `TX:1 = "bar"` (the last value)

This is **by design** in ModSecurity - not a bug in the engine. However, it creates a security vulnerability when used for validation in security-critical rules.

### Why 922110 Was Particularly Vulnerable

Rule 922110 had the perfect storm of conditions:

1. ✅ Targets a **collection** (`MULTIPART_PART_HEADERS`)
2. ✅ Uses **capture** to extract charset value
3. ✅ **Chained rule** validates the captured value
4. ✅ Validation is **negative** (checking for bad charsets)
5. ✅ Attack can be in **first** part, legitimate in **last** part

This specific combination made the bypass possible and reliable.

### Attack Scenario Walkthrough

Let's trace through exactly what happens with the buggy rule:

**Malicious Request:**
```
Part 1: Content-Type: text/plain; charset=utf-7  ← ATTACK
Part 2: Content-Type: text/plain; charset=utf-8  ← LEGITIMATE
```

**Execution with Buggy Rule:**
```
1. Rule 922110 (parent) starts iterating MULTIPART_PART_HEADERS
2. Iteration 1 (Part 1):
   - Matches: "content-type: text/plain; charset=utf-7"
   - Captures: TX:1 = "text/plain; charset=utf-7"
3. Iteration 2 (Part 2):
   - Matches: "content-type: text/plain; charset=utf-8"
   - Captures: TX:1 = "text/plain; charset=utf-8" (OVERWRITES)
4. Parent rule returns 1 (matched at least once)
5. Chained rule executes ONCE:
   - Checks: TX:1 (= "text/plain; charset=utf-8")
   - Validation: charset=utf-8 is allowed → PASSES
6. Result: Request allowed ❌
```

**Execution with Fixed Rule:**
```
1. Rule 922140: Initializes counter = 0
2. Rule 922150 iterates:
   - Part 1: tx.multipart_headers_content_types_0 = "text/plain; charset=utf-7"
   - Part 2: tx.multipart_headers_content_types_1 = "text/plain; charset=utf-8"
3. Rule 922110: Checks TX:/MULTIPART_HEADERS_CONTENT_TYPES_*/
   - Checks: tx.multipart_headers_content_types_0 → charset=utf-7 → FAILS validation
   - Result: BLOCKED ✅
```

### Why We Couldn't Use Simpler Fixes

**Q: Why not just use `MATCHED_VAR` instead of `TX:1`?**

A: Because `MATCHED_VAR` contains the **entire** matched string:
```
MATCHED_VAR = "content-type: text/plain; charset=utf-7"
TX:1 = "text/plain; charset=utf-7"  ← This is what we need
```

The validation regex expects the value **after** the `"content-type: "` prefix. Using `MATCHED_VAR` would check the wrong string.

**Q: Why not use regular expression backreferences?**

A: We could theoretically use a single regex with backreferences to both capture and validate in one step. However, CRS maintains compatibility with multiple regex engines:
- **PCRE** (ModSecurity v2/v3) - Supports backreferences
- **RE2** (Golang/Coraza) - Does NOT support backreferences
- **Rust regex** - Does NOT support backreferences

To ensure CRS rules work across all supported engines, we avoid regex features like:
- Backreferences (`\1`, `\2`, etc.)
- Lookahead/lookbehind assertions (`(?=...)`, `(?<=...)`)
- Conditional patterns (`(?(condition)yes|no)`)

This is why we use the counter-based approach instead.

**Q: Why not just remove the chain?**

A: We need to capture the charset value (the part after `content-type:`) to validate it. A single non-chained rule can't both extract and validate in one step without using complex lookahead assertions or backreferences (both of which we avoid for regex engine compatibility).

**Q: Why not store by part name?**

A: Multipart parts can have duplicate names:
```
name="username"  ← First occurrence
name="username"  ← Second occurrence overwrites the first
```

Using an incremental counter ensures every value is stored uniquely.

---

## Edge Cases and Attack Variations

Our fix handles several important edge cases:

### 1. Duplicate Part Names
```
Part 1: name="data", charset=utf-7    ← ATTACK
Part 2: name="data", charset=utf-8    ← LEGITIMATE
```
✅ Fixed - Counter creates unique keys regardless of name

### 2. Multiple Malicious Parts
```
Part 1: charset=utf-7     ← ATTACK 1
Part 2: charset=utf-16    ← ATTACK 2
Part 3: charset=utf-8     ← LEGITIMATE
```
✅ Fixed - Detects both attacks

### 3. Malicious in Middle Position
```
Part 1: charset=utf-8     ← LEGITIMATE
Part 2: charset=utf-7     ← ATTACK
Part 3: charset=utf-8     ← LEGITIMATE
```
✅ Fixed - Position doesn't matter

### 4. Large Multipart Requests
15+ parts with malicious charset in position 10
✅ Fixed - Checks all parts regardless of count

---

## Lessons Learned

This vulnerability highlights several important points about WAF rule development:

### 1. Chained Rules with Collections Are Dangerous

When using chained rules that iterate over collections:
- **Capture variables get overwritten** with each iteration
- **Chains execute once** after all iterations
- This pattern should be avoided for validation logic

### 2. Testing is Critical

This bug existed for years across multiple CRS versions. Comprehensive testing with:
- Edge cases (duplicate names, position variations)
- Multiple parts in different orders
- Stress tests with many parts

...would have caught this earlier.

### 3. Engine Behavior Documentation

ModSecurity's chained rule behavior with collections is documented but subtle. Rule developers need to understand:
- When chains execute
- How capture variables work
- Collection iteration mechanics

### 4. Security Review of Existing Rules

This discovery prompted us to audit other rules for similar patterns. We completed a comprehensive review and found:
- Rule 922110 was the **only** rule affected by this specific pattern
- Other rules using similar constructs work differently and are not vulnerable
- The audit confirmed no additional fixes are needed

---

## For CRS Developers and Contributors

### Pattern to Avoid

```apache
# DANGEROUS PATTERN - DO NOT USE
SecRule COLLECTION_VARIABLE "@rx regex_with_capture" \
    "capture,chain"
    SecRule TX:1 "validation_operator"
```

When:
- `COLLECTION_VARIABLE` expands to multiple members
- You need to validate captured data
- Validation is negative (looking for bad patterns)

### Safer Alternatives

**Option 1: Store and iterate (like our fix)**
```apache
SecRule COLLECTION "@rx pattern" \
    "capture,setvar:'tx.unique_key_%{tx.counter}=%{TX.1}',setvar:'tx.counter=+1'"

SecRule TX:/^unique_key_/ "validation"
```

**Option 2: Use non-chained rules with negative patterns**
```apache
# If you can express "bad" without capturing
SecRule COLLECTION "@rx bad_pattern_direct" "block"
```

**Option 3: Use @pm or @pmFromFile**
```apache
# For simple pattern lists
SecRule COLLECTION "@pmFromFile bad-charsets.data" "block"
```

### Adding to CRS Linter

We are adding detection for this pattern to the CRS linter tool to prevent future occurrences:
- Check for: collection iteration + capture + TX:N in chained rule
- Warn developers about this dangerous pattern
- Suggest safer alternatives

---

## FAQ

**Q: Am I vulnerable if I'm using CRS 4.21.0?**
A: Yes, if rule 922110 is enabled (it is by default in Paranoia Level 1).

**Q: Has this been exploited in the wild?**
A: We have no evidence of active exploitation, but the vulnerability is trivial to exploit once known.

**Q: Do I need to change my ModSecurity configuration?**
A: No, just upgrade CRS. The fix is backward compatible.

**Q: Will this break my existing setup?**
A: No, the fix maintains the same behavior for legitimate traffic. The only change is properly catching attacks that were previously bypassing.

**Q: Does this affect ModSecurity v2 or v3 differently?**
A: No, both are affected equally. The bug is in the CRS rule logic, not the engine.

**Q: Are there other rules with this same bug?**
A: We have completed a comprehensive audit of all CRS rules and confirmed that rule 922110 is the only rule affected by this specific pattern. No other rules use the vulnerable combination of collection iteration + chained rules + capture variable validation.

---

## References

- **CVE:** CVE-2026-21876 (assigned by GitHub Security)
- **CWE:** CWE-794 (Incomplete Filtering of Multiple Instances of Special Elements)
- **CVSS:** 9.3 (CRITICAL) - `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N`
- **Internal ID:** 9AJ-260102
- **Security Policy:** https://github.com/coreruleset/coreruleset/blob/main/SECURITY.md

### Fixed Releases

- **CRS 4.22.0:** https://github.com/coreruleset/coreruleset/releases/tag/v4.22.0
- **CRS 3.3.8:** https://github.com/coreruleset/coreruleset/releases/tag/v3.3.8

### Documentation

- ModSecurity v3 Reference Manual: https://github.com/owasp-modsecurity/ModSecurity/wiki/Reference-Manual-(v3.x)
- ModSecurity v2 Reference Manual: https://github.com/owasp-modsecurity/ModSecurity/wiki/Reference-Manual-(v2.x)
- Coraza Documentation: https://coraza.io/docs/
- CRS Documentation: https://coreruleset.org/docs/

---

## Acknowledgments

We would like to thank:

- **some0ne** (https://github.com/daytriftnewgen) for discovering and reporting this vulnerability (Internal ID: 9AJ-260102)
- **Ervin Hegedüs (airween)** and **Felipe Zipitría (fzipi)** for developing and testing the fix
- **The OWASP CRS team** for rapid response and coordinated disclosure
- **GitHub Security** for CVE assignment and coordination

---

## Call to Action

### For CRS Users

1. **Upgrade immediately** to the fixed version for your branch:
   - **CRS 4.x users:** Upgrade to CRS 4.22.0
   - **CRS 3.3.x users:** Upgrade to CRS 3.3.8
2. **Test your setup** after upgrading to ensure no disruption
3. **Review your logs** for any suspicious multipart requests from the past
4. **Share this advisory** with your security team

### For Security Researchers

If you discover similar issues in CRS or ModSecurity:
- Report responsibly to security@coreruleset.org
- We respond quickly and credit discoverers appropriately
- Help us make WAF protection stronger for everyone

### For Rule Developers

- Review the technical deep dive section
- Avoid the dangerous chained rule pattern with collections
- Use comprehensive test suites with edge cases
- Consider this when developing custom ModSecurity rules

---

## Conclusion

CVE-2026-21876 represents a critical security issue in CRS with a CVSS score of **9.3 (CRITICAL)**. The vulnerability demonstrates the complexity of WAF rule development and the importance of understanding subtle engine behaviors when working with chained rules and collection variables.

The good news:
- ✅ Fix is available and tested
- ✅ Upgrade path is straightforward
- ✅ No configuration changes required
- ✅ Backward compatible
- ✅ Works across all engines

We urge all CRS users to upgrade to version 4.22.0 as soon as possible.

Stay secure,
The OWASP CRS Team

---

*Disclosure: This post was written assisted by AI*
