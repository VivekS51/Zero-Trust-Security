"""Audit Logger"""

import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs") / "audit.log"


def log_event(event):

    event["timestamp"] = datetime.now().isoformat()

    with open(LOG_FILE, "a") as f:
        f.write(
            json.dumps(event)
        )
        f.write("\n")
