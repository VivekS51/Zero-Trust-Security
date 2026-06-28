from flask import Flask

from routes import gateway

app = Flask(__name__)

app.register_blueprint(gateway)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )