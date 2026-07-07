"""Compliance Context"""


def get_user_compliance(username):
    users = {
        "officer.smith": {
            "gdpr_trained": True,
            "pci_trained": False
        },
        "engineer.diaz": {
            "gdpr_trained": True,
            "pci_trained": False
        },
        "staff.nguyen": {
            "gdpr_trained": True,
            "pci_trained": True
        },
        "admin.patel": {
            "gdpr_trained": True,
            "pci_trained": True
        },
        "guest.test": {
            "gdpr_trained": False,
            "pci_trained": False
        }
    }

    return users.get(
        username,
        {
            "gdpr_trained": False,
            "pci_trained": False
        }
    )
