"""Microsoft Entra ID Simulator"""

GROUPS = {
    "officer.smith": [
        "Bridge-Systems-Access"
    ],
    "engineer.diaz": [
        "Engine-OT-Access"
    ],
    "staff.nguyen": [
        "POS-Access"
    ],
    "admin.patel": [
        "Bridge-Systems-Access",
        "Engine-OT-Access",
        "POS-Access",
        "IT-Admin-Access"
    ],
    "guest.test": [
        "Guest-Wifi-Only"
    ]
}


def get_user_groups(username):
    return GROUPS.get(
        username,
        []
    )
