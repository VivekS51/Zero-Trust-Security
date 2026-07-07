"""
Risk Engine
"""


def get_user_risk(username):

    risk_scores = {

        "officer.smith": {
            "score": 5,
            "level": "Low"
        },

        "engineer.diaz": {
            "score": 15,
            "level": "Low"
        },

        "staff.nguyen": {
            "score": 55,
            "level": "Medium"
        },

        "guest.test": {
            "score": 95,
            "level": "High"
        },

        "admin.patel": {
            "score": 10,
            "level": "Low"
        }

    }

    return risk_scores.get(
        username,
        {
            "score": 100,
            "level": "High"
        }
    )