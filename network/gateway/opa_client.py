import json
import subprocess


POLICY_FILE = "policies/network/network_segmentation.rego"


def evaluate_policy(input_data):

    with open("policy_input.json", "w") as f:
        json.dump(input_data, f)

    result = subprocess.run(
        [
            "opa",
            "eval",
            "-d",
            POLICY_FILE,
            "-i",
            "policy_input.json",
            "data.cruise.network.allow"
        ],
        capture_output=True,
        text=True
    )

    output = json.loads(result.stdout)

    return output["result"][0]["expressions"][0]["value"]