from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

SYSTEM_INFORMATION = {
    "system": "POS Payment",
    "zone": "POS",
    "classification": "PCI-DSS",
    "status": "ONLINE"
}


@app.get("/")
def home():
    return jsonify({
        "message": "POS Payment System",
        "access": "AUTHORIZED",
        "details": SYSTEM_INFORMATION
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "pos"
    })


if __name__ == "__main__":
    print("POS System running on port 5002...")
    serve(app, host="0.0.0.0", port=5002)