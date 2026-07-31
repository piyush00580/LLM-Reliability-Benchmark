import "./Dashboard.css";

function RecentRuns({ runs }) {
    return (
        <div className="table-card">
            <h3>Recent Benchmark Runs</h3>

            <table>
                <thead>
                    <tr>
                        <th>Model</th>
                        <th>Dataset</th>
                        <th>Score</th>
                        <th>Status</th>
                    </tr>
                </thead>

                <tbody>
                    {runs.map((run, index) => (
                        <tr key={index}>
                            <td>{run.model}</td>
                            <td>{run.dataset}</td>
                            <td>{run.score}%</td>
                            <td>{run.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default RecentRuns;