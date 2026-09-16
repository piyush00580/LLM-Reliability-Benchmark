import { useState } from "react";
import Layout from "../components/layout/Layout";
import client from "../api/client";

import {
    FaBalanceScale,
    FaBolt,
    FaBrain,
    FaCheckCircle,
    FaExclamationTriangle,
    FaShieldAlt,
    FaSyncAlt,
    FaTrophy,
} from "react-icons/fa";

import "./Compare.css";

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

const getBenchmarkName = (benchmark) => {
    const names = {
        consistency: "Consistency",
        hallucination: "Hallucination Resistance",
        information_decay: "Information Retention",
        prompt_robustness: "Prompt Robustness",
    };

    return names[benchmark] || benchmark;
};

const normalizeBenchmark = (value) => {
    return String(value || "")
        .toLowerCase()
        .replace(/[\s_-]+/g, "")
        .trim();
};

const getModelName = (modelId) => {
    return MODELS.find((model) => model.id === modelId)?.name || modelId;
};

const getModelProvider = (modelId) => {
    return MODELS.find((model) => model.id === modelId)?.provider || "";
};

const getModelIcon = (modelId) => {
    return MODELS.find((model) => model.id === modelId)?.icon || "◆";
};

function Compare() {
    const [selectedModels, setSelectedModels] = useState([
        "gemini",
        "ollama",
    ]);

    const [selectedBenchmarks, setSelectedBenchmarks] = useState(
        BENCHMARKS.map((benchmark) => benchmark.id)
    );

    const [text, setText] = useState("");
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const toggleModel = (modelId) => {
        setSelectedModels((current) =>
            current.includes(modelId)
                ? current.filter((id) => id !== modelId)
                : [...current, modelId]
        );
    };

    const toggleBenchmark = (benchmarkId) => {
        setSelectedBenchmarks((current) =>
            current.includes(benchmarkId)
                ? current.filter((id) => id !== benchmarkId)
                : [...current, benchmarkId]
        );
    };

    const compareModels = async () => {
        setError("");

        if (!text.trim()) {
            setError("Drop some text first — the models need something to fight over.");
            return;
        }

        if (selectedModels.length < 2) {
            setError("Pick at least two models to start a comparison.");
            return;
        }

        if (selectedBenchmarks.length === 0) {
            setError("Choose at least one pressure test.");
            return;
        }

        try {
            setLoading(true);
            setResults(null);

            const response = await client.post("/compare", {
                text: text.trim(),
                models: selectedModels,
                benchmarks: selectedBenchmarks,
            });

            console.log(
                "COMPARE RESPONSE:",
                JSON.stringify(response.data, null, 2)
            );

            setResults(response.data);
        } catch (err) {
            console.error("Comparison failed:", err);

            const message =
                err.response?.data?.detail ||
                err.response?.data?.message ||
                err.message ||
                "Something went wrong while comparing the models.";

            setError(message);
        } finally {
            setLoading(false);
        }
    };

    const getReportForBenchmark = (modelResult, benchmarkId) => {
        const reports = modelResult?.benchmark_reports || [];

        return reports.find((report) => {
            const reportName = normalizeBenchmark(report?.benchmark);

            const aliases = {
                consistency: ["consistency"],
                hallucination: ["hallucination"],
                information_decay: [
                    "informationdecay",
                    "informationretention",
                ],
                prompt_robustness: ["promptrobustness"],
            };

            return aliases[benchmarkId]?.includes(reportName);
        });
    };

    const getOverallScore = (modelResult) => {
        return modelResult?.overall_reliability?.overall_score;
    };

    const getWinner = () => {
        if (!results) return null;

        const entries = Object.entries(results);

        if (!entries.length) return null;

        return entries.reduce((best, current) => {
            const currentScore =
                current[1]?.overall_reliability?.overall_score ?? -1;

            const bestScore =
                best[1]?.overall_reliability?.overall_score ?? -1;

            return currentScore > bestScore ? current : best;
        });
    };

    const winner = getWinner();

    return (
        <Layout>
            <div className="compare-page">

                {/* HEADER */}
                <section className="compare-header">
                    <div className="compare-eyebrow">
                        <FaBalanceScale />
                        MODEL SHOWDOWN
                    </div>

                    <div className="compare-header-row">
                        <div>
                            <h1>
                                Put models
                                <span> head-to-head.</span>
                            </h1>

                            <p>
                                Same challenge. Same pressure tests. Let the
                                reliability scores decide.
                            </p>
                        </div>

                        <div className="comparison-count">
                            <strong>{selectedModels.length}</strong>
                            <span>models selected</span>
                        </div>
                    </div>
                </section>

                {/* MODELS */}
                <section className="compare-section">
                    <div className="section-heading">
                        <div className="section-number">01</div>

                        <div>
                            <h2>Choose your contenders</h2>
                            <p>Who gets put under the microscope?</p>
                        </div>
                    </div>

                    <div className="model-selection-grid">
                        {MODELS.map((model) => {
                            const selected = selectedModels.includes(model.id);

                            return (
                                <button
                                    key={model.id}
                                    type="button"
                                    className={`compare-model-card ${
                                        selected ? "selected" : ""
                                    }`}
                                    onClick={() => toggleModel(model.id)}
                                >
                                    <div className="model-card-top">
                                        <div className="model-icon">
                                            {model.icon}
                                        </div>

                                        <div
                                            className={`selection-indicator ${
                                                selected ? "active" : ""
                                            }`}
                                        >
                                            {selected && <FaCheckCircle />}
                                        </div>
                                    </div>

                                    <div className="model-card-info">
                                        <span className="provider">
                                            {model.provider}
                                        </span>

                                        <h3>{model.name}</h3>

                                        <p>{model.description}</p>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </section>

                {/* BENCHMARKS */}
                <section className="compare-section">
                    <div className="section-heading">
                        <div className="section-number">02</div>

                        <div>
                            <h2>Pressure tests</h2>
                            <p>Pick the ways you want to stress them.</p>
                        </div>
                    </div>

                    <div className="benchmark-selection-grid">
                        {BENCHMARKS.map((benchmark) => {
                            const selected = selectedBenchmarks.includes(
                                benchmark.id
                            );

                            return (
                                <button
                                    key={benchmark.id}
                                    type="button"
                                    className={`benchmark-choice ${
                                        selected ? "selected" : ""
                                    }`}
                                    onClick={() =>
                                        toggleBenchmark(benchmark.id)
                                    }
                                >
                                    <div className="benchmark-choice-icon">
                                        {benchmark.icon}
                                    </div>

                                    <div>
                                        <strong>{benchmark.title}</strong>
                                        <span>{benchmark.description}</span>
                                    </div>

                                    <div className="benchmark-check">
                                        {selected && <FaCheckCircle />}
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </section>

                {/* INPUT */}
                <section className="compare-section">
                    <div className="section-heading">
                        <div className="section-number">03</div>

                        <div>
                            <h2>Give them the same challenge</h2>
                            <p>
                                Fair fight. Identical input for every model.
                            </p>
                        </div>

                        <div className="character-count">
                            {text.length} / 5000
                        </div>
                    </div>

                    <div className="compare-input-card">
                        <div className="input-status">
                            <span />
                            INPUT READY
                        </div>

                        <textarea
                            value={text}
                            onChange={(e) => {
                                if (e.target.value.length <= 5000) {
                                    setText(e.target.value);
                                }
                            }}
                            placeholder="Enter a question, claim, scenario, or piece of information worth testing..."
                        />

                        <div className="input-footer">
                            <span>
                                Tip: interesting inputs make better experiments.
                            </span>

                            <span>
                                {selectedModels.length} models ·{" "}
                                {selectedBenchmarks.length} tests
                            </span>
                        </div>
                    </div>
                </section>

                {/* ERROR */}
                {error && (
                    <div className="compare-error">
                        <FaExclamationTriangle />
                        <span>{error}</span>
                    </div>
                )}

                {/* ACTION */}
                <section className="compare-launch">
                    <div>
                        <span className="launch-label">
                            READY TO COMPARE?
                        </span>

                        <strong>
                            {selectedModels.length >= 2
                                ? `${selectedModels.length} models enter. One comes out on top.`
                                : "Select at least two models to begin."}
                        </strong>
                    </div>

                    <button
                        type="button"
                        className="compare-launch-button"
                        onClick={compareModels}
                        disabled={
                            loading ||
                            selectedModels.length < 2 ||
                            selectedBenchmarks.length === 0 ||
                            !text.trim()
                        }
                    >
                        <FaBolt />

                        {loading
                            ? "Running comparison..."
                            : "Start the showdown"}
                    </button>
                </section>

                {/* LOADING */}
                {loading && (
                    <section className="comparison-running">
                        <div className="running-spinner">
                            <FaBalanceScale />
                        </div>

                        <div>
                            <span>EXPERIMENT RUNNING</span>
                            <h2>Let’s see what breaks first.</h2>
                            <p>
                                Running identical pressure tests across{" "}
                                {selectedModels.length} models.
                            </p>
                        </div>
                    </section>
                )}

                {/* RESULTS */}
                {results && !loading && (
                    <section className="comparison-results">

                        <div className="results-header">
                            <div>
                                <div className="compare-eyebrow">
                                    <FaTrophy />
                                    COMPARISON COMPLETE
                                </div>

                                <h2>
                                    And the winner is{" "}
                                    <span>
                                        {winner
                                            ? getModelName(
                                                  selectedModels.find(
                                                      (id) =>
                                                          getModelName(id) ===
                                                          winner[0]
                                                  ) || winner[0]
                                              )
                                            : "—"}
                                        .
                                    </span>
                                </h2>

                                <p>
                                    Every model faced the same challenge and
                                    the same pressure tests.
                                </p>
                            </div>
                        </div>

                        {winner && (
                            <div className="winner-card">
                                <div className="winner-icon">
                                    <FaTrophy />
                                </div>

                                <div className="winner-info">
                                    <span>TOP RELIABILITY SCORE</span>

                                    <h3>{winner[0]}</h3>

                                    <p>
                                        {getOverallScore(winner[1])?.toFixed(
                                            1
                                        ) || "—"}
                                        /100 overall reliability
                                    </p>
                                </div>

                                <div className="winner-score">
                                    {Math.round(
                                        getOverallScore(winner[1]) || 0
                                    )}
                                </div>
                            </div>
                        )}

                        {/* SCORE CARDS */}
                        <div className="model-results-grid">
                            {Object.entries(results).map(
                                ([modelName, modelResult]) => {
                                    const score =
                                        getOverallScore(modelResult) || 0;

                                    return (
                                        <div
                                            className="model-result-card"
                                            key={modelName}
                                        >
                                            <div className="result-model-top">
                                                <div className="result-model-icon">
                                                    {getModelIcon(
                                                        selectedModels.find(
                                                            (id) =>
                                                                getModelName(
                                                                    id
                                                                ) === modelName
                                                        )
                                                    )}
                                                </div>

                                                <span>
                                                    {modelName}
                                                </span>
                                            </div>

                                            <div className="result-score">
                                                {Math.round(score)}
                                                <small>/100</small>
                                            </div>

                                            <div className="result-score-bar">
                                                <span
                                                    style={{
                                                        width: `${Math.min(
                                                            Math.max(score, 0),
                                                            100
                                                        )}%`,
                                                    }}
                                                />
                                            </div>

                                            <div className="result-verdict">
                                                {score >= 90
                                                    ? "Highly reliable"
                                                    : score >= 75
                                                    ? "Reliable"
                                                    : score >= 60
                                                    ? "Needs attention"
                                                    : "Unreliable"}
                                            </div>
                                        </div>
                                    );
                                }
                            )}
                        </div>

                        {/* TABLE */}
                        <div className="results-table-card">
                            <div className="results-table-heading">
                                <div>
                                    <span>DETAILED BREAKDOWN</span>
                                    <h3>Where each model held up</h3>
                                </div>
                            </div>

                            <div className="comparison-table-wrapper">
                                <table className="comparison-table">
                                    <thead>
                                        <tr>
                                            <th>Pressure Test</th>

                                            {Object.keys(results).map(
                                                (modelName) => (
                                                    <th key={modelName}>
                                                        {modelName}
                                                    </th>
                                                )
                                            )}
                                        </tr>
                                    </thead>

                                    <tbody>
                                        {selectedBenchmarks.map(
                                            (benchmark) => (
                                                <tr key={benchmark}>
                                                    <td>
                                                        {getBenchmarkName(
                                                            benchmark
                                                        )}
                                                    </td>

                                                    {Object.entries(
                                                        results
                                                    ).map(
                                                        ([
                                                            modelName,
                                                            modelResult,
                                                        ]) => {
                                                            const report =
                                                                getReportForBenchmark(
                                                                    modelResult,
                                                                    benchmark
                                                                );

                                                            const score =
                                                                report?.score;

                                                            return (
                                                                <td
                                                                    key={
                                                                        modelName
                                                                    }
                                                                >
                                                                    {score !==
                                                                    undefined
                                                                        ? `${Math.round(
                                                                              score
                                                                          )}%`
                                                                        : "N/A"}
                                                                </td>
                                                            );
                                                        }
                                                    )}
                                                </tr>
                                            )
                                        )}

                                        <tr className="overall-row">
                                            <td>
                                                <strong>
                                                    Overall Reliability
                                                </strong>
                                            </td>

                                            {Object.entries(results).map(
                                                ([modelName, modelResult]) => {
                                                    const score =
                                                        getOverallScore(
                                                            modelResult
                                                        );

                                                    return (
                                                        <td key={modelName}>
                                                            <strong>
                                                                {score !==
                                                                undefined
                                                                    ? `${Math.round(
                                                                          score
                                                                      )}%`
                                                                    : "N/A"}
                                                            </strong>
                                                        </td>
                                                    );
                                                }
                                            )}
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <button
                            type="button"
                            className="new-comparison-button"
                            onClick={() => {
                                setResults(null);
                                setError("");
                            }}
                        >
                            <FaBalanceScale />
                            Run another comparison
                        </button>
                    </section>
                )}
            </div>
        </Layout>
    );
}

export default Compare;