# LLM Reliability Benchmark Platform

A modular benchmarking platform for evaluating and comparing the reliability of Large Language Models (LLMs) across multiple dimensions such as consistency, hallucination, information retention, and prompt robustness.

The platform supports multiple LLM providers, automated evaluation metrics, dataset-based benchmarking, reliability scoring, benchmark history, report generation, REST APIs, and a React-based dashboard.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Screenshots and Demo](#screenshots-and-demo)
- [System Architecture](#system-architecture)
- [Benchmark Dimensions](#benchmark-dimensions)
- [Evaluation Metrics](#evaluation-metrics)
- [Supported Models](#supported-models)
- [Datasets](#datasets)
- [Reliability Scoring](#reliability-scoring)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [How the Platform Works](#how-the-platform-works)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [Using Ollama](#using-ollama)
- [API Reference](#api-reference)
- [API Validation](#api-validation)
- [Testing](#testing)
- [Reporting and History](#reporting-and-history)
- [Design Principles](#design-principles)
- [Error Handling](#error-handling)
- [Security Notes](#security-notes)
- [Current Status](#current-status)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## Overview

Large Language Models can produce highly convincing responses while still suffering from issues such as hallucination, inconsistency, information loss, and sensitivity to prompt changes.

This project provides a structured environment for evaluating these reliability dimensions using a modular benchmarking architecture.

The platform allows users to:

- Select one or more LLMs
- Select multiple benchmark types
- Run automated evaluations
- Compare model performance
- Calculate an overall reliability score
- Store benchmark history
- Export benchmark results
- Evaluate models using predefined datasets
- Access benchmarking functionality through REST APIs
- Visualize results through a React dashboard

The architecture is designed to make new models, benchmarks, and evaluation metrics easy to integrate without modifying the core execution pipeline.

---

## Problem Statement

LLM evaluation is often performed using isolated metrics or individual test scripts.

This makes it difficult to:

- Compare multiple models consistently
- Evaluate different dimensions of reliability
- Reuse benchmark implementations
- Track historical benchmark runs
- Aggregate multiple reliability dimensions
- Evaluate models across domain-specific datasets
- Expose benchmarking functionality through an application interface

This project addresses these challenges through a modular and extensible LLM reliability benchmarking platform.

---

## Objectives

The primary objectives of the platform are:

1. Build a modular LLM benchmarking framework.
2. Support multiple LLM providers.
3. Evaluate different reliability dimensions.
4. Implement reusable evaluation metrics.
5. Calculate an overall reliability score.
6. Support dataset-based benchmarking.
7. Compare multiple models using the same benchmarks.
8. Maintain historical benchmark results.
9. Export benchmark reports.
10. Provide REST API access.
11. Provide a web-based dashboard.
12. Maintain automated test coverage for core functionality.

---

# Key Features

## Multi-Model Benchmarking

The platform supports benchmarking multiple models using the same input and benchmark configuration.

Currently supported models include:

- Google Gemini
- Ollama
- Mock Excellent
- Mock Average
- Mock Poor

This allows both real-world model comparison and controlled testing using deterministic baseline models.

---

## Modular Benchmark Plugins

Benchmarks are implemented as independent modules.

Current benchmarks include:

- Consistency
- Hallucination
- Information Retention
- Prompt Robustness

The plugin architecture allows additional benchmarks to be added without redesigning the core platform.

---

## Multiple Evaluation Metrics

The platform uses multiple evaluation techniques depending on the benchmark.

Current evaluation metrics include:

- Semantic Similarity
- Entity Consistency
- Keyword Consistency
- Compression Evaluation
- Readability Evaluation

These metrics can be combined to create benchmark-specific scores.

---

## Overall Reliability Score

The platform calculates an overall reliability score from the supported benchmark dimensions.

Current weighting:

| Benchmark | Weight |
|---|---:|
| Consistency | 25% |
| Hallucination | 25% |
| Information Retention | 25% |
| Prompt Robustness | 25% |

The resulting score provides a single high-level reliability indicator while still preserving the individual benchmark scores.

---

## Dataset-Based Evaluation

The platform supports predefined domain-specific datasets.

Current datasets include:

- Finance
- Healthcare
- Legal
- Sports
- Technology

Dataset benchmarking allows models to be evaluated using domain-specific inputs rather than relying only on manually entered text.

---

## Model Comparison

Multiple models can be evaluated using the same benchmark configuration.

The comparison functionality provides model-level benchmark results that can be used to analyze differences in:

- Reliability
- Benchmark performance
- Latency
- Evaluation metrics

---

## Benchmark History

Benchmark executions are stored in a SQLite database.

Stored information includes:

- Run ID
- Timestamp
- Model
- Benchmark
- Score
- Latency
- Input text

This allows previous benchmark runs to be retrieved and analyzed.

---

## Report Generation

Benchmark results can be exported into report formats for further analysis.

Supported export functionality includes:

- JSON
- CSV

Generated reports can be used for:

- Analysis
- Documentation
- Model comparisons
- Benchmark records

---

## REST API

The platform provides a Flask-based REST API for interacting with the benchmarking engine.

Available endpoints include:

```text
GET  /api/dashboard
POST /api/benchmark
POST /api/compare
GET  /api/history
GET  /api/export/csv


## React Dashboard

The frontend provides a web-based interface for interacting with the benchmark platform.

The dashboard includes sections for:

Dashboard
Benchmark
Reports
Model Comparison
Settings

The frontend communicates with the backend through REST APIs.

---

## System Architecture

The platform follows a modular layered architecture.

                        ┌─────────────────────┐
                        │      React UI       │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │     REST API        │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  BenchmarkService   │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │  PlatformRunner     │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
          ┌─────────────────┐           ┌─────────────────┐
          │ Comparison      │           │ PluginManager   │
          │ Service         │           │                 │
          └────────┬────────┘           └────────┬────────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                       ┌──────────────────────┐
                       │ Benchmark Plugins    │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ Evaluation Pipeline  │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ Evaluation Metrics   │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ Reliability Service  │
                       └──────────┬───────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
          ┌──────────────────┐        ┌──────────────────┐
          │ Report Service   │        │ History Service  │
          └──────────────────┘        └──────────────────┘


## Benchmark Dimensions
    1. Consistency

    The consistency benchmark evaluates whether a model produces stable outputs when responding to the same or related inputs.

    The benchmark can help identify variations in model responses and semantic consistency.

    2. Hallucination

    The hallucination benchmark evaluates how faithfully generated summaries preserve information from the original input.

    The current implementation combines:

    Semantic similarity
    Entity consistency
    Keyword consistency

The internal weighting is:

| Metric              | Weight |
| ------------------- | -----: |
| Semantic Similarity |    50% |
| Entity Consistency  |    30% |
| Keyword Consistency |    20% |


    3. Information Retention

    The information retention benchmark evaluates how much important information is preserved when the model generates a transformed or summarized response.

    This dimension helps identify information loss during generation.

    4. Prompt Robustness

    The prompt robustness benchmark evaluates model behavior under variations in prompting conditions.

    This helps assess whether small prompt changes can significantly affect model output.

## Evaluation Metrics

    Semantic Similarity

    Semantic similarity uses embeddings to compare the meaning of two pieces of text.

    The project uses cosine similarity between embeddings.

    The resulting similarity value is normalized before being used in the evaluation pipeline.


    Entity Consistency

    Entity consistency compares entities detected in the original text with entities detected in the generated response.

    Entities may include items such as:

    People
    Organizations
    Locations
    Dates
    Other named entities

    The implementation uses spaCy's NLP pipeline.


    Keyword Consistency

    Keyword consistency extracts important lexical information from the original and generated texts.

    The implementation considers:

    Nouns
    Proper nouns
    Adjectives

    Stop words and punctuation are excluded.

    The overlap between the original and generated keywords contributes to the evaluation score.


    Compression Evaluation

    Compression evaluation measures the relationship between the original text and generated output in terms of textual compression.

    This metric can help identify how much content was reduced during generation.


    Readability Evaluation

    Readability evaluation provides an additional perspective on the generated output by evaluating its readability characteristics.


Supported Models
Google Gemini

The platform supports Google's Gemini models through the Google GenAI Python client.

The active Gemini model is configured through:

backend/core/config.py

The model can therefore be changed without modifying the benchmark architecture.

Ollama

The platform supports locally hosted models through Ollama.

Current configured model:

llama3.2:3b

Ollama is accessed through its local API.

Default endpoint:

http://localhost:11434/api/generate
Mock Models

Three controlled mock models are included:

Mock Excellent
Mock Average
Mock Poor

These models provide controlled baselines for testing the evaluation and scoring system.

They are particularly useful for validating whether the benchmarking pipeline correctly distinguishes between different expected reliability levels.

Datasets

The platform currently supports the following domain datasets:

Dataset	Domain
Finance	Financial information
Healthcare	Healthcare information
Legal	Legal information
Sports	Sports information
Technology	Technology information

Datasets are used by the dataset benchmarking functionality to run predefined evaluation inputs.

Reliability Scoring

The platform calculates an overall reliability score using the benchmark scores and configured weights.

The current reliability configuration is:

Consistency             → 25%
Hallucination           → 25%
Information Retention   → 25%
Prompt Robustness      → 25%

The weighted scores are combined to calculate the final reliability score.

The platform also preserves the individual benchmark scores through the reliability breakdown.

Example structure:

{
    "overall_score": 85.4,
    "breakdown": {
        "Consistency": 88.0,
        "Hallucination": 82.0,
        "Information Retention": 86.0,
        "Prompt Robustness": 85.6
    }
}
Technology Stack
Backend
Python
Flask
REST API
SQLite
pytest
Machine Learning / NLP
Sentence Transformers
spaCy
Cosine Similarity
Text-based evaluation metrics
LLM Integration
Google Gemini
Ollama
Mock LLM services
Frontend
React
Vite
React Router
Axios
Recharts
React Icons
JavaScript
Development Tools
Git
GitHub
VS Code
Postman
Project Structure
LLM-Reliability-Benchmark/
│
├── backend/
│   │
│   ├── api.py
│   ├── main.py
│   ├── list_models.py
│   │
│   ├── api/
│   │
│   ├── benchmarks/
│   │   ├── benchmark.py
│   │   ├── consistency_benchmark.py
│   │   ├── hallucination_benchmark.py
│   │   ├── information_decay_benchmark.py
│   │   ├── prompt_robustness_benchmark.py
│   │   └── __init__.py
│   │
│   ├── config/
│   │   ├── reliability_config.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── __init__.py
│   │
│   ├── evaluation/
│   │   ├── compression_evaluator.py
│   │   ├── entity_consistency_evaluator.py
│   │   ├── evaluation_metric.py
│   │   ├── evaluation_pipeline.py
│   │   ├── keyword_consistency_evaluator.py
│   │   ├── readability_evaluator.py
│   │   ├── similarity_evaluator.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── benchmark_history_service.py
│   │   ├── benchmark_service.py
│   │   ├── comparison_service.py
│   │   ├── dashboard_service.py
│   │   ├── dataset_runner.py
│   │   ├── embedding_service.py
│   │   ├── export_service.py
│   │   ├── gemini_service.py
│   │   ├── llm_factory.py
│   │   ├── llm_service.py
│   │   ├── mock_average_service.py
│   │   ├── mock_excellent_service.py
│   │   ├── mock_poor_service.py
│   │   ├── mock_service.py
│   │   ├── ollama_service.py
│   │   ├── platform_runner.py
│   │   ├── plugin_manager.py
│   │   ├── reliability_service.py
│   │   ├── report_service.py
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── banner.py
│       ├── logger.py
│       └── __init__.py
│
├── frontend/
│
├── datasets/
│
├── database/
│
├── reports/
│
├── tests/
│   ├── test_api.py
│   ├── test_core_services.py
│   ├── test_evaluators.py
│   ├── test_integration.py
│   └── test_reliability.py
│
├── pytest.ini
├── .gitignore
└── README.md
How the Platform Works

The main execution flow is:

User Input
    │
    ▼
Model Selection
    │
    ▼
Benchmark Selection
    │
    ▼
PlatformRunner
    │
    ▼
ComparisonService
    │
    ▼
Benchmark Plugin
    │
    ▼
LLM Generation
    │
    ▼
EvaluationPipeline
    │
    ▼
Evaluation Metrics
    │
    ▼
Benchmark Score
    │
    ▼
ReliabilityService
    │
    ▼
Overall Reliability Score
    │
    ├──────────────► SQLite History
    │
    └──────────────► Reports / API / Dashboard
Installation
1. Clone the Repository
git clone <https://github.com/piyush00580/LLM-Reliability-Benchmark>

Navigate into the project:

cd LLM-Reliability-Benchmark
2. Create a Virtual Environment

On Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate

On Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate
3. Install Backend Dependencies

Install the required Python packages:

pip install -r backend/requirements.txt

If a requirements file is not present, install the dependencies used by the project environment.

Environment Configuration

Create a .env file in the project root.

Example:

GEMINI_API_KEY=your_gemini_api_key

The API key is loaded through environment variables.

Do not commit the .env file to GitHub.

The .gitignore configuration excludes environment files:

.env
.env.*
Running the Backend

Navigate to the backend directory:

cd backend

Start the Flask API:

python api.py

The backend API will run locally.

The dashboard endpoint can be used to verify that the API is available:

GET /api/dashboard
Running the Frontend

Navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the Vite development server:

npm run dev

The terminal will display the local development URL.

Open the provided URL in a browser to access the React dashboard.

Using Ollama

Install Ollama separately and make sure the Ollama server is running.

Pull the configured model:

ollama pull llama3.2:3b

Verify the model:

ollama list

The platform communicates with Ollama through:

http://localhost:11434/api/generate

If the Ollama server is unavailable, the application handles the connection failure and returns an appropriate error response.

API Reference
Dashboard
Request
GET /api/dashboard

Provides dashboard-level information used by the frontend.

Run Benchmark
Request
POST /api/benchmark

Example request body:

{
    "text": "Artificial intelligence is transforming healthcare.",
    "models": [
        "gemini",
        "mock_excellent"
    ],
    "benchmarks": [
        "consistency",
        "hallucination",
        "information_decay",
        "prompt_robustness"
    ]
}
Compare Models
Request
POST /api/compare

The comparison endpoint evaluates selected models using the requested benchmark configuration.

Example:

{
    "text": "Artificial intelligence is transforming healthcare.",
    "models": [
        "gemini",
        "ollama",
        "mock_excellent"
    ],
    "benchmark": "hallucination"
}
Benchmark History
Request
GET /api/history

Returns previously stored benchmark runs.

Stored fields include:

id
timestamp
model
benchmark
score
latency
input_text
CSV Export
Request
GET /api/export/csv

The endpoint exports benchmark history into CSV format.

Filtering can be applied using supported model and benchmark parameters.

API Validation

The API validates incoming requests before executing benchmarks.

Validation includes:

Request body validation
Model validation
Benchmark validation
JSON validation
Unsupported model detection
Unsupported benchmark detection

Supported models:

gemini
ollama
mock_excellent
mock_average
mock_poor

Supported benchmarks:

consistency
hallucination
information_decay
prompt_robustness

Invalid requests return structured error information instead of silently executing unsupported configurations.

Testing

The project uses pytest for automated testing.

The test suite is organized into:

tests/
├── test_api.py
├── test_core_services.py
├── test_evaluators.py
├── test_integration.py
└── test_reliability.py

Run the complete test suite from the project root:

pytest

Current test status:

24 passed

The tests cover:

API validation
Core services
Evaluation metrics
Reliability scoring
Model selection
End-to-end benchmark execution
Integration between major backend components

The integration test verifies the complete benchmarking pipeline from model selection through benchmark execution and reliability calculation.

Reporting and History

Every completed benchmark run can be stored in the SQLite database.

The database is located at:

database/benchmark_history.db

The primary table is:

benchmark_runs

The table stores:

Field	Description
id	Unique run identifier
timestamp	Benchmark execution time
model	Model used
benchmark	Benchmark executed
score	Benchmark score
latency	Generation latency
input_text	Input provided to the benchmark
Design Principles
Modularity

Benchmark implementations are separated from the execution engine.

This allows individual benchmark plugins to be developed and maintained independently.

Extensibility

The plugin discovery architecture allows new benchmarks to be added without modifying the main execution pipeline.

Separation of Concerns

The system separates responsibilities across:

API
Platform execution
Model services
Benchmark plugins
Evaluation metrics
Reliability calculation
History storage
Reporting
Reusability

Evaluation metrics are implemented as reusable components through the evaluation pipeline.

Multiple benchmarks can therefore reuse the same evaluation functionality.

Testability

Core functionality is covered through automated tests.

The project includes unit-level and integration-level tests to validate important components and the end-to-end pipeline.

Error Handling

The platform includes error handling for external model services.

For example, the Ollama service handles:

Server connection failures
Request timeouts
HTTP errors
Invalid responses
Empty generated responses
Unexpected request errors

Gemini API calls also include retry handling for rate-limit conditions.

The goal is to prevent external service failures from causing uncontrolled application crashes.

Security Notes

The project follows basic security practices for local development.

API Keys

API keys are loaded from environment variables rather than being hardcoded in source files.

Example:

GEMINI_API_KEY=your_api_key
.env

Environment files are excluded from version control.

.env
.env.*
Database and Generated Reports

Local database and generated report files are excluded from Git tracking where appropriate.

Current Status

The major backend components of the platform are implemented.

Current capabilities include:

 Modular benchmark architecture
 Plugin discovery
 Multiple benchmark types
 Multiple evaluation metrics
 Reliability scoring
 Dataset-based benchmarking
 Google Gemini integration
 Ollama integration
 Controlled mock models
 Model comparison
 SQLite benchmark history
 JSON export
 CSV export
 REST API
 React dashboard integration
 API validation
 Error handling
 Automated testing
 End-to-end integration testing
 Project cleanup
 GitHub documentation

Current automated test status:

24 / 24 tests passing
Future Improvements

Potential future improvements include:

Additional real LLM providers
More domain-specific datasets
Additional reliability metrics
Advanced hallucination detection
Improved prompt robustness testing
Statistical analysis across repeated benchmark runs
Advanced visualization and analytics
Model performance trend analysis
Cloud deployment
CI/CD integration
Expanded benchmark configuration
Additional export formats

These are future possibilities and are not represented as currently implemented features.