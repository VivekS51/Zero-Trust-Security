"""
JWT Authentication Module
"""

from datetime import datetime, timedelta
import jwt

from config import JWT_SECRET, JWT_ALGORITHM

from config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    TOKEN_EXPIRY_MINUTES
)


def create_token(username: str, role: str):

    payload = {
        "username": username,
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None