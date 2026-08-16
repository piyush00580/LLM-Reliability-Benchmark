import { useEffect, useState } from "react";
import axios from "axios";
import Layout from "../components/layout/Layout";
import "./Reports.css";

function Reports() {

    const [runs, setRuns] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

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

                                {runs.map((run) => (

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

                    </div>

                )}

            </div>

        </Layout>

    );
}

export default Reports;