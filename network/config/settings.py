"""
Global configuration for the Zero Trust Cruise Platform.
"""

# ----------------------------
# Application Ports
# ----------------------------

BRIDGE_PORT = 5001
POS_PORT = 5002
CREW_ADMIN_PORT = 5003

# ----------------------------
# Security
# ----------------------------

JWT_SECRET = "change-this-in-production"

TOKEN_EXPIRY_MINUTES = 60

# ----------------------------
# Satellite Simulation
# ----------------------------

BASE_LATENCY_MS = 800
LATENCY_JITTER_MS = 200
DROPOUT_PROBABILITY = 0.02
DROPOUT_DURATION_SECONDS = 45

# ----------------------------
# Offline Cache
# ----------------------------

LOCAL_POLICY_CACHE_SECONDS = 120

# ----------------------------
# Logging
# ----------------------------

LOG_LEVEL = "INFO"