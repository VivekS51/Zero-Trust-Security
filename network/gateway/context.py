"""
Request Context Builder
"""

from datetime import datetime


def build_request_context(username, resource):

    current_hour = datetime.now().hour

    working_hours = 8 <= current_hour <= 18

    return {
        "username": username,
        "resource": resource,
        "working_hours": working_hours,
        "emergency_mode": False,
        "location": "Ship Network",
        "region": "EU",
        "personal_data": True
    }