import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import "./Reports.css";

function Reports() {

    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [selectedModel, setSelectedModel] = useState("All");
    const [selectedBenchmark, setSelectedBenchmark] = useState("All");

    useEffect(() => {

        const fetchHistory = async () => {

            try {

                const response = await axios.get(
                    "http://127.0.0.1:5000/api/history"
                );

                setRuns(response.data.runs);

            } catch (err) {

                console.error(err);
                setError("Could not load benchmark history.");

            } finally {

                setLoading(false);

            }
        };

        fetchHistory();

    }, []);

    const models = [
        "All",
        ...new Set(runs.map((run) => run.model))
    ];

    const benchmarks = [
        "All",
        ...new Set(runs.map((run) => run.benchmark))
    ];

    const filteredRuns = runs.filter((run) => {

        const modelMatch =
            selectedModel === "All" ||
            run.model === selectedModel;

        const benchmarkMatch =
            selectedBenchmark === "All" ||
            run.benchmark === selectedBenchmark;

        return modelMatch && benchmarkMatch;
    });

    const resetFilters = () => {
        setSelectedModel("All");
        setSelectedBenchmark("All");
    };

    return (

        <Layout>

            <div className="reports-container">

                <h1>Reports</h1>

                {loading && (
                    <p>Loading benchmark history...</p>
                )}

                {error && (
                    <p className="error-message">
                        {error}
                    </p>
                )}

                {!loading && !error && runs.length === 0 && (
                    <p>No benchmark runs found.</p>
                )}

                {!loading && !error && runs.length > 0 && (

                    <div className="reports-card">

                        <h2>Benchmark History</h2>

                        <button
                            className="export-csv-button"
                            onClick={() => {

                                const params = new URLSearchParams();

                                if (selectedModel !== "All") {
                                    params.append("model", selectedModel);
                                }

                                if (selectedBenchmark !== "All") {
                                    params.append("benchmark", selectedBenchmark);
                                }

                                const queryString = params.toString();

                                const url =
                                    "http://127.0.0.1:5000/api/export/csv" +
                                    (queryString ? `?${queryString}` : "");

                                window.open(url, "_blank");
                            }}
                        >
                            Export CSV
                        </button>

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
                                            {model}
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
                                            {benchmark}
                                        </option>
                                    ))}

                                </select>

                            </div>

                            <button
                                className="reset-filter-button"
                                onClick={resetFilters}
                            >
                                Reset Filters
                            </button>

                        </div>

                        <p className="results-count">
                            Showing {filteredRuns.length} of {runs.length} runs
                        </p>

                        {filteredRuns.length === 0 ? (

                            <p>
                                No runs match the selected filters.
                            </p>

                        ) : (

                            <table>

                                <thead>

                                    <tr>
                                        <th>Model</th>
                                        <th>Benchmark</th>
                                        <th>Score</th>
                                        <th>Latency</th>
                                        <th>Timestamp</th>
                                    </tr>

                                </thead>

                                <tbody>

                                    {filteredRuns.map((run) => (

                                        <tr key={run.id}>

                                            <td>{run.model}</td>

                                            <td>{run.benchmark}</td>

                                            <td>
                                                {Math.round(run.score * 100)}%
                                            </td>

                                            <td>
                                                {run.latency}s
                                            </td>

                                            <td>
                                                {run.timestamp}
                                            </td>

                                        </tr>

                                    ))}

                                </tbody>

                            </table>

                        )}

                    </div>

                )}

            </div>

        </Layout>
    );
}

export default Reports;