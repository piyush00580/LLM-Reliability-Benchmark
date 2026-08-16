from flask import Flask, jsonify, request
from flask_cors import CORS
from services.dashboard_service import DashboardService
from services.benchmark_service import BenchmarkService
from services.benchmark_history_service import BenchmarkHistoryService

app = Flask(__name__)
CORS(app)

benchmark_service = BenchmarkService()
history_service = BenchmarkHistoryService()

@app.route("/api/dashboard")
def dashboard():

    stats = DashboardService.get_stats()

    return jsonify(stats)


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

@app.route("/api/history", methods=["GET"])
def history():

    runs = history_service.get_all_runs()

    return jsonify({
        "runs": runs,
        "total": len(runs)
    })


if __name__ == "__main__":
    app.run(debug=True)