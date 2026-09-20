import { useEffect, useState } from "react";

import Layout from "../components/layout/Layout";

import {
    FaDatabase,
    FaRobot,
    FaPlayCircle,
    FaChartLine,
    FaArrowUp,
    FaShieldAlt,
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

                const response = await getDashboard();

                const dashboardData = response?.data ?? response;

                setDashboard({
                    ...dashboardData,
                    recent_runs: Array.isArray(dashboardData?.recent_runs)
                        ? dashboardData.recent_runs
                        : [],
                    chart: Array.isArray(dashboardData?.chart)
                        ? dashboardData.chart
                        : [],
                });

            } catch (error) {

                console.error(
                    "Failed to load dashboard:",
                    error
                );

            }

        }

        loadDashboard();

    }, []);

    if (!dashboard) {

        return (

            <Layout>

                <div className="dashboard-loading">

                    <div className="loading-spinner"></div>

                    <p>
                        Loading reliability data...
                    </p>

                </div>

            </Layout>

        );

    }

    return (

        <Layout>

            <div className="dashboard-container">

                {/* =========================
                    Dashboard Header
                ========================= */}

                <section className="dashboard-header">

                    <div>

                        <div className="dashboard-eyebrow">

                            <FaShieldAlt />

                            MODEL EVALUATION PLATFORM

                        </div>

                        <h1>
                            Reliability Overview
                        </h1>

                        <p>
                            Monitor the reliability, consistency and
                            performance of your language models.
                        </p>

                    </div>

                    <div className="dashboard-status">

                        <span className="status-dot"></span>

                        System operational

                    </div>

                </section>


                {/* =========================
                    KPI Cards
                ========================= */}

                <section className="stats-grid">

                    <StatCard
                        title="Benchmark Runs"
                        value={dashboard.total_runs}
                        icon={<FaPlayCircle />}
                        color="purple"
                        description="Total evaluations"
                    />

                    <StatCard
                        title="Models Evaluated"
                        value={dashboard.models}
                        icon={<FaRobot />}
                        color="blue"
                        description="Active model providers"
                    />

                    <StatCard
                        title="Datasets"
                        value={dashboard.datasets}
                        icon={<FaDatabase />}
                        color="orange"
                        description="Available evaluation data"
                    />

                    <StatCard
                        title="Overall Reliability"
                        value={`${dashboard.reliability}%`}
                        icon={<FaChartLine />}
                        color="green"
                        description="Weighted reliability score"
                    />

                </section>


                {/* =========================
                    Reliability Section
                ========================= */}

                <section className="dashboard-section">

                    <div className="section-heading">

                        <div>

                            <h2>
                                Model Reliability
                            </h2>

                            <p>
                                Compare reliability scores across
                                evaluated language models.
                            </p>

                        </div>

                        <div className="section-badge">

                            <FaArrowUp />

                            Higher is better

                        </div>

                    </div>

                    <ReliabilityChart
                        data={dashboard.chart}
                    />

                </section>


                {/* =========================
                    Recent Activity
                ========================= */}

                <section className="dashboard-section">

                    <div className="section-heading">

                        <div>

                            <h2>
                                Recent Benchmark Activity
                            </h2>

                            <p>
                                Latest model evaluation runs recorded
                                by the platform.
                            </p>

                        </div>

                    </div>

                    <RecentRuns
                        runs={dashboard.recent_runs}
                    />

                </section>

            </div>

        </Layout>

    );

}

export default Dashboard;