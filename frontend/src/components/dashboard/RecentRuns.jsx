import "./Dashboard.css";

function RecentRuns({ runs }) {

    return (

        <div className="table-card">

            <h3>Recent Benchmark Runs</h3>

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

                    {runs.length === 0 ? (

                        <tr>
                            <td colSpan="5">
                                No benchmark runs yet.
                            </td>
                        </tr>

                    ) : (

                        runs.map((run) => (

                            <tr key={run.id}>

                                <td>
                                    {run.model}
                                </td>

                                <td>
                                    {run.benchmark}
                                </td>

                                <td>
                                    {run.score}%
                                </td>

                                <td>
                                    {run.latency}s
                                </td>

                                <td>
                                    {run.timestamp}
                                </td>

                            </tr>

                        ))

                    )}

                </tbody>

            </table>

        </div>

    );
}

export default RecentRuns;