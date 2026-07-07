"""
Device Trust Simulator
"""


def get_device_context(username):

    devices = {

        "officer.smith": {
            "managed": True,
            "encrypted": True,
            "os": "Windows 11",
            "risk": "Low"
        },

        "engineer.diaz": {
            "managed": True,
            "encrypted": True,
            "os": "Ubuntu",
            "risk": "Low"
        },

        "staff.nguyen": {
            "managed": True,
            "encrypted": False,
            "os": "Windows 10",
            "risk": "Medium"
        },

        "guest.test": {
            "managed": False,
            "encrypted": False,
            "os": "Android",
            "risk": "High"
        },

        "admin.patel": {
            "managed": True,
            "encrypted": True,
            "os": "Windows 11",
            "risk": "Low"
        }

    }

    return devices.get(
        username,
        {
            "managed": False,
            "encrypted": False,
            "risk": "High"
        }
    )