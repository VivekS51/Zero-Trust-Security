"""
Zero Trust Cruise Platform
Gateway Routes
"""

from flask import Blueprint, jsonify, request

from authorization_context import build_authorization_context
from auth import create_token, verify_token
from session_manager import create_session
from user_store import authenticate
from proxy import forward_request
from opa_client import evaluate_policy
from audit import log_event


gateway = Blueprint(
    "gateway",
    __name__
)


@gateway.get("/")
def home():

    return jsonify({
        "project": "Zero Trust Cruise Platform",
        "gateway": "ONLINE",
        "version": "1.0"
    })


@gateway.post("/login")
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body missing"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    user = authenticate(
        username,
        password
    )

    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    token = create_token(
        username=user["username"],
        role=user["role"]
    )

    create_session(
        user["username"]
    )

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "role": user["role"]
    })


def validate_request(resource):

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:
        return None, (
            jsonify({
                "error": "Authorization header missing"
            }),
            401,
        )

    if not auth_header.startswith("Bearer "):
        return None, (
            jsonify({
                "error": "Invalid Authorization format"
            }),
            401,
        )

    token = auth_header.split(
        " ",
        1
    )[1].strip()

    if not token:
        return None, (
            jsonify({
                "error": "Bearer token missing"
            }),
            401,
        )

    payload = verify_token(token)

    if payload is None:
        return None, (
            jsonify({
                "error": "Invalid or expired token"
            }),
            401,
        )

    policy_input = build_authorization_context(
        payload,
        resource
    )

    # Audit the authorization request.
    log_event({
        "event_type": "authorization_request",
        "user": payload["username"],
        "role": payload["role"],
        "resource": resource,
        "action": "access",
        "device": policy_input["device"],
        "risk": policy_input["risk"]
    })

    # OPA evaluates the authorization policy.
    allowed = evaluate_policy(
        policy_input
    )

    # Audit the authorization decision.
    log_event({
        "event_type": "authorization_decision",
        "user": payload["username"],
        "role": payload["role"],
        "resource": resource,
        "action": "access",
        "decision": (
            "ALLOW"
            if allowed
            else "DENY"
        ),
        "risk_level": policy_input["risk"]["level"],
        "risk_score": policy_input["risk"]["score"]
    })

    if not allowed:
        return None, (
            jsonify({
                "error": "Access denied by OPA"
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
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
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
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
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
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
    }), status