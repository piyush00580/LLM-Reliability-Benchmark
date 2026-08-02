from flask import Flask, jsonify, request
from flask_cors import CORS

from services.dashboard_service import DashboardService
from services.benchmark_service import BenchmarkService

app = Flask(__name__)
CORS(app)

benchmark_service = BenchmarkService()


@app.route("/api/dashboard")
def dashboard():

    stats = DashboardService.get_stats()

    return jsonify({
        **stats,

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
            {"name": "Robustness", "score": 94}
        ]
    })


@app.route("/api/benchmark", methods=["POST"])
def benchmark():

    data = request.get_json()

    text = data.get("text", "")
    models = data.get("models", [])
    benchmarks = data.get("benchmarks", [])

    if not text.strip():
        return {"error": "Text is required."}, 400

    if not models:
        return {"error": "Select at least one model"}, 400

    if not benchmarks:
        return {"error": "Select at least one benchmark"}, 400

    results = benchmark_service.run(text=text,
        models=models,
        benchmarks=benchmarks)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)