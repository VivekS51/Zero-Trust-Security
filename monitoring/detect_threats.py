import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests


# ============================================================
# PROJECT PATH SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from incident_response.blocklist import block_identity


# ============================================================
# CONFIGURATION
# ============================================================

ELASTICSEARCH_URL = "http://localhost:9200"

AUDIT_INDEX = "zero-trust-audit-*"

ALERT_INDEX = "zero-trust-security-alerts"

DENIAL_THRESHOLD = 3

REQUEST_TIMEOUT = 10


# ============================================================
# ELASTICSEARCH HELPERS
# ============================================================

def check_elasticsearch():
    """
    Verify that Elasticsearch is reachable.
    """

    try:
        response = requests.get(
            ELASTICSEARCH_URL,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return True

    except requests.RequestException as error:
        print(
            "ERROR: Elasticsearch is unavailable:",
            error,
        )

        return False


def search_repeated_denials():
    """
    Search authorization events and identify users whose
    DENY count meets or exceeds the configured threshold.
    """

    query = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {
                        "term": {
                            "event_type.keyword":
                                "authorization_decision"
                        }
                    },
                    {
                        "term": {
                            "decision.keyword": "DENY"
                        }
                    }
                ]
            }
        },
        "aggs": {
            "users": {
                "terms": {
                    "field": "user.keyword",
                    "size": 100
                },
                "aggs": {
                    "threat_filter": {
                        "bucket_selector": {
                            "buckets_path": {
                                "deny_count": "_count"
                            },
                            "script":
                                f"params.deny_count >= "
                                f"{DENIAL_THRESHOLD}"
                        }
                    }
                }
            }
        }
    }

    try:
        response = requests.post(
            f"{ELASTICSEARCH_URL}/"
            f"{AUDIT_INDEX}/_search",
            json=query,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        buckets = (
            response
            .json()
            .get("aggregations", {})
            .get("users", {})
            .get("buckets", [])
        )

        return buckets

    except requests.RequestException as error:
        print(
            "ERROR: Failed to search audit events:",
            error,
        )

        return []


# ============================================================
# ALERT CREATION
# ============================================================

def create_alert(username, deny_count):
    """
    Create a normalized security alert.
    """

    return {
        "@timestamp":
            datetime.now(timezone.utc).isoformat(),

        "event_type":
            "security_alert",

        "alert_type":
            "repeated_access_denials",

        "severity":
            "HIGH",

        "user":
            username,

        "deny_count":
            deny_count,

        "threshold":
            DENIAL_THRESHOLD,

        "project":
            "zero-trust-cruise-platform",
    }


def create_document_id(alert):
    """
    Create a deterministic Elasticsearch document ID.

    Repeated detector executions update the same alert instead
    of creating duplicate alert documents.
    """

    identity = (
        f"{alert['alert_type']}:"
        f"{alert['user']}"
    )

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()


# ============================================================
# ALERT INDEXING
# ============================================================

def index_alert(alert):
    """
    Store or update the security alert in Elasticsearch.
    """

    document_id = create_document_id(alert)

    url = (
        f"{ELASTICSEARCH_URL}/"
        f"{ALERT_INDEX}/_doc/"
        f"{document_id}"
        f"?refresh=wait_for"
    )

    try:
        response = requests.put(
            url,
            json=alert,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        result = response.json().get(
            "result",
            "unknown",
        )

        print(
            f"ALERT INDEXED: "
            f"{ALERT_INDEX} {result}"
        )

        return True

    except requests.RequestException as error:
        print(
            "ERROR: Failed to index alert:",
            error,
        )

        return False


# ============================================================
# AUTOMATED INCIDENT RESPONSE
# ============================================================

def execute_incident_response(alert):
    """
    Automatically block the identity associated with a
    detected security threat.
    """

    username = alert.get("user")

    if not username:
        print(
            "INCIDENT RESPONSE: "
            "Alert does not contain a username"
        )

        return False

    reason = alert.get(
        "alert_type",
        "security_threat",
    )

    newly_blocked = block_identity(
        username,
        reason,
    )

    if newly_blocked:

        print(
            f"INCIDENT RESPONSE: "
            f"{username} automatically blocked"
        )

    else:

        print(
            f"INCIDENT RESPONSE: "
            f"{username} already blocked"
        )

    return True


# ============================================================
# THREAT DETECTION
# ============================================================

def detect_threats():
    """
    Execute threat detection and return generated alerts.
    """

    denial_buckets = search_repeated_denials()

    alerts = []

    for bucket in denial_buckets:

        username = bucket.get("key")

        deny_count = bucket.get(
            "doc_count",
            0,
        )

        alert = create_alert(
            username,
            deny_count,
        )

        alerts.append(alert)

    return alerts


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)

    print(
        "Zero Trust Cruise Platform - Threat Detector"
    )

    print("=" * 60)

    if not check_elasticsearch():
        return

    alerts = detect_threats()

    if not alerts:

        print(
            "STATUS: No threats detected."
        )

        return

    print(
        f"STATUS: {len(alerts)} threat(s) detected."
    )

    for alert in alerts:

        print(
            json.dumps(
                alert,
                indent=2,
            )
        )

        indexed = index_alert(alert)

        if indexed:

            execute_incident_response(alert)

        else:

            print(
                "INCIDENT RESPONSE SKIPPED: "
                "Alert indexing failed"
            )


if __name__ == "__main__":
    main()