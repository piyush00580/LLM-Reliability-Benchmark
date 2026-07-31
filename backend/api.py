from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/api/dashboard")
def dashboard():
    return jsonify({
        "total_runs": 18,
        "models": 2,
        "datasets": 5,
        "reliability": 88,

        "recent_runs": [
            {
                "model": "Gemini",
                "dataset": "Finance",
                "score": 91,
                "status": "Success"
            },
            {
                "model": "Mock",
                "dataset": "Healthcare",
                "score": 88,
                "status": "Success"
            }
        ],

        "chart": [
            {"name": "Consistency", "score": 90},
            {"name": "Hallucination", "score": 82},
            {"name": "Information Decay", "score": 88},
            {"name": "Robustness", "score": 94},
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)