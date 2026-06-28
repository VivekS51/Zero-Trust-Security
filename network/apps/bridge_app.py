from flask import Flask, jsonify
from waitress import serve

app = Flask(__name__)

SYSTEM_INFORMATION = {
    "system": "Bridge Navigation",
    "zone": "Bridge",
    "classification": "Highest Restriction",
    "status": "ONLINE"
}


@app.get("/")
def home():
    return jsonify({
        "message": "Bridge Navigation System",
        "access": "AUTHORIZED",
        "details": SYSTEM_INFORMATION
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "bridge"
    })


if __name__ == "__main__":
    print("Bridge System running on port 5001...")
    serve(app, host="0.0.0.0", port=5001)