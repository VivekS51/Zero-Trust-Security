import sys
from pathlib import Path


# ============================================================
# PROJECT PATH SETUP
#
# app.py location:
# project_root/network/gateway/app.py
#
# parents[0] = gateway
# parents[1] = network
# parents[2] = project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Import Flask and gateway only AFTER project root is added
# to sys.path.
from flask import Flask
from routes import gateway


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# REGISTER API GATEWAY BLUEPRINT
# ============================================================

app.register_blueprint(gateway)


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return {
        "error": "Route not found"
    }, 404


@app.errorhandler(405)
def method_not_allowed(error):

    return {
        "error": "Method not allowed"
    }, 405


@app.errorhandler(500)
def internal_server_error(error):

    return {
        "error": "Internal server error"
    }, 500


# ============================================================
# APPLICATION STARTUP
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Zero Trust Cruise Platform")
    print("API Gateway starting...")
    print("Gateway URL: http://127.0.0.1:8000")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )