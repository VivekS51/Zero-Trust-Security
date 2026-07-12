from flask import Blueprint
from flask import jsonify
from flask import request

from authorization_context import build_authorization_context

from auth import create_token
from auth import verify_token

from session_manager import create_session

from user_store import authenticate

from proxy import forward_request

from opa_client import evaluate_policy

from audit import log_event

from incident_response.blocklist import is_identity_blocked


gateway = Blueprint(
    "gateway",
    __name__,
)


@gateway.get("/")
def home():

    return jsonify({
        "project": "Zero Trust Cruise Platform",
        "gateway": "ONLINE",
        "version": "1.0",
    })


@gateway.post("/login")
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body missing",
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required",
        }), 400

    user = authenticate(
        username,
        password,
    )

    if not user:
        return jsonify({
            "error": "Invalid username or password",
        }), 401

    # Prevent blocked identities from obtaining new sessions.

    if is_identity_blocked(user["username"]):

        log_event({
            "event_type":
                "incident_response_enforcement",

            "user":
                user["username"],

            "resource":
                "login",

            "decision":
                "DENY",

            "reason":
                "identity_blocked",

            "source":
                "flask-gateway",
        })

        return jsonify({
            "error": "Login denied",
            "reason":
                "Identity blocked by automated incident response",
        }), 403

    token = create_token(
        username=user["username"],
        role=user["role"],
    )

    create_session(
        user["username"],
    )

    log_event({
        "event_type":
            "authentication_event",

        "user":
            user["username"],

        "resource":
            "login",

        "decision":
            "ALLOW",

        "source":
            "flask-gateway",
    })

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "role": user["role"],
    })


def validate_request(resource):

    # ========================================================
    # AUTHORIZATION HEADER VALIDATION
    # ========================================================

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        return None, (
            jsonify({
                "error":
                    "Authorization header missing",
            }),
            401,
        )

    if not auth_header.startswith("Bearer "):

        return None, (
            jsonify({
                "error":
                    "Invalid Authorization format",
            }),
            401,
        )

    token = auth_header.split(
        " ",
        1,
    )[1].strip()

    if not token:

        return None, (
            jsonify({
                "error":
                    "Bearer token missing",
            }),
            401,
        )

    # ========================================================
    # TOKEN VERIFICATION
    # ========================================================

    payload = verify_token(token)

    if payload is None:

        return None, (
            jsonify({
                "error":
                    "Invalid or expired token",
            }),
            401,
        )

    username = payload.get("username")

    if not username:

        return None, (
            jsonify({
                "error":
                    "Token does not contain username",
            }),
            401,
        )

    # ========================================================
    # AUTOMATED INCIDENT RESPONSE ENFORCEMENT
    #
    # IMPORTANT:
    # This check happens before authorization context creation
    # and before OPA evaluation.
    # ========================================================

    if is_identity_blocked(username):

        log_event({
            "event_type":
                "incident_response_enforcement",

            "user":
                username,

            "resource":
                resource,

            "decision":
                "DENY",

            "reason":
                "identity_blocked",

            "source":
                "flask-gateway",
        })

        return None, (
            jsonify({
                "error":
                    "Access denied",

                "reason":
                    "Identity blocked by automated incident response",
            }),
            403,
        )

    # ========================================================
    # BUILD ZERO TRUST AUTHORIZATION CONTEXT
    # ========================================================

    policy_input = build_authorization_context(
        payload,
        resource,
    )

    # ========================================================
    # AUDIT AUTHORIZATION REQUEST
    # ========================================================

    log_event({
        "event_type":
            "authorization_request",

        "user":
            username,

        "resource":
            resource,

        "action":
            "Authorization Request",

        "device":
            policy_input.get("device"),

        "risk":
            policy_input.get("risk"),

        "source":
            "flask-gateway",
    })

    # ========================================================
    # OPA POLICY EVALUATION
    # ========================================================

    try:

        allowed = evaluate_policy(
            policy_input
        )

    except Exception as error:

        log_event({
            "event_type":
                "authorization_decision",

            "user":
                username,

            "resource":
                resource,

            "decision":
                "DENY",

            "reason":
                "opa_evaluation_error",

            "error":
                str(error),

            "source":
                "flask-gateway",
        })

        return None, (
            jsonify({
                "error":
                    "Authorization service unavailable",
            }),
            503,
        )

    # ========================================================
    # AUDIT AUTHORIZATION DECISION
    # ========================================================

    log_event({
        "event_type":
            "authorization_decision",

        "user":
            username,

        "resource":
            resource,

        "decision":
            "ALLOW" if allowed else "DENY",

        "source":
            "flask-gateway",
    })

    # ========================================================
    # DENY REQUEST WHEN OPA RETURNS FALSE
    # ========================================================

    if not allowed:

        return None, (
            jsonify({
                "error":
                    "Access denied by OPA",
            }),
            403,
        )

    return payload, None


@gateway.get("/bridge")
def bridge():

    payload, error = validate_request(
        "bridge"
    )

    if error:
        return error

    response, status = forward_request(
        "bridge"
    )

    return jsonify({
        "user":
            payload["username"],

        "role":
            payload["role"],

        "backend":
            response,
    }), status


@gateway.get("/pos")
def pos():

    payload, error = validate_request(
        "pos"
    )

    if error:
        return error

    response, status = forward_request(
        "pos"
    )

    return jsonify({
        "user":
            payload["username"],

        "role":
            payload["role"],

        "backend":
            response,
    }), status


@gateway.get("/crew")
def crew():

    payload, error = validate_request(
        "crew"
    )

    if error:
        return error

    response, status = forward_request(
        "crew"
    )

    return jsonify({
        "user":
            payload["username"],

        "role":
            payload["role"],

        "backend":
            response,
    }), status