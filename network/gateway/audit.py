"""
Zero Trust Audit Logger

Writes structured audit events to:
1. Local JSON-lines audit log
2. Logstash over TCP

SIEM delivery failures must not interrupt authorization requests.
"""

import json
import socket
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "audit.log"

LOGSTASH_HOST = "127.0.0.1"
LOGSTASH_PORT = 5000
LOGSTASH_TIMEOUT_SECONDS = 1.0


def _prepare_event(event):
    audit_event = event.copy()

    audit_event["timestamp"] = datetime.now(
        timezone.utc
    ).isoformat()

    audit_event["event_type"] = audit_event.get(
        "event_type",
        "authorization_audit"
    )

    audit_event["source"] = audit_event.get(
        "source",
        "flask-gateway"
    )

    return audit_event


def _write_local(event):
    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as log_file:
        log_file.write(
            json.dumps(event)
        )
        log_file.write("\n")


def _send_to_logstash(event):
    message = (
        json.dumps(event) + "\n"
    ).encode("utf-8")

    with socket.create_connection(
        (
            LOGSTASH_HOST,
            LOGSTASH_PORT
        ),
        timeout=LOGSTASH_TIMEOUT_SECONDS
    ) as connection:

        connection.sendall(message)


def log_event(event):
    audit_event = _prepare_event(event)

    _write_local(audit_event)

    try:
        _send_to_logstash(audit_event)

    except (
        OSError,
        socket.timeout
    ):
        # Local audit logging already succeeded.
        # SIEM unavailability must not break authorization.
        pass