from network.gateway.opa_client import evaluate_policy

input_data = {
    "source_zone": "bridge_navigation",
    "target_zone": "bridge_navigation",
    "group_membership": [
        "Bridge-Systems-Access"
    ],
    "required_group": "Bridge-Systems-Access"
}

print(evaluate_policy(input_data))