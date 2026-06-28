import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRY_MINUTES = int(
    os.getenv("TOKEN_EXPIRY_MINUTES", "60")
)

SESSION_TIMEOUT = 3600

SERVICES = {
    "bridge": "http://127.0.0.1:5001",
    "pos": "http://127.0.0.1:5002",
    "crew": "http://127.0.0.1:5003"
}