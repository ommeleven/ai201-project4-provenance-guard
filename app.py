from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import uuid

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Provenance Guard API is running!"
    })


@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():

    data = request.get_json()

    text = data.get("text")
    creator_id = data.get("creator_id")

    if not text or not creator_id:
        return jsonify({
            "error": "text and creator_id are required"
        }), 400

    content_id = str(uuid.uuid4())

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "attribution": "unknown",
        "confidence": 0.50,
        "label": "Placeholder label"
    })


if __name__ == "__main__":
    app.run(debug=True)