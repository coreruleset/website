#!/usr/bin/env python3
"""Generate crs-dashboard.ndjson, the Kibana saved objects for the CRS
logging series.

Kibana's Lens panels are stored as rather verbose JSON. Rather than
maintaining that by hand, this script builds the data view, a saved
Discover session and a dashboard with by-value Lens panels, and writes them
as an NDJSON file that can be imported with the Saved Objects API:

    curl -X POST "http://localhost:5601/api/saved_objects/_import?overwrite=true" \
         -H "kbn-xsrf: true" --form file=@crs-dashboard.ndjson

The compose file runs that import for you (service `kibana-setup`).

Run this script again if you change the panels:

    python3 build-dashboard.py > crs-dashboard.ndjson
"""

import json
import sys

DATA_VIEW_ID = "crs-modsec-audit"
SEARCH_ID = "crs-modsec-transactions"
DASHBOARD_ID = "crs-modsec-overview"
KIBANA_VERSION = "9.5.5"

# ---------------------------------------------------------------------------
# Lens building blocks
# ---------------------------------------------------------------------------


def col_count(label="Transactions", filter_query=None):
    col = {
        "label": label,
        "customLabel": True,
        "dataType": "number",
        "operationType": "count",
        "isBucketed": False,
        "scale": "ratio",
        "sourceField": "___records___",
        "params": {"emptyAsNull": True},
    }
    if filter_query:
        col["filter"] = {"query": filter_query, "language": "kuery"}
    return col


def col_sum(field, label):
    return {
        "label": label,
        "customLabel": True,
        "dataType": "number",
        "operationType": "sum",
        "sourceField": field,
        "isBucketed": False,
        "scale": "ratio",
        "params": {"emptyAsNull": True},
    }


def col_unique(field, label, data_type="string"):
    return {
        "label": label,
        "customLabel": True,
        "dataType": "number",
        "operationType": "unique_count",
        "sourceField": field,
        "isBucketed": False,
        "scale": "ratio",
        "params": {"emptyAsNull": True},
    }


def col_max(field, label):
    return {
        "label": label,
        "customLabel": True,
        "dataType": "number",
        "operationType": "max",
        "sourceField": field,
        "isBucketed": False,
        "scale": "ratio",
        "params": {"emptyAsNull": True},
    }


def col_terms(field, label, order_col, size=10, data_type="string"):
    return {
        "label": label,
        "customLabel": True,
        "dataType": data_type,
        "operationType": "terms",
        "scale": "ordinal",
        "sourceField": field,
        "isBucketed": True,
        "params": {
            "size": size,
            "orderBy": {"type": "column", "columnId": order_col},
            "orderDirection": "desc",
            "otherBucket": False,
            "missingBucket": False,
            "parentFormat": {"id": "terms"},
            "include": [],
            "exclude": [],
            "includeIsRegex": False,
            "excludeIsRegex": False,
        },
    }


def col_date_histogram(label="@timestamp"):
    return {
        "label": label,
        "dataType": "date",
        "operationType": "date_histogram",
        "sourceField": "@timestamp",
        "isBucketed": True,
        "scale": "interval",
        "params": {"interval": "auto", "includeEmptyRows": True, "dropPartials": False},
    }


def col_filters(label, filters):
    return {
        "label": label,
        "customLabel": True,
        "dataType": "string",
        "operationType": "filters",
        "scale": "ordinal",
        "isBucketed": True,
        "params": {
            "filters": [
                {"input": {"query": q, "language": "kuery"}, "label": lbl} for lbl, q in filters
            ]
        },
    }


def lens_attributes(title, vis_type, layer_id, columns, visualization):
    """A Lens saved object's `attributes`, used by value inside a dashboard."""
    return {
        "title": title,
        "visualizationType": vis_type,
        "type": "lens",
        "references": [
            {
                "type": "index-pattern",
                "id": DATA_VIEW_ID,
                "name": f"indexpattern-datasource-layer-{layer_id}",
            }
        ],
        "state": {
            "visualization": visualization,
            "query": {"query": "", "language": "kuery"},
            "filters": [],
            "datasourceStates": {
                "formBased": {
                    "layers": {
                        layer_id: {
                            "columns": columns,
                            "columnOrder": list(columns.keys()),
                            "incompleteColumns": {},
                            "sampling": 1,
                        }
                    }
                }
            },
            "internalReferences": [],
            "adHocDataViews": {},
        },
    }


# ---------------------------------------------------------------------------
# Panels
# ---------------------------------------------------------------------------

panels = []
references = [
    {
        "name": f"{SEARCH_ID}:panel_{SEARCH_ID}",
        "type": "search",
        "id": SEARCH_ID,
    }
]


def add_lens(panel_id, title, vis_type, columns, visualization, x, y, w, h):
    layer_id = f"layer-{panel_id}"
    panels.append(
        {
            "version": KIBANA_VERSION,
            "type": "lens",
            "gridData": {"x": x, "y": y, "w": w, "h": h, "i": panel_id},
            "panelIndex": panel_id,
            "title": title,
            "embeddableConfig": {
                "attributes": lens_attributes(title, vis_type, layer_id, columns, visualization),
                "enhancements": {},
            },
        }
    )
    references.append(
        {
            "name": f"{panel_id}:indexpattern-datasource-layer-{layer_id}",
            "type": "index-pattern",
            "id": DATA_VIEW_ID,
        }
    )


def metric(panel_id, title, column, x, y, w=12, h=6, color=None):
    layer = f"layer-{panel_id}"
    vis = {"layerId": layer, "layerType": "data", "metricAccessor": "m"}
    if color:
        vis["color"] = color
    add_lens(panel_id, title, "lnsMetric", {"m": column}, vis, x, y, w, h)
    # The metric already shows its label; a panel title on top would repeat it.
    panels[-1]["embeddableConfig"]["hidePanelTitles"] = True


def pie(panel_id, title, group_col, x, y, w=16, h=12, size=8):
    layer = f"layer-{panel_id}"
    columns = {"g": group_col, "c": col_count()}
    columns["g"]["params"]["size"] = size
    vis = {
        "shape": "donut",
        "layers": [
            {
                "layerId": layer,
                "layerType": "data",
                "primaryGroups": ["g"],
                "metrics": ["c"],
                "numberDisplay": "percent",
                "categoryDisplay": "default",
                "legendDisplay": "show",
                "legendPosition": "right",
                "nestedLegend": False,
            }
        ],
    }
    add_lens(panel_id, title, "lnsPie", columns, vis, x, y, w, h)


def table(panel_id, title, group_col, x, y, w=24, h=14, extra_metrics=None):
    layer = f"layer-{panel_id}"
    columns = {"g": group_col, "c": col_count()}
    column_list = [{"columnId": "g"}, {"columnId": "c"}]
    for cid, col in (extra_metrics or {}).items():
        columns[cid] = col
        column_list.append({"columnId": cid})
    vis = {
        "layerId": layer,
        "layerType": "data",
        "columns": column_list,
        "sorting": {"columnId": "c", "direction": "desc"},
        "rowHeight": "single",
        "headerRowHeight": "single",
    }
    add_lens(panel_id, title, "lnsDatatable", columns, vis, x, y, w, h)


def bars(panel_id, title, x_col, columns_extra, accessors, x, y, w, h, series="bar_stacked", split=None):
    layer = f"layer-{panel_id}"
    columns = {"x": x_col}
    columns.update(columns_extra)
    layer_def = {
        "layerId": layer,
        "layerType": "data",
        "seriesType": series,
        "accessors": accessors,
        "xAccessor": "x",
        "position": "top",
        "showGridlines": False,
    }
    if split:
        layer_def["splitAccessor"] = split
    vis = {
        "legend": {"isVisible": True, "position": "right"},
        "valueLabels": "hide",
        "fittingFunction": "None",
        "axisTitlesVisibilitySettings": {"x": False, "yLeft": False, "yRight": True},
        "tickLabelsVisibilitySettings": {"x": True, "yLeft": True, "yRight": True},
        "labelsOrientation": {"x": 0, "yLeft": 0, "yRight": 0},
        "gridlinesVisibilitySettings": {"x": True, "yLeft": True, "yRight": True},
        "preferredSeriesType": series,
        "layers": [layer_def],
    }
    add_lens(panel_id, title, "lnsXY", columns, vis, x, y, w, h)


# Row 1: headline numbers
metric("p-total", "Transactions logged", col_count("Transactions logged"), 0, 0)
metric("p-blocked", "Blocked", col_count("Blocked", "modsec.blocked : true"), 12, 0, color="#bd271e")
metric("p-alerts", "Rule matches", col_sum("modsec.rule.count", "Rule matches"), 24, 0)
metric("p-clients", "Distinct clients", col_unique("client.ip", "Distinct clients"), 36, 0)

# Row 2: timeline + attack categories
bars(
    "p-timeline",
    "Transactions over time: blocked vs. logged only",
    col_date_histogram(),
    {
        "o": col_filters(
            "Outcome",
            [("Blocked", "modsec.blocked : true"), ("Logged only", "modsec.blocked : false")],
        ),
        "c": col_count(),
    },
    ["c"],
    0, 6, 32, 12,
    split="o",
)
pie("p-attack", "Attack categories (CRS attack-* tags)", col_terms("modsec.attack", "Category", "c"), 32, 6)

# Row 3: top rules and top URLs
table(
    "p-rules",
    "Top rules",
    col_terms("modsec.rule.ids", "Rule ID", "c", size=15),
    0, 18,
    extra_metrics={"b": col_count("Blocked", "modsec.blocked : true")},
)
table(
    "p-urls",
    "Most targeted paths",
    col_terms("url.path", "Path", "c", size=15),
    24, 18,
    extra_metrics={"b": col_count("Blocked", "modsec.blocked : true")},
)

# Row 4: clients, paranoia level, severity
bars(
    "p-clients-bar",
    "Top clients",
    col_terms("client.ip", "Client", "c", size=10, data_type="ip"),
    {"c": col_count()},
    ["c"],
    0, 32, 16, 12,
    series="bar_horizontal",
)
pie("p-pl", "Paranoia level of matched rules", col_terms("modsec.paranoia_level", "PL", "c"), 16, 32)
pie("p-sev", "Highest severity per transaction", col_terms("modsec.rule.top_severity", "Severity", "c"), 32, 32)

# Row 5: anomaly scores
score_col = col_terms("modsec.anomaly.inbound_detection", "Inbound detection score", "c", size=25, data_type="number")
score_col["params"]["orderBy"] = {"type": "alphabetical"}
score_col["params"]["orderDirection"] = "asc"
bars(
    "p-score-hist",
    "Inbound anomaly score distribution (detection PL)",
    score_col,
    {"c": col_count()},
    ["c"],
    0, 44, 24, 12,
    series="bar",
)
bars(
    "p-score-time",
    "Highest inbound score per interval: blocking PL vs. detection PL",
    col_date_histogram(),
    {
        "b": col_max("modsec.anomaly.inbound_blocking", "Blocking PL score"),
        "d": col_max("modsec.anomaly.inbound_detection", "Detection PL score"),
    },
    ["b", "d"],
    24, 44, 24, 12,
    series="line",
)

# Row 6: the raw transactions (saved Discover session, by reference)
panels.append(
    {
        "version": KIBANA_VERSION,
        "type": "search",
        "gridData": {"x": 0, "y": 56, "w": 48, "h": 18, "i": SEARCH_ID},
        "panelIndex": SEARCH_ID,
        "title": "Transactions",
        "embeddableConfig": {"enhancements": {}},
        "panelRefName": f"panel_{SEARCH_ID}",
    }
)

# ---------------------------------------------------------------------------
# Saved objects
# ---------------------------------------------------------------------------

data_view = {
    "id": DATA_VIEW_ID,
    "type": "index-pattern",
    "attributes": {
        "title": "modsec-audit-*",
        "name": "ModSecurity audit log",
        "timeFieldName": "@timestamp",
        "allowHidden": False,
        "fieldAttrs": "{}",
        "fieldFormatMap": "{}",
        "runtimeFieldMap": "{}",
        "sourceFilters": "[]",
        "fields": "[]",
    },
    "references": [],
    "managed": False,
}

# Discover sessions are stored as "tabs" since Kibana 9.x.
search = {
    "id": SEARCH_ID,
    "type": "search",
    "attributes": {
        "title": "CRS transactions",
        "description": "ModSecurity audit log entries with the CRS summary fields",
        "tabs": [
            {
                "id": "crs-modsec-transactions-tab",
                "label": "Transactions",
                "attributes": {
                    "columns": [
                        "modsec.blocked",
                        "client.ip",
                        "http.request.method",
                        "url.original",
                        "http.response.status_code",
                        "modsec.anomaly.inbound_detection",
                        "modsec.attack",
                        "modsec.rule.ids",
                    ],
                    "sort": [["@timestamp", "desc"]],
                    "grid": {},
                    "hideChart": True,
                    "isTextBasedQuery": False,
                    "kibanaSavedObjectMeta": {
                        "searchSourceJSON": json.dumps(
                            {
                                "query": {"query": "", "language": "kuery"},
                                "filter": [],
                                "indexRefName": "kibanaSavedObjectMeta.searchSourceJSON.index",
                            }
                        )
                    },
                },
            }
        ],
    },
    "references": [
        {
            "name": "kibanaSavedObjectMeta.searchSourceJSON.index",
            "type": "index-pattern",
            "id": DATA_VIEW_ID,
        }
    ],
    "managed": False,
}

dashboard = {
    "id": DASHBOARD_ID,
    "type": "dashboard",
    "attributes": {
        "title": "OWASP CRS - ModSecurity overview",
        "description": "What the WAF is seeing: blocked vs. logged transactions, top rules, attack categories, anomaly scores.",
        "panelsJSON": json.dumps(panels),
        "optionsJSON": json.dumps(
            {"useMargins": True, "syncColors": False, "syncCursor": True, "syncTooltips": False, "hidePanelTitles": False}
        ),
        "timeRestore": True,
        "timeFrom": "now-24h",
        "timeTo": "now",
        "refreshInterval": {"pause": False, "value": 30000},
        "version": 1,
        "kibanaSavedObjectMeta": {
            "searchSourceJSON": json.dumps({"query": {"query": "", "language": "kuery"}, "filter": []})
        },
    },
    "references": references,
    "managed": False,
}

# Saved object migration versions as written by Kibana 9.5. With these set,
# the import skips the migration chain (which cannot handle by-value Lens
# panels written in the current format). Bump them when Kibana changes.
MIGRATION_VERSIONS = {
    "index-pattern": "8.0.0",
    "search": "10.13.0",
    "dashboard": "10.3.0",
}

for obj in (data_view, search, dashboard):
    obj["coreMigrationVersion"] = "8.8.0"
    obj["typeMigrationVersion"] = MIGRATION_VERSIONS[obj["type"]]
    sys.stdout.write(json.dumps(obj) + "\n")
