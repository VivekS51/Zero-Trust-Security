"""
OPA REST Client
Enterprise Version
"""

import requests

OPA_URL = "http://localhost:8181/v1/data/cruise/network/allow"


def evaluate_policy(input_data):
    payload = {
        "input": input_data
    }

    response = requests.post(
        OPA_URL,
        json=payload,
        timeout=5
    )

    response.raise_for_status()

    result = response.json()

    return result["result"]