
import {
    FaCircle,
    FaBolt
} from "react-icons/fa";

import "./Dashboard.css";

function formatModelName(model) {

    const names = {
        gemini: "Gemini 2.5 Flash-Lite",
        ollama: "Llama 3.2 3B",
        groq: "GPT-OSS 120B",
        mistral: "Ministral 3B",
    };

    return names[model] || model;

}

function RecentRuns({ runs = [] }) {

    const safeRuns = Array.isArray(runs) ? runs : [];

    return (

        <div className="table-card">

            {safeRuns.length === 0 ? (

                <div className="empty-runs">

                    <FaBolt />

                    <h3>
                        No benchmark runs yet
                    </h3>

                    <p>
                        Run your first benchmark to start
                        collecting reliability data.
                    </p>

                </div>

            ) : (

                <div className="table-container">

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

                            {safeRuns.map((run, index) => (

                                <tr key={run.id || `${run.model}-${run.benchmark}-${index}`}>

                                    <td>

                                        <div className="model-cell">

                                            <span className="model-status">
                                                <FaCircle />
                                            </span>

                                            <span>
                                                {formatModelName(run.model)}
                                            </span>

                                        </div>

                                    </td>

                                    <td>

                                        <span className="benchmark-badge">
                                            {run.benchmark}
                                        </span>

                                    </td>

                                    <td>

                                        <span className="score-value">
                                            {run.score}%
                                        </span>

                                    </td>

                                    <td>

                                        <span className="latency-value">
                                            {run.latency}s
                                        </span>

                                    </td>

                                    <td>

                                        <span className="timestamp">
                                            {run.timestamp}
                                        </span>

                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                </div>

            )}

        </div>

    );

}

export default RecentRuns;