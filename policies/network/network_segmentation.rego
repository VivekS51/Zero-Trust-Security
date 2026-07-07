package cruise.network

import rego.v1

default allow := false

allow if {

    input.required_group in input.group_membership

    input.device.managed == true

    input.device.encrypted == true

    input.device.risk == "Low"

    input.request.working_hours == true

    input.request.location == "Ship Network"

    input.request.emergency_mode == false

    input.risk.level == "Low"

    input.risk.score <= 25
}