package cruise.gdpr

import rego.v1

default allow_pii_export := false

eu_waters := {
    "FR",
    "IT",
    "ES",
    "GR",
    "DE",
    "NL",
    "PT",
    "MT",
    "CY"
}

requires_consent if {
    input.data_subject_region == "EU"
}

requires_consent if {
    input.ship_location in eu_waters
    input.data_type == "passenger_PII"
}

allow_pii_export if {
    requires_consent
    input.consent_flag == true
}

allow_pii_export if {
    not requires_consent
}

decision_reason := "Allowed: GDPR consent verified" if {
    allow_pii_export
    requires_consent
}

decision_reason := "Allowed: GDPR not applicable to this request" if {
    allow_pii_export
    not requires_consent
}

decision_reason := "Denied: GDPR consent required but not present" if {
    not allow_pii_export
}