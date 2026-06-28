package cruise.network

import rego.v1

default allow := false

# Hard deny: Guest WiFi can never access Bridge
deny_guest_to_bridge if {
    input.source_zone == "guest_wifi"
    input.target_zone == "bridge_navigation"
}

# Hard deny: Guest WiFi can never access POS
deny_guest_to_pos if {
    input.source_zone == "guest_wifi"
    input.target_zone == "pos_payments"
}

# Hard deny: Guest WiFi can never access Engine
deny_guest_to_engine if {
    input.source_zone == "guest_wifi"
    input.target_zone == "engine_ot"
}

hard_denied if {
    deny_guest_to_bridge
}

hard_denied if {
    deny_guest_to_pos
}

hard_denied if {
    deny_guest_to_engine
}

allow if {
    not hard_denied
    input.required_group in input.group_membership
}