import "./Dashboard.css";

function StatCard({ title, value, icon, color }) {
    return (
        <div className="stat-card">
            <div className="stat-icon" style={{ backgroundColor: color }}>
                {icon}
            </div>

            <div className="stat-info">
                <p>{title}</p>
                <h2>{value}</h2>
            </div>
        </div>
    );
}

export default StatCard;