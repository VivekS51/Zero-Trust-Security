package cruise.pci

import rego.v1

default allow_payment_access := false

allow_payment_access if {
    input.device.managed == true
    input.device.encrypted == true
    input.user.pci_trained == true
    input.user.mfa == true
}

decision_reason := "Allowed: PCI requirements satisfied" if {
    allow_payment_access
}

decision_reason := "Denied: PCI compliance requirements not met" if {
    not allow_payment_access
}