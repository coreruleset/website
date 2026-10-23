# Logstash Ruby filter script: flatten a ModSecurity v3 JSON audit log
# entry into fields that are easy to aggregate in Kibana.
#
# Input:  event["transaction"] as written by libmodsecurity (SecAuditLogFormat JSON)
# Output: the same event with modsec.*, client.*, url.*, http.*, user_agent.*
#
# Loaded via:  ruby { path => "/usr/share/logstash/scripts/modsec_flatten.rb" }

SEVERITY_NAMES = {
  "0" => "EMERGENCY", "1" => "ALERT",  "2" => "CRITICAL", "3" => "ERROR",
  "4" => "WARNING",   "5" => "NOTICE", "6" => "INFO",     "7" => "DEBUG",
}.freeze
SEVERITY_ORDER = SEVERITY_NAMES.values.freeze

# Tag used by the summary rule in waf/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
SUMMARY_TAG = "crs-summary".freeze

# Keys of the summary line that are plain integers
SUMMARY_INT_KEYS = %w[
  inbound_blocking inbound_detection inbound_threshold
  outbound_blocking outbound_detection outbound_threshold
  sqli xss rfi lfi rce phpi http sess
].freeze

def register(params)
end

def header(headers, name)
  return nil unless headers.is_a?(Hash)
  key = headers.keys.find { |k| k.to_s.casecmp(name).zero? }
  key ? headers[key] : nil
end

def filter(event)
  tx = event.get("[transaction]")
  return [event] unless tx.is_a?(Hash)

  req     = tx["request"]  || {}
  resp    = tx["response"] || {}
  headers = req["headers"] || {}

  # --- Transaction level -------------------------------------------------
  event.set("[modsec][unique_id]", tx["unique_id"])
  event.set("[modsec][blocked]", tx["is_interrupted"] == true)
  event.set("[client][ip]", tx["client_ip"])
  event.set("[client][port]", tx["client_port"])
  event.set("[server][ip]", tx["host_ip"])
  event.set("[server][port]", tx["host_port"])

  event.set("[http][request][method]", req["method"])
  event.set("[http][version]", req["http_version"])
  event.set("[http][response][status_code]", resp["http_code"])

  uri = req["uri"].to_s
  path, query = uri.split("?", 2)
  event.set("[url][original]", uri)
  event.set("[url][path]", path)
  event.set("[url][query]", query) if query
  event.set("[url][domain]", req["hostname"]) if req["hostname"]

  ua = header(headers, "User-Agent")
  event.set("[user_agent][original]", ua) if ua
  referer = header(headers, "Referer")
  event.set("[http][request][referrer]", referer) if referer
  ctype = header(headers, "Content-Type")
  event.set("[http][request][content_type]", ctype) if ctype

  producer = tx["producer"] || {}
  event.set("[modsec][engine]", producer["modsecurity"])
  event.set("[modsec][connector]", producer["connector"])
  crs = (producer["components"] || []).map(&:to_s).find { |c| c.start_with?("OWASP_CRS/") }
  event.set("[modsec][crs_version]", crs.delete('"')) if crs

  # --- Rule matches ------------------------------------------------------
  ids, msgs, sevs, tags, files, data, attacks, pls, matches = [], [], [], [], [], [], [], [], []
  summary = nil
  fallback_inbound = nil

  (tx["messages"] || []).each do |m|
    d     = m["details"] || {}
    mtags = d["tags"] || []

    # The summary rule is not an alert, it is metadata about the transaction.
    if mtags.include?(SUMMARY_TAG)
      summary = m["message"].to_s
      next
    end

    id  = d["ruleId"].to_s
    sev = SEVERITY_NAMES[d["severity"].to_s] || d["severity"].to_s
    msg = m["message"].to_s

    matches << {
      "id" => id, "msg" => msg, "severity" => sev, "data" => d["data"],
      "file" => File.basename(d["file"].to_s), "line" => d["lineNumber"], "tags" => mtags,
    }

    # The blocking evaluation rules (949xxx inbound, 959xxx outbound) and the
    # correlation rules (980xxx) are not detections, they are the verdict.
    # Keep them in `matches`, but leave them out of the per-rule statistics
    # so that "top rules" and "severity" charts show real detections.
    if id.start_with?("949", "959", "980")
      score = msg[/Total Score: (\d+)/, 1]
      fallback_inbound = score.to_i if score && id.start_with?("949")
      next
    end

    ids   << id
    msgs  << msg
    sevs  << sev
    files << File.basename(d["file"].to_s)
    data  << d["data"] unless d["data"].to_s.empty?
    tags.concat(mtags)
    mtags.each do |t|
      attacks << t.sub("attack-", "") if t.start_with?("attack-")
      pls     << t.split("/").last    if t.start_with?("paranoia-level/")
    end

  end

  event.set("[modsec][rule][ids]", ids.uniq)
  event.set("[modsec][rule][messages]", msgs.uniq)
  event.set("[modsec][rule][severities]", sevs.uniq)
  event.set("[modsec][rule][tags]", tags.uniq)
  event.set("[modsec][rule][files]", files.uniq)
  event.set("[modsec][rule][data]", data)
  event.set("[modsec][rule][count]", ids.size)
  event.set("[modsec][attack]", attacks.uniq)
  event.set("[modsec][paranoia_level]", pls.uniq.sort)
  event.set("[modsec][matches]", matches)

  top = sevs.min_by { |s| SEVERITY_ORDER.index(s) || 99 }
  event.set("[modsec][rule][top_severity]", top) if top

  # --- Anomaly scores ----------------------------------------------------
  if summary
    summary.scan(/(\w+)=([\w.-]+)/).each do |key, value|
      case key
      when *SUMMARY_INT_KEYS
        event.set("[modsec][anomaly][#{key}]", value.to_i)
      when "inbound_pl"
        value.split("-").each_with_index do |v, i|
          event.set("[modsec][anomaly][inbound_pl#{i + 1}]", v.to_i)
        end
      when "blocking_pl"
        event.set("[modsec][paranoia][blocking]", value.to_i)
      when "detection_pl"
        event.set("[modsec][paranoia][detection]", value.to_i)
      end
    end
    event.set("[modsec][anomaly][source]", "summary-rule")
  elsif fallback_inbound
    # No summary rule installed: at least record the score that blocked.
    event.set("[modsec][anomaly][inbound_blocking]", fallback_inbound)
    event.set("[modsec][anomaly][source]", "blocking-rule")
  end

  # The response body is either the block page or the backend's answer.
  # Neither belongs in a log index.
  event.remove("[transaction][response][body]")

  [event]
end
