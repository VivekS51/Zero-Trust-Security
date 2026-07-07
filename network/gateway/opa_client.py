import requests

NETWORK_URL = "http://localhost:8181/v1/data/cruise/network/allow"
GDPR_URL = "http://localhost:8181/v1/data/cruise/compliance/gdpr/allow"
PCI_URL = "http://localhost:8181/v1/data/cruise/compliance/pci/allow"


def evaluate_policy(input_data):
    payload = {
        "input": input_data
    }

    network = requests.post(
        NETWORK_URL,
        json=payload,
        timeout=5
    ).json()["result"]

    gdpr = requests.post(
        GDPR_URL,
        json=payload,
        timeout=5
    ).json()["result"]

    pci = requests.post(
        PCI_URL,
        json=payload,
        timeout=5
    ).json()["result"]

    return network and gdpr and pci