import { useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import "./Benchmark.css";
import ResultCard from "../components/results/ResultCard";


function Benchmark() {
    const [text, setText] = useState("");

    const [models, setModels] = useState({
        mock_excellent: true,
        mock_average: false,
        mock_poor: false,
        gemini: false,
        ollama: false
    });

    const [benchmarks, setBenchmarks] = useState({
        consistency: true,
        hallucination: true,
        information_decay: false,
        prompt_robustness: false,
    });

    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const toggleModel = (name) => {
        setModels((prev) => ({
            ...prev,
            [name]: !prev[name],
        }));
    };

    const toggleBenchmark = (name) => {
        setBenchmarks((prev) => ({
            ...prev,
            [name]: !prev[name],
        }));
    };

    const runBenchmark = async () => {  

        if (!text.trim()) {
        alert("Please enter some text.");
        return;
        }

        const selectedModels = Object.keys(models).filter(
            (model) => models[model]
        );

        const selectedBenchmarks = Object.keys(benchmarks).filter(
            (benchmark) => benchmarks[benchmark]
        );

        if (selectedModels.length === 0) {
            alert("Please select at least one model.");
            return;
        }

        if (selectedBenchmarks.length === 0) {
            alert("Please select at least one benchmark.");
            return;
        }

        try {

            setLoading(true);

            const response = await axios.post(
                "http://127.0.0.1:5000/api/benchmark",
                {
                    text,
                    models: selectedModels,
                    benchmarks: selectedBenchmarks,
                },

                {
                        timeout: 600000, // 10 minutes
                }
            );

            console.log(JSON.stringify(response.data, null, 2));
            setResults(response.data);

        } catch (error) {

            console.error(error);

            alert("Benchmark failed.");

        } finally {

            setLoading(false);

        }
    };

    return (
        <Layout>
            <div className="benchmark-container">

                <h1>Benchmark</h1>

                {/* Models */}

                <div className="section-card">

                    <h3 className="section-title">
                        Available Models
                    </h3>

                    <div className="checkbox-grid">

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={models.mock_excellent}
                                onChange={() => toggleModel("mock_excellent")}
                            />
                            Mock Excellent
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={models.mock_average}
                                onChange={() => toggleModel("mock_average")}
                            />
                            Mock Average
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={models.mock_poor}
                                onChange={() => toggleModel("mock_poor")}
                            />
                            Mock Poor
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={models.gemini}
                                onChange={() => toggleModel("gemini")}
                            />
                            Gemini (Cloud)
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={models.ollama}
                                onChange={() => toggleModel("ollama")}
                            />
                            Ollama (Local)
                        </label>

                    </div>

                </div>

                {/* Benchmarks */}

                <div className="section-card">

                    <h3 className="section-title">
                        Benchmarks
                    </h3>

                    <div className="checkbox-grid">

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={benchmarks.consistency}
                                onChange={() =>
                                    toggleBenchmark("consistency")
                                }
                            />
                            Consistency
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={benchmarks.hallucination}
                                onChange={() =>
                                    toggleBenchmark("hallucination")
                                }
                            />
                            Hallucination
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={benchmarks.information_decay}
                                onChange={() =>
                                    toggleBenchmark("information_decay")
                                }
                            />
                            Information Retention
                        </label>

                        <label className="checkbox-item">
                            <input
                                type="checkbox"
                                checked={benchmarks.prompt_robustness}
                                onChange={() =>
                                    toggleBenchmark("prompt_robustness")
                                }
                            />
                            Prompt Robustness
                        </label>

                    </div>

                </div>

                {/* Input Text */}

                <div className="section-card">

                    <h3 className="section-title">
                        Input Text
                    </h3>

                    <textarea
                        className="text-input"
                        placeholder="Enter the text to benchmark..."
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                    />

                </div>

                <button
                    className="run-button"
                    onClick={runBenchmark}
                    disabled={loading}
                >
                    {loading ? "Running..." : "🚀 Run Benchmark"}
                </button>
                {results && (
                        Object.entries(results).map(([model, result]) => (
                            <ResultCard
                                key={model}
                                model={model}
                                result={result}
                            />
                        ))
                    )}

            </div>
        </Layout>
    );
}

export default Benchmark;