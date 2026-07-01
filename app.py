from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from audit import add_entry, load_log, update_entry
from datetime import datetime
import uuid
from detector import llm_detector
from heuristics import heuristic_detector
from confidence import combine_scores
from labels import generate_label


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

    llm_score = llm_detector(text)

    heuristic_score = heuristic_detector(text)

    confidence = combine_scores(
            llm_score,
            heuristic_score
    )

    attribution, label = generate_label(confidence)

    entry = {
            "content_id": content_id,
            "creator_id": creator_id,
            "timestamp": datetime.utcnow().isoformat(),
            "llm_score": llm_score,
            "heuristic_score": heuristic_score,
            "confidence": confidence,
            "attribution": attribution,
            "label": label,
            "status": "classified"
    }

    add_entry(entry)

    return jsonify(entry)

@app.route("/log", methods=["GET"])
def log():
    return jsonify({
        "entries": load_log()
    })

@app.route("/appeal", methods=["POST"])
def appeal():

    data = request.get_json()

    content_id = data.get("content_id")
    creator_reasoning = data.get("creator_reasoning")

    if not content_id or not creator_reasoning:
        return jsonify({
            "error": "content_id and creator_reasoning are required"
        }), 400

    update_entry(content_id, creator_reasoning)

    return jsonify({
        "message": "Appeal received.",
        "content_id": content_id,
        "status": "under_review"
    })

if __name__ == "__main__":
    app.run(debug=True)
