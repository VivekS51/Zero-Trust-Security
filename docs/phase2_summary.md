# Phase 2 – Identity & Access Management

## Azure Resources

Subscription:
Azure for Students

Resource Group:
zerotrust-rg

Tenant:
vivekbytesoutlook.onmicrosoft.com

---

## Microsoft Entra Users

Officer Smith

Engineer Diaz

Staff Nguyen

Admin Patel

Guest Test

BreakGlass Emergency

---

## Security Groups

Bridge-Systems-Access

Engine-OT-Access

POS-Access

IT-Admin-Access

Guest-Wifi-Only

---

## Zero Trust Identity Controls

- Microsoft Entra ID
- Security Defaults Enabled
- MFA enforced through Security Defaults
- RBAC through Security Groups
- Least Privilege
- Break Glass Account

---

## Notes

Microsoft Entra ID Free does not support Conditional Access.

Therefore device compliance and Conditional Access will be implemented in later phases using:

- Open Policy Agent (OPA)
- Authorization API
- Local Device Registry
- Policy Engine