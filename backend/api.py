from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from services.dashboard_service import DashboardService
from services.benchmark_service import BenchmarkService
from services.benchmark_history_service import BenchmarkHistoryService
from services.export_service import ExportService

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

@app.route("/api/compare", methods=["POST"])
def compare():

    data = request.get_json()

    text = data.get("text", "")
    models = data.get("models", [])
    benchmarks = data.get("benchmarks", [])

    if not text.strip():
        return {"error": "Text is required."}, 400

    if len(models) < 2:
        return {"error": "Select at least two models"}, 400

    if not benchmarks:
        return {"error": "Select at least one benchmark"}, 400

    results = benchmark_service.run(
        text=text,
        models=models,
        benchmarks=benchmarks
    )

    return jsonify(results)

@app.route("/api/history", methods=["GET"])
def history():

    runs = history_service.get_all_runs()

    return jsonify({
        "runs": runs,
        "total": len(runs)
    })

@app.route("/api/export/csv", methods=["GET"])
def export_csv():

    runs = history_service.get_all_runs()

    selected_model = request.args.get("model", "All")
    selected_benchmark = request.args.get("benchmark", "All")

    if selected_model != "All":
        runs = [
            run for run in runs
            if run["model"] == selected_model
        ]

    if selected_benchmark != "All":
        runs = [
            run for run in runs
            if run["benchmark"] == selected_benchmark
        ]

    output_file = ExportService.export_csv(runs)

    return send_file(
        output_file,
        as_attachment=True,
        download_name=output_file.name,
        mimetype="text/csv"
    )


if __name__ == "__main__":
    app.run(debug=True)