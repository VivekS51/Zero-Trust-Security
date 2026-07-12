import json
from pathlib import Path
from threading import Lock


BLOCKLIST_FILE = (
    Path(__file__).resolve().parent
    / "blocked_identities.json"
)

_file_lock = Lock()


def _load_blocklist():
    """
    Load blocked identities from persistent JSON storage.
    """

    if not BLOCKLIST_FILE.exists():
        return []

    try:
        with BLOCKLIST_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

    except (
        json.JSONDecodeError,
        OSError,
    ):
        pass

    return []


def _save_blocklist(blocked_identities):
    """
    Persist blocked identities to JSON storage.
    """

    with BLOCKLIST_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            blocked_identities,
            file,
            indent=2,
        )


def block_identity(username, reason="security_threat"):
    """
    Add an identity to the blocklist.

    Returns True if newly blocked.
    Returns False if already blocked.
    """

    if not username:
        return False

    with _file_lock:

        blocked_identities = _load_blocklist()

        existing_users = {
            item["username"]
            for item in blocked_identities
            if isinstance(item, dict)
            and "username" in item
        }

        if username in existing_users:
            return False

        blocked_identities.append({
            "username": username,
            "reason": reason,
        })

        _save_blocklist(blocked_identities)

    return True


def is_identity_blocked(username):
    """
    Check whether an identity is blocked.
    """

    blocked_identities = _load_blocklist()

    return any(
        isinstance(item, dict)
        and item.get("username") == username
        for item in blocked_identities
    )


def unblock_identity(username):
    """
    Remove an identity from the blocklist.

    Returns True if removed.
    """

    with _file_lock:

        blocked_identities = _load_blocklist()

        updated_blocklist = [
            item
            for item in blocked_identities
            if not (
                isinstance(item, dict)
                and item.get("username") == username
            )
        ]

        if len(updated_blocklist) == len(blocked_identities):
            return False

        _save_blocklist(updated_blocklist)

    return True


def get_blocked_identities():
    """
    Return all blocked identities.
    """

    return _load_blocklist()