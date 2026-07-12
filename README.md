# Zero Trust Cruise Platform

A security-focused cloud and network simulation that implements Zero Trust Architecture for a cruise ship IT environment.

The platform demonstrates identity-based authentication, policy-driven authorization, continuous access verification, centralized security monitoring, automated threat detection, and automated incident response.

The system follows the core Zero Trust principle:

> Never Trust, Always Verify.

## Project Overview

Modern cruise ships operate complex distributed IT environments containing navigation systems, crew administration services, point-of-sale systems, guest networks, IoT devices, and cloud infrastructure.

Traditional perimeter-based security models are insufficient for protecting these environments.

The Zero Trust Cruise Platform demonstrates how Zero Trust security controls can be applied to a simulated cruise ship infrastructure.

Every request must:

1. Authenticate using identity credentials.
2. Present a valid JWT access token.
3. Pass automated incident-response blocklist enforcement.
4. Build a contextual authorization request.
5. Be evaluated by Open Policy Agent.
6. Generate centralized security audit events.
7. Be forwarded to the backend only when authorized.

Security events are processed through an ELK-based SIEM pipeline and analyzed by an automated threat detection system.

## Architecture

```text
                         USER / CLIENT
                               |
                               v
                     +-------------------+
                     |   Flask Gateway   |
                     |      :8000        |
                     +-------------------+
                               |
                  +------------+-------------+
                  |                          |
                  v                          v
         +------------------+       +------------------+
         | JWT Authentication|       | Identity        |
         | & Token Validation|       | Blocklist Check |
         +------------------+       +------------------+
                  |                          |
                  +------------+-------------+
                               |
                               v
                  +--------------------------+
                  | Authorization Context    |
                  | User + Role + Device +   |
                  | Risk + Resource          |
                  +--------------------------+
                               |
                               v
                     +------------------+
                     | Open Policy Agent|
                     |      (OPA)       |
                     +------------------+
                               |
                        ALLOW / DENY
                               |
                  +------------+-------------+
                  |                          |
               ALLOW                       DENY
                  |                          |
                  v                          v
         +------------------+       +------------------+
         | Backend Services |       | Access Rejected  |
         | Bridge / POS /   |       | HTTP 403         |
         | Crew             |       +------------------+
         +------------------+
                  |
                  +------------------+
                                     |
                                     v
                           +------------------+
                           |   Audit Events   |
                           +------------------+
                                     |
                                     v
                           +------------------+
                           |    Logstash      |
                           | TCP / UDP :5000  |
                           +------------------+
                                     |
                                     v
                           +------------------+
                           | Elasticsearch    |
                           |      :9200       |
                           +------------------+
                                     |
                    +----------------+----------------+
                    |                                 |
                    v                                 v
          +--------------------+           +--------------------+
          | Kibana Dashboard   |           | Threat Detector    |
          |      :5601         |           | detect_threats.py  |
          +--------------------+           +--------------------+
                                                     |
                                                     v
                                           +--------------------+
                                           | Security Alerts    |
                                           | Elasticsearch Index|
                                           +--------------------+
                                                     |
                                                     v
                                           +--------------------+
                                           | Automated Incident |
                                           | Response            |
                                           +--------------------+
                                                     |
                                                     v
                                           +--------------------+
                                           | Identity Blocklist |
                                           +--------------------+
                                                     |
                                                     +----> Gateway Enforcement
```

## Core Security Features

### JWT Authentication

Users authenticate through the Flask API Gateway.

After successful authentication, the gateway generates a JWT token containing identity information such as username and role.

Protected resources require:

```text
Authorization: Bearer <JWT_TOKEN>
```

Invalid, missing, and expired tokens are rejected.

### Zero Trust Authorization Context

Every protected request generates a contextual authorization request containing information such as:

```json
{
  "username": "officer.smith",
  "role": "Officer",
  "resource": "bridge",
  "device": {
    "managed": true,
    "encrypted": true,
    "os": "Windows 11"
  },
  "risk": {
    "score": 10,
    "level": "Low"
  }
}
```

Authorization decisions are not based only on network location.

The system evaluates identity, role, device posture, risk, and requested resource.

### Policy-Based Authorization with OPA

Open Policy Agent is used as the Policy Decision Point.

OPA evaluates authorization context against Rego security policies.

Implemented policy areas include:

- Network access control.
- PCI-related authorization controls.
- GDPR-related consent controls.

Policy tests can be executed using:

```powershell
opa test policies -v
```

Expected result:

```text
PASS: 3/3
```

### API Gateway Enforcement

The Flask Gateway acts as the Policy Enforcement Point.

Protected resources include:

```text
/bridge
/pos
/crew
```

The gateway performs:

```text
Request
   |
   v
JWT Verification
   |
   v
Automated Blocklist Enforcement
   |
   v
Authorization Context Creation
   |
   v
OPA Policy Evaluation
   |
   +------ DENY ------> HTTP 403
   |
   v
ALLOW
   |
   v
Backend Request Forwarding
```

### Centralized Security Audit Logging

The gateway generates security events for:

- Authentication events.
- Authorization requests.
- Authorization decisions.
- OPA evaluation failures.
- Automated incident-response enforcement.

Audit events are forwarded to Logstash.

Example:

```json
{
  "event_type": "authorization_decision",
  "user": "officer.smith",
  "resource": "bridge",
  "decision": "ALLOW",
  "source": "flask-gateway"
}
```

### ELK SIEM Monitoring

The project uses:

- Elasticsearch 9.2.6
- Logstash 9.2.6
- Kibana 9.2.6

Docker Compose manages the SIEM infrastructure.

Start the stack:

```powershell
docker compose up -d
```

Verify services:

```powershell
docker compose ps
```

Service endpoints:

```text
Elasticsearch: http://localhost:9200
Kibana:        http://localhost:5601
Logstash API:  http://localhost:9600
Logstash TCP:  localhost:5000
Logstash UDP:  localhost:5000
```

### Kibana Security Dashboard

The project includes a Kibana dashboard for visual security monitoring.

Dashboard:

```text
Zero Trust Cruise Security Dashboard
```

Visualizations include:

- ALLOW vs DENY Decisions.
- Authorization Events by Resource.
- Average Risk Score by Resource.

The exported Kibana saved objects are stored in:

```text
siem/kibana/zero-trust-cruise-security-dashboard.ndjson
```

### Automated Threat Detection

The threat detection engine analyzes Elasticsearch audit events.

Run:

```powershell
python monitoring\detect_threats.py
```

The current detection rule identifies repeated authorization denials.

Example alert:

```json
{
  "event_type": "security_alert",
  "alert_type": "repeated_access_denials",
  "severity": "HIGH",
  "user": "intruder.user",
  "deny_count": 5,
  "threshold": 3,
  "project": "zero-trust-cruise-platform"
}
```

Detected alerts are indexed into:

```text
zero-trust-security-alerts
```

Deterministic document identifiers prevent duplicate alerts for the same detection condition.

### Automated Incident Response

High-severity repeated-access-denial alerts trigger automated incident response.

The offending identity is added to:

```text
incident_response/blocked_identities.json
```

Example:

```json
[
  {
    "username": "intruder.user",
    "reason": "repeated_access_denials"
  }
]
```

The Flask Gateway checks the blocklist:

```text
Before Login Token Issuance
          +
Before OPA Policy Evaluation
```

Blocked identities receive:

```text
HTTP/1.1 403 FORBIDDEN
```

Example response:

```json
{
  "error": "Access denied",
  "reason": "Identity blocked by automated incident response"
}
```

This creates a complete security feedback loop:

```text
REQUEST
   |
   v
AUTHENTICATION
   |
   v
ZERO TRUST AUTHORIZATION
   |
   v
OPA POLICY DECISION
   |
   v
AUDIT LOGGING
   |
   v
LOGSTASH
   |
   v
ELASTICSEARCH
   |
   v
THREAT DETECTION
   |
   v
SECURITY ALERT
   |
   v
AUTOMATED INCIDENT RESPONSE
   |
   v
IDENTITY BLOCKING
   |
   +-----------> FUTURE REQUESTS DENIED
```

## Automated Testing

The project contains OPA policy tests and Flask Gateway integration tests.

Run OPA tests:

```powershell
opa test policies -v
```

Run gateway integration tests:

```powershell
python .\network\gateway\test_gateway_integration.py
```

The gateway integration test suite verifies:

- Gateway health endpoint.
- Missing authorization header rejection.
- Invalid token rejection.
- Blocked identity enforcement.
- Blocklist enforcement before OPA evaluation.
- OPA authorization denial.
- OPA service failure handling.
- Authorized backend request forwarding.

Verified result:

```text
Ran 7 tests

OK
```

## Project Structure

```text
zerotrust-cruise-platform/
|
|-- docs/
|
|-- incident_response/
|   |-- blocklist.py
|   `-- blocked_identities.json
|
|-- monitoring/
|   `-- detect_threats.py
|
|-- network/
|   |-- apps/
|   |-- config/
|   |-- gateway/
|   |   |-- app.py
|   |   |-- audit.py
|   |   |-- auth.py
|   |   |-- authorization_context.py
|   |   |-- opa_client.py
|   |   |-- proxy.py
|   |   |-- routes.py
|   |   |-- session_manager.py
|   |   |-- test_gateway_integration.py
|   |   `-- user_store.py
|   |
|   |-- simulation/
|   `-- tests/
|
|-- policies/
|   |-- tests/
|   `-- Rego policy files
|
|-- siem/
|   |-- kibana/
|   |   `-- zero-trust-cruise-security-dashboard.ndjson
|   |
|   `-- logstash/
|       `-- pipeline/
|           `-- logstash.conf
|
|-- docker-compose.yml
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| API Gateway | Flask |
| Authentication | JWT |
| Policy Engine | Open Policy Agent |
| Policy Language | Rego |
| SIEM Pipeline | Logstash |
| Search and Security Analytics | Elasticsearch |
| Visualization | Kibana |
| Containerization | Docker and Docker Compose |
| Cloud Platform | Microsoft Azure |
| Testing | Python unittest and OPA tests |
| Version Control | Git and GitHub |

## Running the Project

### 1. Clone the Repository

```powershell
git clone <repository-url>

cd zerotrust-cruise-platform
```

### 2. Create a Python Virtual Environment

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file containing the required secrets and configuration.

Do not commit `.env` files or credentials to Git.

### 5. Start the ELK SIEM Stack

```powershell
docker compose up -d
```

### 6. Verify Elasticsearch

```powershell
Invoke-RestMethod http://localhost:9200/_cluster/health
```

### 7. Verify Logstash

```powershell
Invoke-RestMethod http://localhost:9600/_node/pipelines
```

### 8. Run OPA Policy Tests

```powershell
opa test policies -v
```

### 9. Start the API Gateway

```powershell
python .\network\gateway\app.py
```

Gateway:

```text
http://127.0.0.1:8000
```

### 10. Run Gateway Integration Tests

Open another terminal:

```powershell
python .\network\gateway\test_gateway_integration.py
```

### 11. Run Threat Detection

```powershell
python .\monitoring\detect_threats.py
```

### 12. Open Kibana

Open:

```text
http://localhost:5601
```

Import the saved objects if required from:

```text
siem/kibana/zero-trust-cruise-security-dashboard.ndjson
```

## Verification Commands

```powershell
git status

python -m compileall `
    .\network\gateway `
    .\monitoring `
    .\incident_response

opa test policies -v

python .\network\gateway\test_gateway_integration.py

docker compose ps

Invoke-RestMethod http://localhost:9200/_cluster/health

Invoke-RestMethod http://localhost:9600/_node/pipelines

Invoke-RestMethod "http://localhost:9200/zero-trust-audit-*/_count"

Invoke-RestMethod "http://localhost:9200/zero-trust-security-alerts/_count"

Get-Content .\incident_response\blocked_identities.json

Test-Path .\siem\kibana\zero-trust-cruise-security-dashboard.ndjson
```

## Security Principles Demonstrated

The project demonstrates:

- Never Trust, Always Verify.
- Explicit authentication and authorization.
- Least-privilege access control.
- Policy-as-Code.
- Context-aware authorization.
- Device posture evaluation.
- Risk-based access decisions.
- Centralized security telemetry.
- Continuous security monitoring.
- Automated threat detection.
- Automated incident response.
- Identity containment.
- Security event visualization.
- Testable security controls.

## Future Improvements

Potential improvements include:

- Microsoft Entra ID integration.
- Azure Key Vault for secret management.
- Azure Monitor and Microsoft Sentinel integration.
- Mutual TLS between internal services.
- Dynamic device posture collection.
- Risk scoring based on historical behavior.
- Additional threat detection rules.
- Automated token revocation.
- Network micro-segmentation.
- Kubernetes deployment.
- CI/CD security testing.
- Infrastructure as Code using Terraform or Bicep.
- Production WSGI deployment.
- TLS for gateway and SIEM communication.

## Disclaimer

This project is an educational and simulated Zero Trust security environment.

It is not intended for direct production deployment without additional security hardening, secret management, TLS configuration, high availability, and operational controls.
