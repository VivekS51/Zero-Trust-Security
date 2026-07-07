"""Authorization Context Builder"""

from device import get_device_context
from risk import get_user_risk
from compliance import get_user_compliance
from context import build_request_context
from entra import get_user_groups


GROUP_MAPPING = {
    "bridge": "Bridge-Systems-Access",
    "pos": "POS-Access",
    "crew": "Engine-OT-Access"
}

def build_authorization_context(payload, resource):
    username = payload["username"]

    device = get_device_context(username)
    risk = get_user_risk(username)
    compliance = get_user_compliance(username)
    request_context = build_request_context(
        username,
        resource
    )

    return {
        "source_zone": resource,
        "target_zone": resource,
        "group_membership": get_user_groups(username),
        "required_group": GROUP_MAPPING[resource],
        "device": device,
        "request": request_context,
        "risk": risk,
        "user": compliance
    }
