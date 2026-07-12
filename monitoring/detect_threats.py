import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone


ELASTICSEARCH_URL = "http://localhost:9200"
INDEX_PATTERN = "zero-trust-audit-*"
ALERT_INDEX = "zero-trust-security-alerts"
DENY_THRESHOLD = 3


def elasticsearch_request(url, payload, method="POST"):
    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method=method,
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def search_denied_users():
    query = {
        "size": 0,
        "query": {
            "term": {
                "decision.keyword": "DENY"
            }
        },
        "aggs": {
            "denied_users": {
                "terms": {
                    "field": "user.keyword",
                    "size": 100
                }
            }
        }
    }

    url = f"{ELASTICSEARCH_URL}/{INDEX_PATTERN}/_search"

    return elasticsearch_request(url, query)


def detect_threats(search_result):
    buckets = (
        search_result
        .get("aggregations", {})
        .get("denied_users", {})
        .get("buckets", [])
    )

    threats = []

    for bucket in buckets:
        if bucket["doc_count"] >= DENY_THRESHOLD:
            threats.append({
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "security_alert",
                "alert_type": "repeated_access_denials",
                "severity": "HIGH",
                "user": bucket["key"],
                "deny_count": bucket["doc_count"],
                "threshold": DENY_THRESHOLD,
                "project": "zero-trust-cruise-platform",
            })

    return threats


def persist_alert(alert):
    # Deterministic document ID prevents duplicate alert documents
    # when the detector runs repeatedly for the same user and rule.
    document_id = (
        f"{alert['alert_type']}-"
        f"{alert['user']}"
    )

    url = (
    f"{ELASTICSEARCH_URL}/"
    f"{ALERT_INDEX}/_doc/"
    f"{document_id}?refresh=wait_for"
    )

    return elasticsearch_request(
        url,
        alert,
        method="PUT",
    )


def main():
    print("=" * 60)
    print("Zero Trust Cruise Platform - Threat Detector")
    print("=" * 60)

    try:
        result = search_denied_users()

        threats = detect_threats(result)

        if not threats:
            print("STATUS: No threats detected.")
            return 0

        print(f"STATUS: {len(threats)} threat(s) detected.")

        for threat in threats:
            result = persist_alert(threat)

            print(json.dumps(threat, indent=2))

            print(
                "ALERT INDEXED:",
                result.get("_index"),
                result.get("result"),
            )

        return 2

    except urllib.error.URLError as error:
        print(
            f"ERROR: Cannot connect to Elasticsearch: {error}"
        )
        return 1

    except Exception as error:
        print(
            f"ERROR: Threat detection failed: {error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())