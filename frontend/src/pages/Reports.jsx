import { useEffect, useMemo, useState } from "react";

import Layout from "../components/layout/Layout";
import client from "../api/client";

import {
    FaFileAlt,
    FaDownload,
    FaFilter,
    FaRedo,
    FaChartLine,
    FaClock,
    FaDatabase,
} from "react-icons/fa";

import "./Reports.css";

function Reports() {

    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [selectedModel, setSelectedModel] = useState("All");
    const [selectedBenchmark, setSelectedBenchmark] = useState("All");

    const fetchHistory = async () => {

        try {

            setLoading(true);
            setError("");

            const response = await client.get("/history");

            setRuns(response.data.runs || []);

        } catch (err) {

            console.error("Failed to load benchmark history:", err);

            setError(
                err.response?.data?.detail ||
                err.response?.data?.message ||
                "Could not load benchmark history."
            );

        } finally {

            setLoading(false);

        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const modelNameMap = {
        gemini: "Gemini 2.5 Flash-Lite",
        "gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite",

        ollama: "Llama 3.2 3B",
        "llama3.2:3b": "Llama 3.2 3B",

        groq: "GPT-OSS 120B",
        "openai/gpt-oss-120b": "GPT-OSS 120B",

        mistral: "Ministral 3B",
        "ministral-3b-2512": "Ministral 3B",
    };

    const benchmarkNameMap = {
        consistency: "Consistency",
        Consistency: "Consistency",

        hallucination: "Hallucination Resistance",
        Hallucination: "Hallucination Resistance",

        information_decay: "Information Retention",
        "Information Retention": "Information Retention",

        prompt_robustness: "Prompt Robustness",
        "Prompt Robustness": "Prompt Robustness",
    };

    const getModelName = (model) =>
        modelNameMap[model] || model;

    const getBenchmarkName = (benchmark) =>
        benchmarkNameMap[benchmark] || benchmark;

    const models = useMemo(() => {

        return [
            "All",
            ...new Set(runs.map((run) => run.model))
        ];

    }, [runs]);

    const benchmarks = useMemo(() => {

        return [
            "All",
            ...new Set(runs.map((run) => run.benchmark))
        ];

    }, [runs]);

    const filteredRuns = useMemo(() => {

        return runs.filter((run) => {

            const modelMatch =
                selectedModel === "All" ||
                run.model === selectedModel;

            const benchmarkMatch =
                selectedBenchmark === "All" ||
                run.benchmark === selectedBenchmark;

            return modelMatch && benchmarkMatch;

        });

    }, [runs, selectedModel, selectedBenchmark]);

    const averageScore = useMemo(() => {

        if (!filteredRuns.length) {
            return 0;
        }

        const total = filteredRuns.reduce(
            (sum, run) => sum + Number(run.score || 0),
            0
        );

        return (total / filteredRuns.length) * 100;

    }, [filteredRuns]);

    const averageLatency = useMemo(() => {

        if (!filteredRuns.length) {
            return 0;
        }

        const total = filteredRuns.reduce(
            (sum, run) => sum + Number(run.latency || 0),
            0
        );

        return total / filteredRuns.length;

    }, [filteredRuns]);

    const resetFilters = () => {

        setSelectedModel("All");
        setSelectedBenchmark("All");

    };

    const exportCSV = () => {

        const params = new URLSearchParams();

        if (selectedModel !== "All") {
            params.append("model", selectedModel);
        }

        if (selectedBenchmark !== "All") {
            params.append("benchmark", selectedBenchmark);
        }

        const queryString = params.toString();

        const baseURL = client.defaults.baseURL;

        const url =
            `${baseURL}/export/csv` +
            (queryString ? `?${queryString}` : "");

        window.open(url, "_blank");

    };

    return (

        <Layout>

            <div className="reports-container">

                {/* =========================
                    Header
                ========================= */}

                <section className="reports-header">

                    <div>

                        <div className="reports-eyebrow">

                            <FaFileAlt />

                            EVALUATION ARCHIVE

                        </div>

                        <h1>
                            Reports
                        </h1>

                        <p>
                            Review, filter and export your benchmark history.
                        </p>

                    </div>

                    <button
                        className="reports-export-button"
                        onClick={exportCSV}
                        disabled={loading || runs.length === 0}
                    >

                        <FaDownload />

                        Export CSV

                    </button>

                </section>


                {/* =========================
                    Loading
                ========================= */}

                {loading && (

                    <div className="reports-state">

                        <div className="loading-spinner"></div>

                        <p>
                            Loading evaluation history...
                        </p>

                    </div>

                )}


                {/* =========================
                    Error
                ========================= */}

                {!loading && error && (

                    <div className="reports-state reports-error">

                        <FaFileAlt />

                        <h3>
                            Couldn't load the archive
                        </h3>

                        <p>
                            {error}
                        </p>

                        <button
                            className="retry-button"
                            onClick={fetchHistory}
                        >

                            <FaRedo />

                            Try again

                        </button>

                    </div>

                )}


                {/* =========================
                    Empty
                ========================= */}

                {!loading && !error && runs.length === 0 && (

                    <div className="reports-state">

                        <FaDatabase />

                        <h3>
                            No experiments yet
                        </h3>

                        <p>
                            Run a benchmark and your results will appear here.
                        </p>

                    </div>

                )}


                {/* =========================
                    Reports
                ========================= */}

                {!loading && !error && runs.length > 0 && (

                    <>

                        {/* KPI cards */}

                        <section className="reports-stats">

                            <div className="report-stat-card">

                                <div className="report-stat-icon purple">
                                    <FaDatabase />
                                </div>

                                <div>
                                    <span>Total Runs</span>
                                    <strong>
                                        {filteredRuns.length}
                                    </strong>
                                </div>

                            </div>


                            <div className="report-stat-card">

                                <div className="report-stat-icon green">
                                    <FaChartLine />
                                </div>

                                <div>
                                    <span>Average Score</span>
                                    <strong>
                                        {averageScore.toFixed(1)}%
                                    </strong>
                                </div>

                            </div>


                            <div className="report-stat-card">

                                <div className="report-stat-icon blue">
                                    <FaClock />
                                </div>

                                <div>
                                    <span>Average Latency</span>
                                    <strong>
                                        {averageLatency.toFixed(2)}s
                                    </strong>
                                </div>

                            </div>

                        </section>


                        {/* Main report card */}

                        <section className="reports-card">

                            <div className="reports-card-header">

                                <div>

                                    <div className="card-eyebrow">
                                        <FaFilter />
                                        RUN HISTORY
                                    </div>

                                    <h2>
                                        Benchmark Activity
                                    </h2>

                                    <p>
                                        Every completed evaluation recorded by
                                        the platform.
                                    </p>

                                </div>

                                <span className="results-count-badge">
                                    {filteredRuns.length} / {runs.length}
                                </span>

                            </div>


                            {/* Filters */}

                            <div className="report-filters">

                                <div className="filter-group">

                                    <label>
                                        Model
                                    </label>

                                    <select
                                        value={selectedModel}
                                        onChange={(e) =>
                                            setSelectedModel(e.target.value)
                                        }
                                    >

                                        {models.map((model) => (

                                            <option
                                                key={model}
                                                value={model}
                                            >
                                                {model === "All"
                                                    ? "All models"
                                                    : getModelName(model)}
                                            </option>

                                        ))}

                                    </select>

                                </div>


                                <div className="filter-group">

                                    <label>
                                        Benchmark
                                    </label>

                                    <select
                                        value={selectedBenchmark}
                                        onChange={(e) =>
                                            setSelectedBenchmark(e.target.value)
                                        }
                                    >

                                        {benchmarks.map((benchmark) => (

                                            <option
                                                key={benchmark}
                                                value={benchmark}
                                            >
                                                {benchmark === "All"
                                                    ? "All benchmarks"
                                                    : getBenchmarkName(benchmark)}
                                            </option>

                                        ))}

                                    </select>

                                </div>


                                <button
                                    className="reset-filter-button"
                                    onClick={resetFilters}
                                    disabled={
                                        selectedModel === "All" &&
                                        selectedBenchmark === "All"
                                    }
                                >

                                    <FaRedo />

                                    Reset

                                </button>

                            </div>


                            {/* Results */}

                            {filteredRuns.length === 0 ? (

                                <div className="no-results">

                                    <FaFilter />

                                    <h3>
                                        Nothing matched
                                    </h3>

                                    <p>
                                        Try changing your filters.
                                    </p>

                                </div>

                            ) : (

                                <div className="reports-table-wrapper">

                                    <table className="reports-table">

                                        <thead>

                                            <tr>

                                                <th>
                                                    Model
                                                </th>

                                                <th>
                                                    Benchmark
                                                </th>

                                                <th>
                                                    Score
                                                </th>

                                                <th>
                                                    Latency
                                                </th>

                                                <th>
                                                    Timestamp
                                                </th>

                                            </tr>

                                        </thead>

                                        <tbody>

                                            {filteredRuns.map((run) => {

                                                const score =
                                                    Number(run.score || 0) * 100;

                                                const latency =
                                                    Number(run.latency || 0);

                                                return (

                                                    <tr key={run.id}>

                                                        <td>

                                                            <span className="model-name">
                                                                {getModelName(run.model)}
                                                            </span>

                                                        </td>

                                                        <td>

                                                            <span className="benchmark-name">
                                                                {getBenchmarkName(run.benchmark)}
                                                            </span>

                                                        </td>

                                                        <td>

                                                            <span
                                                                className={`score-pill ${
                                                                    score >= 80
                                                                        ? "score-good"
                                                                        : score >= 60
                                                                            ? "score-medium"
                                                                            : "score-low"
                                                                }`}
                                                            >
                                                                {score.toFixed(1)}%
                                                            </span>

                                                        </td>

                                                        <td>
                                                            {latency.toFixed(2)}s
                                                        </td>

                                                        <td className="timestamp">
                                                            {run.timestamp}
                                                        </td>

                                                    </tr>

                                                );

                                            })}

                                        </tbody>

                                    </table>

                                </div>

                            )}

                        </section>

                    </>

                )}

            </div>

        </Layout>

    );
}

export default Reports;