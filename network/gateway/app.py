"""
Zero Trust Cruise Platform
Flask API Gateway Application
"""

from flask import Flask

from routes import gateway


def create_app():
    """
    Create and configure the Flask Gateway application.
    """

    app = Flask(__name__)

    # Register all routes:
    # /
    # /login
    # /bridge
    # /pos
    # /crew
    app.register_blueprint(gateway)

    return app


app = create_app()


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
        use_reloader=False
    )