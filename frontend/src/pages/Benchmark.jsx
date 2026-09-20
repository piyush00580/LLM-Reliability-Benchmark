import { useState } from "react";
import client from "../api/client";

import Layout from "../components/layout/Layout";

import {
    FaBolt,
    FaBrain,
    FaCheckCircle,
    FaChevronRight,
    FaExclamationTriangle,
    FaFire,
    FaFlask,
    FaLayerGroup,
    FaShieldAlt,
    FaSyncAlt,
    FaClock,
    FaTrophy,
    FaRedo,
} from "react-icons/fa";

import "./Benchmark.css";

const MODELS = [
    {
        id: "gemini",
        name: "Gemini 2.5 Flash-Lite",
        provider: "Google",
        description: "Fast & capable",
        icon: "✦",
    },
    {
        id: "ollama",
        name: "Llama 3.2 3B",
        provider: "Ollama",
        description: "Local & private",
        icon: "⚡",
    },
    {
        id: "groq",
        name: "GPT-OSS 120B",
        provider: "Groq",
        description: "Open-weight beast",
        icon: "◆",
    },
    {
        id: "mistral",
        name: "Ministral 3B",
        provider: "Mistral",
        description: "Small but mighty",
        icon: "◈",
    },
];

const BENCHMARKS = [
    {
        id: "consistency",
        title: "Consistency",
        description: "Does it stay consistent?",
        icon: <FaSyncAlt />,
    },
    {
        id: "hallucination",
        title: "Hallucination Resistance",
        description: "Can it avoid making things up?",
        icon: <FaExclamationTriangle />,
    },
    {
        id: "information_decay",
        title: "Information Retention",
        description: "What survives over time?",
        icon: <FaBrain />,
    },
    {
        id: "prompt_robustness",
        title: "Prompt Robustness",
        description: "Try to break the prompt.",
        icon: <FaShieldAlt />,
    },
];

const BENCHMARK_LABELS = {
    consistency: "Consistency",
    hallucination: "Hallucination",
    information_decay: "Information Retention",
    prompt_robustness: "Prompt Robustness",
};

function formatScore(score) {
    if (typeof score !== "number") {
        return 0;
    }

    return score > 1 ? score : score * 100;
}

function formatLatency(latency) {
    if (typeof latency !== "number") {
        return "—";
    }

    return `${latency.toFixed(2)}s`;
}

function isFailedReport(report) {
    return report?.status === "failed";
}

function getResultSummary(reports = []) {

    const failedReports = reports.filter(isFailedReport);

    const successfulReports = reports.filter(
        (report) => !isFailedReport(report)
    );

    if (failedReports.length === reports.length) {
        return {
            title: "The experiment hit a snag.",
            description: "None of the selected benchmarks completed successfully.",
            type: "failed",
        };
    }

    if (failedReports.length > 0) {
        return {
            title: "The experiment returned mixed results.",
            description: "Some benchmarks completed while others encountered errors.",
            type: "mixed",
        };
    }

    return {
        title: "The model survived.",
        description: "All selected benchmarks completed successfully.",
        type: "success",
    };
}

function Benchmark() {
    const [selectedModel, setSelectedModel] = useState("gemini");

    const [selectedBenchmarks, setSelectedBenchmarks] = useState(
        BENCHMARKS.map((benchmark) => benchmark.id)
    );

    const [inputText, setInputText] = useState("");

    const [isRunning, setIsRunning] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState("");

    const selectedModelData = MODELS.find(
        (model) => model.id === selectedModel
    );

    const toggleBenchmark = (benchmarkId) => {
        if (isRunning) {
            return;
        }

        setSelectedBenchmarks((current) =>
            current.includes(benchmarkId)
                ? current.filter((id) => id !== benchmarkId)
                : [...current, benchmarkId]
        );
    };

    const runBenchmark = async () => {
    if (!inputText.trim()) {
        setError("Give the model something to work with first.");
        return;
    }

    if (selectedBenchmarks.length === 0) {
        setError("Pick at least one pressure test.");
        return;
    }

    setError("");
    setResults(null);
    setIsRunning(true);

    try {
        const response = await client.post("/benchmark", {
            text: inputText.trim(),
            models: [selectedModel],
            benchmarks: selectedBenchmarks,
        });

        setResults(response.data.results);
    } catch (err) {
        console.error("Benchmark execution failed:", err);

        const message =
            err.response?.data?.detail ||
            err.response?.data?.message ||
            err.message ||
            "Something went wrong while running the experiment.";

        setError(message);
    } finally {
        setIsRunning(false);
    }
};

    const getModelResult = () => {
        if (!results) {
            return null;
        }

        /*
         * Backend returns:
         * {
         *   model_name: {
         *      benchmark_reports: [],
         *      overall_reliability: {}
         *   }
         * }
         */

        return (
            results[selectedModel] ||
            results.results?.[selectedModel] ||
            Object.values(results)[0]
        );
    };

    const modelResult = getModelResult();

    const reports = modelResult?.benchmark_reports || [];

    const failedReports = reports.filter(isFailedReport);

    const successfulReports = reports.filter(
        (report) => !isFailedReport(report)
    );

    const resultSummary = getResultSummary(reports);

    const hasSuccessfulReports = successfulReports.length > 0;

    const overallScore = hasSuccessfulReports
        ? (
            modelResult?.overall_reliability?.overall_score ??
            modelResult?.overall_score ??
            null
        )
        : null;
    const resetExperiment = () => {
        setResults(null);
        setError("");
    };

    return (
        <Layout>
            <div className="benchmark-page">

                {/* =========================
                    HERO
                ========================== */}

                {!results && !isRunning && (
                    <section className="benchmark-hero">
                        <div>
                            <div className="benchmark-eyebrow">
                                <FaFlask />
                                BENCHMARK LAB
                            </div>

                            <h1>
                                How reliable is your model...
                                <span> really?</span>
                            </h1>

                            <p>
                                Put your language model under pressure and see
                                what actually survives the experiment.
                            </p>
                        </div>

                        <div className="experiment-status">
                            <span className="status-pulse"></span>
                            <span>LAB READY</span>
                        </div>
                    </section>
                )}

                {/* =========================
                    RUNNING STATE
                ========================== */}

                {isRunning && (
                    <section className="experiment-running">

                        <div className="running-header">
                            <div className="running-icon">
                                <FaFlask />
                            </div>

                            <div>
                                <div className="benchmark-eyebrow">
                                    EXPERIMENT IN PROGRESS
                                </div>

                                <h1>
                                    Putting{" "}
                                    <span>
                                        {selectedModelData?.name}
                                    </span>{" "}
                                    under pressure.
                                </h1>

                                <p>
                                    Running {selectedBenchmarks.length}{" "}
                                    reliability test
                                    {selectedBenchmarks.length !== 1
                                        ? "s"
                                        : ""}
                                    . This may take a moment.
                                </p>
                            </div>
                        </div>

                        <div className="experiment-console">

                            <div className="console-header">
                                <span>
                                    RELIABILITY EXPERIMENT
                                </span>

                                <span className="console-live">
                                    ● LIVE
                                </span>
                            </div>

                            <div className="console-model">
                                <div className="console-model-symbol">
                                    {selectedModelData?.icon}
                                </div>

                                <div>
                                    <strong>
                                        {selectedModelData?.name}
                                    </strong>
                                    <span>
                                        {selectedModelData?.provider}
                                    </span>
                                </div>
                            </div>

                            <div className="running-tests">
                                {BENCHMARKS.filter((benchmark) =>
                                    selectedBenchmarks.includes(
                                        benchmark.id
                                    )
                                ).map((benchmark, index) => (
                                    <div
                                        className="running-test"
                                        key={benchmark.id}
                                    >
                                        <div className="running-test-icon">
                                            {benchmark.icon}
                                        </div>

                                        <div className="running-test-info">
                                            <strong>
                                                {benchmark.title}
                                            </strong>

                                            <span>
                                                {index === 0
                                                    ? "Analyzing model response..."
                                                    : "Queued for evaluation"}
                                            </span>
                                        </div>

                                        <div className="running-test-state">
                                            {index === 0 ? (
                                                <span className="analyzing">
                                                    ANALYZING
                                                </span>
                                            ) : (
                                                <span className="queued">
                                                    QUEUED
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="console-footer">
                                <span>
                                    <FaClock />
                                    Benchmark engine running
                                </span>

                                <span>
                                    "Let's see what breaks first."
                                </span>
                            </div>
                        </div>
                    </section>
                )}

                {/* =========================
                    INPUT FORM
                ========================== */}

                {!isRunning && !results && (
                    <>
                        {/* MODEL */}
                        <section className="benchmark-section">
                            <div className="section-title-row">
                                <div>
                                    <span className="section-number">
                                        01
                                    </span>

                                    <div>
                                        <h2>
                                            Choose your test subject
                                        </h2>

                                        <p>
                                            Pick the model you want to put
                                            through the reliability lab.
                                        </p>
                                    </div>
                                </div>
                            </div>

                            <div className="model-grid">
                                {MODELS.map((model) => (
                                    <button
                                        key={model.id}
                                        type="button"
                                        disabled={isRunning}
                                        className={`model-card ${
                                            selectedModel === model.id
                                                ? "model-card-selected"
                                                : ""
                                        }`}
                                        onClick={() =>
                                            setSelectedModel(model.id)
                                        }
                                    >
                                        <div className="model-card-top">
                                            <div className="model-symbol">
                                                {model.icon}
                                            </div>

                                            <div
                                                className={`selection-indicator ${
                                                    selectedModel ===
                                                    model.id
                                                        ? "selected"
                                                        : ""
                                                }`}
                                            >
                                                {selectedModel ===
                                                    model.id && (
                                                    <FaCheckCircle />
                                                )}
                                            </div>
                                        </div>

                                        <div className="model-info">
                                            <span className="model-provider">
                                                {model.provider}
                                            </span>

                                            <h3>{model.name}</h3>

                                            <p>
                                                {model.description}
                                            </p>
                                        </div>

                                        <FaChevronRight className="model-arrow" />
                                    </button>
                                ))}
                            </div>
                        </section>

                        {/* BENCHMARKS */}
                        <section className="benchmark-section">
                            <div className="section-title-row">
                                <div>
                                    <span className="section-number">
                                        02
                                    </span>

                                    <div>
                                        <h2>Pressure tests</h2>

                                        <p>
                                            Select the ways you want to
                                            challenge the model.
                                        </p>
                                    </div>
                                </div>

                                <span className="selection-count">
                                    {selectedBenchmarks.length} /{" "}
                                    {BENCHMARKS.length} selected
                                </span>
                            </div>

                            <div className="pressure-grid">
                                {BENCHMARKS.map((benchmark) => {
                                    const selected =
                                        selectedBenchmarks.includes(
                                            benchmark.id
                                        );

                                    return (
                                        <button
                                            key={benchmark.id}
                                            type="button"
                                            className={`pressure-card ${
                                                selected
                                                    ? "pressure-card-selected"
                                                    : ""
                                            }`}
                                            onClick={() =>
                                                toggleBenchmark(
                                                    benchmark.id
                                                )
                                            }
                                        >
                                            <div className="pressure-icon">
                                                {benchmark.icon}
                                            </div>

                                            <div className="pressure-content">
                                                <div className="pressure-heading">
                                                    <h3>
                                                        {benchmark.title}
                                                    </h3>

                                                    {selected && (
                                                        <FaCheckCircle />
                                                    )}
                                                </div>

                                                <p>
                                                    {benchmark.description}
                                                </p>
                                            </div>
                                        </button>
                                    );
                                })}
                            </div>
                        </section>

                        {/* INPUT */}
                        <section className="benchmark-section">
                            <div className="section-title-row">
                                <div>
                                    <span className="section-number">
                                        03
                                    </span>

                                    <div>
                                        <h2>Drop your challenge</h2>

                                        <p>
                                            Give the model something worth
                                            testing.
                                        </p>
                                    </div>
                                </div>

                                <span className="character-count">
                                    {inputText.length} / 5000
                                </span>
                            </div>

                            <div className="challenge-card">
                                <div className="challenge-toolbar">
                                    <div className="toolbar-status">
                                        <span></span>
                                        INPUT READY
                                    </div>

                                    <span>
                                        {selectedModelData?.name}
                                    </span>
                                </div>

                                <textarea
                                    value={inputText}
                                    onChange={(event) =>
                                        setInputText(
                                            event.target.value.slice(
                                                0,
                                                5000
                                            )
                                        )
                                    }
                                    placeholder="Paste a question, claim, paragraph, or anything you want to put under pressure..."
                                    maxLength={5000}
                                />

                                <div className="challenge-footer">
                                    <span>
                                        Tip: harder questions make better
                                        experiments.
                                    </span>

                                    <FaLayerGroup />
                                </div>
                            </div>
                        </section>

                        {/* ERROR */}
                        {error && (
                            <div className="benchmark-error">
                                <FaExclamationTriangle />
                                <span>{error}</span>
                            </div>
                        )}

                        {/* LAUNCH */}
                        <section className="experiment-launch">
                            <div className="launch-info">
                                <div className="launch-icon">
                                    <FaFire />
                                </div>

                                <div>
                                    <h3>
                                        Ready to run the experiment?
                                    </h3>

                                    <p>
                                        {selectedModelData?.name} ·{" "}
                                        {selectedBenchmarks.length} pressure
                                        test
                                        {selectedBenchmarks.length !== 1
                                            ? "s"
                                            : ""}
                                    </p>
                                </div>
                            </div>

                            <button
                                type="button"
                                className="run-experiment-btn"
                                disabled={
                                    isRunning ||
                                    !inputText.trim() ||
                                    selectedBenchmarks.length === 0
                                }
                                onClick={runBenchmark}
                            >
                                {isRunning ? (
                                    <>
                                        <FaSyncAlt className="button-spinner" />
                                        Running experiment...
                                    </>
                                ) : (
                                    <>
                                        <FaBolt />
                                        Run the experiment
                                    </>
                                )}
                            </button>
                        </section>
                    </>
                )}

                {/* =========================
                    RESULTS
                ========================== */}

                {!isRunning && results && (
                    <section className="benchmark-results">

                        <div className="results-header">
                            <div>
                                <div className="benchmark-eyebrow">
                                    <FaTrophy />
                                    EXPERIMENT COMPLETE
                                </div>

                                <div
                                    className={`result-summary result-summary-${resultSummary.type}`}
                                >

                                    <h1>
                                        {resultSummary.title}
                                    </h1>

                                    <p>
                                        {resultSummary.description}
                                    </p>

                                </div>

                                <p>
                                    Reliability analysis for{" "}
                                    {selectedModelData?.name}.
                                </p>
                            </div>

                            <button
                                type="button"
                                className="new-experiment-btn"
                                onClick={resetExperiment}
                            >
                                <FaRedo />
                                New experiment
                            </button>
                        </div>

                        <div className="results-overview">

                            <div className="overall-score-card">
                                <div className="score-card-label">
                                    OVERALL RELIABILITY
                                </div>

                                <div className="overall-score">
                                    {overallScore !== null
                                        ? Math.round(
                                              overallScore
                                          )
                                        : "—"}
                                    <span>/100</span>
                                </div>

                                <div className="score-verdict">

                                    {overallScore === null
                                        ? "Score unavailable"
                                        : overallScore >= 85
                                        ? "Highly reliable"
                                        : overallScore >= 70
                                        ? "Mostly reliable"
                                        : overallScore >= 50
                                        ? "Needs attention"
                                        : "Under pressure"}

                                </div>
                            </div>

                            <div className="result-model-card">
                                <div className="result-model-symbol">
                                    {selectedModelData?.icon}
                                </div>

                                <div>
                                    <span>TEST SUBJECT</span>
                                    <h3>
                                        {selectedModelData?.name}
                                    </h3>
                                    <p>
                                        {selectedModelData?.provider}
                                    </p>
                                </div>
                            </div>

                        </div>

                        <div className="results-heading">
                            <div>
                                <h2>Pressure test results</h2>
                                <p>
                                    Here's where the model held up — and
                                    where it didn't.
                                </p>
                            </div>
                        </div>

                        <div className="result-grid">

                            {reports.map((report, index) => {

                                const failed = isFailedReport(report);

                                const score = formatScore(report.score);

                                const benchmarkDefinition = BENCHMARKS.find(
                                    (benchmark) => benchmark.id === report.benchmark
                                );

                                const benchmarkLabel =
                                    BENCHMARK_LABELS[report.benchmark] ||
                                    report.benchmark;

                                const latency =
                                    report.latency ??
                                    report.average_latency;

                                return (

                                    <div
                                        className={`result-card ${
                                            failed ? "result-card-failed" : ""
                                        }`}
                                        key={`${report.benchmark}-${index}`}
                                    >

                                        <div className="result-card-top">

                                            <div className="result-card-icon">

                                                {benchmarkDefinition?.icon}

                                            </div>

                                            <span
                                                className={`result-check ${
                                                    failed ? "result-status-failed" : ""
                                                }`}
                                            >

                                                {failed ? (
                                                    <FaExclamationTriangle />
                                                ) : (
                                                    <FaCheckCircle />
                                                )}

                                            </span>

                                        </div>

                                        <span className="result-card-label">

                                            {benchmarkLabel}

                                        </span>

                                        <div className="result-score">

                                            {failed ? "—" : Math.round(score)}

                                            {!failed && <span>%</span>}

                                        </div>

                                        {!failed && (

                                            <div className="result-progress">

                                                <div
                                                    style={{
                                                        width: `${Math.min(
                                                            Math.max(score, 0),
                                                            100
                                                        )}%`,
                                                    }}
                                                ></div>

                                            </div>

                                        )}

                                        {failed && (

                                            <div className="result-error">

                                                <strong>
                                                    Benchmark failed
                                                </strong>

                                                <p>
                                                    {report.error ||
                                                        "This benchmark could not be completed."}
                                                </p>

                                            </div>

                                        )}

                                        <div className="result-latency">

                                            <FaClock />

                                            {failed
                                                ? "—"
                                                : formatLatency(latency)}

                                        </div>

                                    </div>

                                );

                            })}

                        </div>

                        {reports.length === 0 && (
                            <div className="empty-results">
                                <FaFlask />
                                <h3>
                                    The experiment returned no benchmark
                                    reports.
                                </h3>
                                <p>
                                    Check the backend response and try again.
                                </p>
                            </div>
                        )}

                    </section>
                )}
            </div>
        </Layout>
    );
}

export default Benchmark;