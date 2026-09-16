import "./Dashboard.css";

function StatCard({
    title,
    value,
    icon,
    color,
    description
}) {

    return (

        <div className={`stat-card stat-${color}`}>

            <div className="stat-card-top">

                <div className="stat-icon">

                    {icon}

                </div>

                <span className="stat-label">

                    {title}

                </span>

            </div>

            <div className="stat-value">

                {value}

            </div>

            <div className="stat-description">

                {description}

            </div>

        </div>

    );

}

export default StatCard;