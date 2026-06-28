import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USER_FILE = BASE_DIR / "data" / "users.json"


def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)["users"]


import bcrypt

def authenticate(username, password):

    users = load_users()

    for user in users:

        if user["username"] != username:
            continue

        if bcrypt.checkpw(
            password.encode(),
            user["password_hash"].encode()
        ):
            return user

    return None