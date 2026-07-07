"""
OPA REST Service
"""

from typing import Any

import requests


OPA_BASE_URL = "http://127.0.0.1:8181/v1/data"

ALLOWED_POLICY_PATHS = {
    "cruise/network/allow",
    "cruise/gdpr/allow_pii_export",
    "cruise/pci/allow_payment_access",
}


def evaluate_opa_policy(
    policy_path: str,
    input_data: dict[str, Any]
):
    if policy_path not in ALLOWED_POLICY_PATHS:
        raise ValueError("Unsupported policy path")

    url = f"{OPA_BASE_URL}/{policy_path}"

    response = requests.post(
        url,
        json={
            "input": input_data
        },
        timeout=5
    )

    response.raise_for_status()

    result = response.json()

    if "result" not in result:
        raise RuntimeError(
            "OPA response does not contain a result"
        )

    return result["result"]