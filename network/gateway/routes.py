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

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body missing"
        }), 400

    username = data.get("username")
    password = data.get("password")

    user = authenticate(username, password)

    if not user:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    token = create_token(
        username=user["username"],
        role=user["role"]
    )

    create_session(user["username"])

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "role": user["role"]
    })


def validate_request(resource):

    auth_header = request.headers.get("Authorization")

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

    token = auth_header.split(" ")[1]

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

    log_event({
        "user": payload["username"],
        "resource": resource,
        "action": "Authorization Request",
        "device": policy_input["device"],
        "risk": policy_input["risk"]
    })

    allowed = evaluate_policy(policy_input)

    log_event({
        "user": payload["username"],
        "resource": resource,
        "decision": "ALLOW" if allowed else "DENY"
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

    payload, error = validate_request("bridge")

    if error:
        return error

    response, status = forward_request("bridge")

    return jsonify({
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
    }), status


@gateway.get("/pos")
def pos():

    payload, error = validate_request("pos")

    if error:
        return error

    response, status = forward_request("pos")

    return jsonify({
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
    }), status


@gateway.get("/crew")
def crew():

    payload, error = validate_request("crew")

    if error:
        return error

    response, status = forward_request("crew")

    return jsonify({
        "user": payload["username"],
        "role": payload["role"],
        "backend": response
    }), status