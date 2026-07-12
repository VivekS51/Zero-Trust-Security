import requests


OPA_BASE_URL = "http://127.0.0.1:8181"

NETWORK_URL = (
    f"{OPA_BASE_URL}/v1/data/cruise/network/allow"
)

GDPR_URL = (
    f"{OPA_BASE_URL}/v1/data/cruise/gdpr/allow"
)

PCI_URL = (
    f"{OPA_BASE_URL}/v1/data/cruise/pci/allow_payment_access"
)


def query_opa(url, policy_input, policy_name):
    """
    Query an OPA policy endpoint.

    Zero Trust behavior:
    - Network failure -> DENY
    - Invalid JSON -> DENY
    - Missing result -> DENY
    - Non-boolean result -> DENY
    - OPA HTTP error -> DENY
    """

    payload = {
        "input": policy_input
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(
            f"OPA ERROR [{policy_name}]: "
            f"{error}"
        )

        return False

    try:
        data = response.json()

    except ValueError:
        print(
            f"OPA ERROR [{policy_name}]: "
            "Invalid JSON response"
        )

        return False

    if "result" not in data:
        print(
            f"OPA ERROR [{policy_name}]: "
            "Missing result field"
        )

        return False

    result = data["result"]

    if not isinstance(result, bool):
        print(
            f"OPA ERROR [{policy_name}]: "
            f"Non-boolean result: {result!r}"
        )

        return False

    return result


def evaluate_policy(policy_input):
    """
    Evaluate Zero Trust authorization policies.

    Network segmentation is required for every resource.

    GDPR is additionally required for crew access.

    PCI-DSS is additionally required for POS access.

    Any failed or unavailable policy evaluation causes DENY.
    """

    resource = policy_input.get("resource")

    network_allowed = query_opa(
        NETWORK_URL,
        policy_input,
        "network",
    )

    if not network_allowed:
        return False

    if resource == "crew":

        gdpr_allowed = query_opa(
            GDPR_URL,
            policy_input,
            "gdpr",
        )

        if not gdpr_allowed:
            return False

    if resource == "pos":

        pci_allowed = query_opa(
            PCI_URL,
            policy_input,
            "pci",
        )

        if not pci_allowed:
            return False

    return True