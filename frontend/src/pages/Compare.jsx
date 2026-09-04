import { useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import "./Compare.css";

const benchmarkDisplayNames = {
    consistency: "Consistency",
    hallucination: "Hallucination",
    information_decay: "Information Retention",
    prompt_robustness: "Prompt Robustness",
};


const normalizeBenchmark = (value) => {
    return String(value || "")
        .toLowerCase()
        .replace(/[\s_-]+/g, "")
        .trim();
};


function Compare() {

    const [models, setModels] = useState({
        mock_poor: false,
        mock_average: false,
        mock_excellent: false,
        gemini: false,
        ollama: true,
    });

    const [benchmarks, setBenchmarks] = useState({
        consistency: true,
        hallucination: true,
        information_decay: true,
        prompt_robustness: true,
    });

    const [text, setText] = useState("");

    const [results, setResults] = useState(null);

    const [loading, setLoading] = useState(false);


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


    const compareModels = async () => {

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


        if (selectedModels.length < 2) {

            alert("Please select at least two models.");

            return;
        }


        if (selectedBenchmarks.length === 0) {

            alert("Please select at least one benchmark.");

            return;
        }


        try {

            setLoading(true);

            setResults(null);


            const response = await axios.post(
                "http://127.0.0.1:5000/api/compare",
                {
                    text,
                    models: selectedModels,
                    benchmarks: selectedBenchmarks,
                }
            );


            console.log(
                            "COMPARE RESPONSE JSON:",
                            JSON.stringify(response.data, null, 2)
            );


            setResults(response.data);


        } catch (error) {

            console.error("Comparison error:", error);

            alert("Comparison failed.");

        } finally {

            setLoading(false);

        }

    };


    return (

        <Layout>

            <div className="compare-container">

                <h1>Compare Models</h1>


                {/* MODELS */}

                <div className="compare-card">

                    <h2>Models</h2>

                    <div className="compare-grid">

                        <label>

                            <input
                                type="checkbox"
                                checked={models.mock_poor}
                                onChange={() =>
                                    toggleModel("mock_poor")
                                }
                            />

                            Mock Poor

                        </label>


                        <label>

                            <input
                                type="checkbox"
                                checked={models.mock_average}
                                onChange={() =>
                                    toggleModel("mock_average")
                                }
                            />

                            Mock Average

                        </label>


                        <label>

                            <input
                                type="checkbox"
                                checked={models.mock_excellent}
                                onChange={() =>
                                    toggleModel("mock_excellent")
                                }
                            />

                            Mock Excellent

                        </label>

                        <label>

                            <input
                                type="checkbox"
                                checked={models.gemini}
                                onChange={() =>
                                    toggleModel("gemini")
                                }
                            />

                            Gemini

                        </label>


                        <label>

                            <input
                                type="checkbox"
                                checked={models.ollama}
                                onChange={() =>
                                    toggleModel("ollama")
                                }
                            />

                            Llama 3.2 3B (Ollama)

                        </label>

                    </div>

                </div>


                {/* BENCHMARKS */}

                <div className="compare-card">

                    <h2>Benchmarks</h2>

                    <div className="compare-grid">

                        <label>

                            <input
                                type="checkbox"
                                checked={benchmarks.consistency}
                                onChange={() =>
                                    toggleBenchmark("consistency")
                                }
                            />

                            Consistency

                        </label>


                        <label>

                            <input
                                type="checkbox"
                                checked={benchmarks.hallucination}
                                onChange={() =>
                                    toggleBenchmark("hallucination")
                                }
                            />

                            Hallucination

                        </label>


                        <label>

                            <input
                                type="checkbox"
                                checked={benchmarks.information_decay}
                                onChange={() =>
                                    toggleBenchmark("information_decay")
                                }
                            />

                            Information Retention

                        </label>


                        <label>

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


                {/* INPUT TEXT */}

                <div className="compare-card">

                    <h2>Input Text</h2>

                    <textarea
                        value={text}
                        onChange={(e) =>
                            setText(e.target.value)
                        }
                        placeholder="Enter text to compare model reliability..."
                    />

                </div>


                {/* COMPARE BUTTON */}

                <button
                    className="compare-button"
                    onClick={compareModels}
                    disabled={loading}
                >

                    {loading
                        ? "Comparing..."
                        : "⚖️ Compare Models"}

                </button>


                {/* RESULTS */}

                {results && (

                    <div className="compare-card">

                        <h2>Comparison Results</h2>


                        <div className="comparison-table-wrapper">

                            <table className="comparison-table">

                                <thead>

                                    <tr>

                                        <th>
                                            Benchmark
                                        </th>


                                        {Object.keys(results).map(
                                            (model) => (

                                                <th key={model}>
                                                    {model}
                                                </th>

                                            )
                                        )}

                                    </tr>

                                </thead>


                                <tbody>


                                    {/* BENCHMARK ROWS */}

                                    {Object.keys(benchmarks)
                                        .filter(
                                            (benchmark) =>
                                                benchmarks[benchmark]
                                        )
                                        .map((benchmark) => {

                                            const displayName =
                                                benchmarkDisplayNames[benchmark] || benchmark;


                                            return (

                                                <tr
                                                    key={benchmark}
                                                >

                                                    <td>
                                                        {displayName}
                                                    </td>


                                                    {Object.keys(
                                                        results
                                                    ).map(
                                                        (model) => {

                                                            const modelResult =
                                                                results[
                                                                    model
                                                                ];


                                                            const reports =
                                                                modelResult?.benchmark_reports ||
                                                                [];


                                                            const report = reports.find((item) => {
                                                                const reportName = normalizeBenchmark(item?.benchmark);

                                                                const benchmarkAliases = {
                                                                    consistency: ["consistency"],
                                                                    hallucination: ["hallucination"],
                                                                    information_decay: [
                                                                        "informationdecay",
                                                                        "informationretention"
                                                                    ],
                                                                    prompt_robustness: ["promptrobustness"]
                                                                };

                                                                return benchmarkAliases[benchmark]?.includes(reportName);
                                                            });


                                                            const score =
                                                                report?.score;


                                                            return (

                                                                <td
                                                                    key={
                                                                        model
                                                                    }
                                                                >

                                                                    {score !== undefined
                                                                        && score !== null
                                                                        ? `${Math.round(score)}%`
                                                                        : "N/A"}

                                                                </td>

                                                            );

                                                        }
                                                    )}

                                                </tr>

                                            );

                                        })}


                                    {/* OVERALL ROW */}

                                    <tr className="overall-row">

                                        <td>

                                            <strong>
                                                Overall
                                            </strong>

                                        </td>


                                        {Object.keys(results).map(
                                            (model) => {

                                                const score =
                                                    results[
                                                        model
                                                    ]
                                                        ?.overall_reliability
                                                        ?.overall_score;


                                                return (

                                                    <td
                                                        key={model}
                                                    >

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

                )}

            </div>

        </Layout>

    );

}


export default Compare;