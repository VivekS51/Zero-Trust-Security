package cruise.network_test

import rego.v1

test_allow_network if {

    data.cruise.network.allow with input as {
        "source_zone": "bridge",
        "target_zone": "bridge",
        "required_group": "Bridge-Systems-Access",
        "group_membership": [
            "Bridge-Systems-Access"
        ],
        "device": {
            "managed": true,
            "encrypted": true,
            "risk": "Low"
        },
        "request": {
            "working_hours": true,
            "location": "Ship Network",
            "emergency_mode": false
        },
        "risk": {
            "level": "Low",
            "score": 5
        }
    }
}