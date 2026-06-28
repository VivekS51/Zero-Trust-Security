"""
Reverse Proxy
"""

import requests

from config import SERVICES


def forward_request(service):

    if service not in SERVICES:

        return {
            "error": "Unknown Service"
        }, 404

    response = requests.get(
        SERVICES[service]
    )

    return response.json(), response.status_code