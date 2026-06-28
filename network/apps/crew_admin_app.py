from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

SYSTEM_INFORMATION = {
    "system": "Crew Administration",
    "zone": "Crew",
    "classification": "Internal",
    "status": "ONLINE"
}


@app.get("/")
def home():
    return jsonify({
        "message": "Crew Administration System",
        "access": "AUTHORIZED",
        "details": SYSTEM_INFORMATION
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "crew-admin"
    })


if __name__ == "__main__":
    print("Crew Admin System running on port 5003...")
    serve(app, host="0.0.0.0", port=5003)