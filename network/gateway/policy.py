"""
Simple RBAC policy engine.

Later this will be replaced by OPA.
"""

ACCESS_POLICY = {

    "Officer": [
        "bridge",
        "crew"
    ],

    "Engineer": [
        "crew"
    ],

    "Staff": [
        "pos"
    ],

    "Admin": [
        "bridge",
        "crew",
        "pos"
    ]
}


def authorize(role, resource):

    allowed = ACCESS_POLICY.get(role, [])

    return resource in allowed