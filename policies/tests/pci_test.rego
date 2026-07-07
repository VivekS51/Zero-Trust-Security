package cruise.pci_test

import rego.v1

test_pci_allows_compliant_user if {

    data.cruise.pci.allow_payment_access with input as {
        "device": {
            "managed": true,
            "encrypted": true
        },
        "user": {
            "pci_trained": true,
            "mfa": true
        }
    }
}