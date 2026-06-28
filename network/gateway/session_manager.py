"""
Session Manager
"""

from datetime import datetime

ACTIVE_SESSIONS = {}


def create_session(username):

    ACTIVE_SESSIONS[username] = {
        "created_at": datetime.utcnow(),
        "last_seen": datetime.utcnow()
    }


def update_session(username):

    if username in ACTIVE_SESSIONS:
        ACTIVE_SESSIONS[username]["last_seen"] = datetime.utcnow()


def remove_session(username):

    ACTIVE_SESSIONS.pop(username, None)


def get_all_sessions():

    return ACTIVE_SESSIONS