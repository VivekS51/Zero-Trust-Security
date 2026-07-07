package cruise.gdpr_test

import rego.v1

test_gdpr_denies_without_consent if {

    not data.cruise.gdpr.allow_pii_export with input as {
        "ship_location": "IT",
        "data_type": "passenger_PII",
        "data_subject_region": "US",
        "consent_flag": false
    }
}