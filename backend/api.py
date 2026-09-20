
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from services.dashboard_service import DashboardService
from services.benchmark_service import BenchmarkService
from services.benchmark_history_service import BenchmarkHistoryService
from services.export_service import ExportService
from services.llm_factory import LLMFactory


app = Flask(__name__)
CORS(app)

benchmark_service = BenchmarkService()
history_service = BenchmarkHistoryService()


VALID_MODELS = {
    "gemini",
    "ollama",
    "groq",
    "mistral",
    "mock_excellent",
    "mock_average",
    "mock_poor",
}


VALID_BENCHMARKS = {
    "consistency",
    "hallucination",
    "information_decay",
    "prompt_robustness",
}


# -------------------------------------------------------------------
# Response Helpers
# -------------------------------------------------------------------

def success_response(data=None, status_code=200):
    """
    Return a consistent success response.
    """
    response = {
        "status": "success"
    }

    if data:
        response.update(data)

    return jsonify(response), status_code


def error_response(
    message,
    error_code="INTERNAL_ERROR",
    status_code=500,
    details=None
):
    """
    Return a consistent error response.
    """
    response = {
        "status": "error",
        "message": message,
        "error_code": error_code
    }

    if details:
        response["details"] = details

    return jsonify(response), status_code


# -------------------------------------------------------------------
# Validation Helpers
# -------------------------------------------------------------------

def validate_request_data(data):
    """
    Validate whether the request contains a JSON object.
    """
    if not isinstance(data, dict):
        return error_response(
            message="Request body must be valid JSON.",
            error_code="INVALID_JSON",
            status_code=400
        )

    return None


def validate_models(models):
    """
    Validate selected model names.
    """
    if not isinstance(models, list):
        return error_response(
            message="Models must be provided as a list.",
            error_code="INVALID_MODELS_FORMAT",
            status_code=400
        )

    invalid_models = [
        model for model in models
        if model not in VALID_MODELS
    ]

    if invalid_models:
        return error_response(
            message="One or more selected models are unsupported.",
            error_code="UNSUPPORTED_MODEL",
            status_code=400,
            details={
                "invalid_models": invalid_models,
                "available_models": sorted(VALID_MODELS)
            }
        )

    return None


def validate_benchmarks(benchmarks):
    """
    Validate selected benchmark names.
    """
    if not isinstance(benchmarks, list):
        return error_response(
            message="Benchmarks must be provided as a list.",
            error_code="INVALID_BENCHMARKS_FORMAT",
            status_code=400
        )

    invalid_benchmarks = [
        benchmark
        for benchmark in benchmarks
        if benchmark not in VALID_BENCHMARKS
    ]

    if invalid_benchmarks:
        return error_response(
            message="One or more selected benchmarks are unsupported.",
            error_code="UNSUPPORTED_BENCHMARK",
            status_code=400,
            details={
                "invalid_benchmarks": invalid_benchmarks,
                "available_benchmarks": sorted(VALID_BENCHMARKS)
            }
        )

    return None


def validate_benchmark_payload(data, minimum_models=1):
    """
    Validate the shared payload used by benchmark and compare routes.
    """
    text = data.get("text", "")
    models = data.get("models", [])
    benchmarks = data.get("benchmarks", [])

    if not isinstance(text, str) or not text.strip():
        return error_response(
            message="Text is required and cannot be empty.",
            error_code="MISSING_TEXT",
            status_code=400
        )

    if not isinstance(models, list) or len(models) < minimum_models:
        if minimum_models == 1:
            message = "Select at least one model."
        else:
            message = f"Select at least {minimum_models} models."

        return error_response(
            message=message,
            error_code="INSUFFICIENT_MODELS",
            status_code=400
        )

    if not isinstance(benchmarks, list) or not benchmarks:
        return error_response(
            message="Select at least one benchmark.",
            error_code="MISSING_BENCHMARKS",
            status_code=400
        )

    model_error = validate_models(models)

    if model_error:
        return model_error

    benchmark_error = validate_benchmarks(benchmarks)

    if benchmark_error:
        return benchmark_error

    return None


# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    """
    Return dashboard statistics.
    """
    try:
        stats = DashboardService.get_stats()

        return success_response(
            data={
                "data": stats
            }
        )

    except Exception as error:
        app.logger.exception("Dashboard error: %s", error)

        return error_response(
            message="Unable to load dashboard statistics.",
            error_code="DASHBOARD_UNAVAILABLE",
            status_code=500
        )


# -------------------------------------------------------------------
# Benchmark
# -------------------------------------------------------------------

@app.route("/api/benchmark", methods=["POST"])
def benchmark():
    """
    Run selected benchmarks against selected models.
    """
    data = request.get_json(silent=True)

    validation_error = validate_request_data(data)

    if validation_error:
        return validation_error

    validation_error = validate_benchmark_payload(
        data=data,
        minimum_models=1
    )

    if validation_error:
        return validation_error

    text = data["text"].strip()
    models = data["models"]
    benchmarks = data["benchmarks"]

    try:
        results = benchmark_service.run(
            text=text,
            models=models,
            benchmarks=benchmarks
        )

        return success_response(
            data={
                "results": results
            }
        )

    except ValueError as error:
        app.logger.warning("Benchmark validation/provider error: %s", error)

        return error_response(
            message=str(error),
            error_code="BENCHMARK_CONFIGURATION_ERROR",
            status_code=400
        )

    except Exception as error:
        app.logger.exception("Benchmark execution error: %s", error)

        return error_response(
            message="Benchmark execution failed. Please try again.",
            error_code="BENCHMARK_EXECUTION_FAILED",
            status_code=500
        )


# -------------------------------------------------------------------
# Model Comparison
# -------------------------------------------------------------------

@app.route("/api/compare", methods=["POST"])
def compare():
    """
    Compare multiple models using selected benchmarks.
    """
    data = request.get_json(silent=True)

    validation_error = validate_request_data(data)

    if validation_error:
        return validation_error

    validation_error = validate_benchmark_payload(
        data=data,
        minimum_models=2
    )

    if validation_error:
        return validation_error

    text = data["text"].strip()
    models = data["models"]
    benchmarks = data["benchmarks"]

    try:
        results = benchmark_service.run(
            text=text,
            models=models,
            benchmarks=benchmarks
        )

        return success_response(
            data={
                "results": results
            }
        )

    except ValueError as error:
        app.logger.warning("Comparison configuration error: %s", error)

        return error_response(
            message=str(error),
            error_code="COMPARISON_CONFIGURATION_ERROR",
            status_code=400
        )

    except Exception as error:
        app.logger.exception("Comparison execution error: %s", error)

        return error_response(
            message="Model comparison failed. Please try again.",
            error_code="COMPARISON_EXECUTION_FAILED",
            status_code=500
        )


# -------------------------------------------------------------------
# Benchmark History
# -------------------------------------------------------------------

@app.route("/api/history", methods=["GET"])
def history():
    """
    Return benchmark history.
    """
    try:
        runs = history_service.get_all_runs()

        return success_response(
            data={
                "runs": runs,
                "total": len(runs)
            }
        )

    except Exception as error:
        app.logger.exception("History retrieval error: %s", error)

        return error_response(
            message="Unable to load benchmark history.",
            error_code="HISTORY_UNAVAILABLE",
            status_code=500
        )


# -------------------------------------------------------------------
# CSV Export
# -------------------------------------------------------------------

@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    """
    Export benchmark history as a CSV file.
    """
    try:
        runs = history_service.get_all_runs()

        selected_model = request.args.get("model", "All")
        selected_benchmark = request.args.get("benchmark", "All")

        if selected_model != "All":
            runs = [
                run
                for run in runs
                if run["model"] == selected_model
            ]

        if selected_benchmark != "All":
            runs = [
                run
                for run in runs
                if run["benchmark"] == selected_benchmark
            ]

        output_file = ExportService.export_csv(runs)

        return send_file(
            output_file,
            as_attachment=True,
            download_name=output_file.name,
            mimetype="text/csv"
        )

    except Exception as error:
        app.logger.exception("CSV export error: %s", error)

        return error_response(
            message="Unable to export benchmark history.",
            error_code="EXPORT_FAILED",
            status_code=500
        )


# -------------------------------------------------------------------
# Provider Status
# -------------------------------------------------------------------

@app.route("/api/providers", methods=["GET"])
def providers():
    """
    Return the configuration and availability status of providers.
    """
    try:
        provider_status = LLMFactory.provider_status()

        return success_response(
            data={
                "providers": provider_status
            }
        )

    except Exception as error:
        app.logger.exception("Provider status error: %s", error)

        return error_response(
            message="Unable to retrieve provider status.",
            error_code="PROVIDER_STATUS_UNAVAILABLE",
            status_code=500
        )


# -------------------------------------------------------------------
# Global Error Handlers
# -------------------------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):
    """
    Handle unknown routes.
    """
    return error_response(
        message="The requested endpoint was not found.",
        error_code="ROUTE_NOT_FOUND",
        status_code=404
    )


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """
    Handle unsupported HTTP methods.
    """
    return error_response(
        message="The HTTP method is not allowed for this endpoint.",
        error_code="METHOD_NOT_ALLOWED",
        status_code=405
    )


@app.errorhandler(500)
def handle_internal_server_error(error):
    """
    Handle unexpected Flask server errors.
    """
    return error_response(
        message="An unexpected server error occurred.",
        error_code="INTERNAL_SERVER_ERROR",
        status_code=500
    )


# -------------------------------------------------------------------
# Application Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)