---
title: Sandbox
description: Send a request to the CRS Sandbox and see which rules it triggers on Apache, Nginx or Coraza, with the CRS version and paranoia level of your choice.
url: /sandbox
---

The CRS Sandbox is a public instance of OWASP CRS running on
three WAF engines ([ModSecurity](https://github.com/owasp-modsecurity/ModSecurity) 2 on Apache,
ModSecurity 3 on Nginx, and [Coraza](https://coraza.io/)) in several CRS versions. Send it a request,
pick the engine, version and paranoia level with headers, and get back the rules that matched instead of the page.

It is there for integrators who need to know how CRS reacts to a fresh exploit, for researchers who
want to check whether a payload is caught and from which paranoia level on, and for rule writers
who want to try a variant without setting up a WAF. The sandbox is a shared public resource: read the
[security policy](/docs/crs-sandbox-policy/) before you use it, and the
[documentation](/docs/6-development/6-4-using-the-crs-sandbox/) for the architecture behind it.

Use the form below, or the headers directly from the command line further down.

{{< crs-sandbox >}}

## From the command line

Every option in the form is a request header. Send the request to `https://sandbox.coreruleset.org`
with any path, method, query string or body you like:

```shell
curl -H "x-backend: nginx" \
     -H "x-crs-version: latest" \
     -H "x-crs-paranoia-level: 2" \
     -H "x-format-output: txt-matched-rules" \
     "https://sandbox.coreruleset.org/get?file=../../etc/passwd"
```

| Header | Values | Default |
|--------|--------|---------|
| `x-backend` | `apache`, `nginx`, `coraza` | `apache` |
| `x-crs-version` | `v4-lts`, `v3-lts`, `latest` (`coraza` has no `v3-lts`) | `v4-lts` |
| `x-crs-paranoia-level` | `1` to `4`, blocking and detection | `1` |
| `x-crs-detection-paranoia-level` | `1` to `4`, detection only | same as above |
| `x-crs-inbound-anomaly-score-threshold` | number | `5` |
| `x-crs-mode` | `detection` for DetectionOnly, never blocks | blocking |
| `x-format-output` | `json-matched-rules`, `json-report`, `csv-matched-rules`, `txt-matched-rules`, `txt-matched-rules-extended`, `html-matched-rules` | raw audit log |

`GET https://sandbox.coreruleset.org/backends` returns the supported combinations as JSON.
The response carries `x-backend` with the service that answered and `x-crs-version` with the exact
CRS tag it runs, so `latest` always resolves to something you can check.

`txt-matched-rules-extended` wraps the list in a paragraph you can paste into an advisory or a
publication ("This payload has been tested against the OWASP CRS... CRS therefore detects this
payload starting with paranoia level 1"). The JSON formats pair well with `jq`.

## Good to know

- The response body is the WAF's verdict, not the page you asked for. Behind every WAF is a small
  HTTP mirror ([go-httpbin](https://github.com/mccutchen/go-httpbin)) that accepts anything, so you
  can use any path and any method.
- A `403` with a blocking rule (`949110`) in the list means CRS blocked the request. In detection
  mode, or when the anomaly score stays below the threshold, you get the matched rules with a `200`.
- The form sends what a browser can send. Before the request leaves the browser, `#fragments` are
  dropped, `..` path segments and backslashes are resolved, control characters are removed and most
  special characters are percent-encoded; the result shows the URL that was actually sent. Headers
  such as `Cookie`, `Host` or `Referer` cannot be set from a page at all. For raw bytes use curl
  (`--path-as-is` keeps `..` segments).
- A `400` with `"source": "sandbox-edge"` in the body comes from the sandbox's own HTTP parser or
  from the backend web server, not from CRS: the request was malformed and was never scanned. A `502`
  after a long wait usually means the request made a regular expression time out (ReDoS).
- Please keep it under 10 requests per second.
- Requests are logged in full and may be kept and analysed by the CRS team to improve the rules and
  the sandbox, see the [security policy](/docs/crs-sandbox-policy/). Do not send real credentials or
  personal data.
- Something broken? [Open an issue](https://github.com/coreruleset/coreruleset/issues) and include the
  `x-unique-id` shown with the result.
