import { useEffect, useState } from "react";

import Layout from "../components/layout/Layout";

import {
    FaDatabase,
    FaRobot,
    FaPlayCircle,
    FaChartLine,
} from "react-icons/fa";

import StatCard from "../components/dashboard/StatCard";
import RecentRuns from "../components/dashboard/RecentRuns";
import ReliabilityChart from "../components/dashboard/ReliabilityChart";

import { getDashboard } from "../api/dashboardApi";

import "../components/dashboard/Dashboard.css";

function Dashboard() {

    const [dashboard, setDashboard] = useState(null);

    useEffect(() => {
        async function loadDashboard() {
            try {
                const data = await getDashboard();
                setDashboard(data);
            } catch (error) {
                console.error("Failed to load dashboard:", error);
            }
        }

        loadDashboard();
    }, []);

    if (!dashboard) {
        return (
            <Layout>
                <h2>Loading Dashboard...</h2>
            </Layout>
        );
    }

    return (
        <Layout>

            <div className="dashboard-page">

                <h1>LLM Reliability Dashboard</h1>

                <StatCard
                    title="Total Benchmarks"
                    value={dashboard.total_runs}
                    icon={<FaPlayCircle />}
                    color="#2563eb"
                />

                <StatCard
                    title="Models"
                    value={dashboard.models}
                    icon={<FaRobot />}
                    color="#16a34a"
                />

                <StatCard
                    title="Datasets"
                    value={dashboard.datasets}
                    icon={<FaDatabase />}
                    color="#ca8a04"
                />

                <StatCard
                    title="Reliability"
                    value={`${dashboard.reliability}%`}
                    icon={<FaChartLine />}
                    color="#9333ea"
                />

            </div>

            <RecentRuns runs={dashboard.recent_runs} />

            <ReliabilityChart data={dashboard.chart} />

        </Layout>
    );
}

export default Dashboard;