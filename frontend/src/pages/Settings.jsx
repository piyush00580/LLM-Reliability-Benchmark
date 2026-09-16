import Layout from "../components/layout/Layout";

import {
    FaCog,
    FaServer,
    FaRobot,
    FaChartPie,
    FaCheckCircle,
    FaCloud,
    FaLaptopCode,
    FaInfoCircle,
} from "react-icons/fa";

import "./Settings.css";

function Settings() {

    const models = [
        {
            name: "Gemini 2.5 Flash-Lite",
            provider: "Google Gemini",
            type: "Cloud API",
            icon: <FaCloud />,
            status: "Connected",
        },
        {
            name: "Llama 3.2 3B",
            provider: "Ollama",
            type: "Local",
            icon: <FaLaptopCode />,
            status: "Local",
        },
        {
            name: "GPT-OSS 120B",
            provider: "Groq",
            type: "Cloud API",
            icon: <FaCloud />,
            status: "Connected",
        },
        {
            name: "Ministral 3B",
            provider: "Mistral",
            type: "Cloud API",
            icon: <FaCloud />,
            status: "Connected",
        },
    ];

    const benchmarks = [
        {
            name: "Consistency",
            description: "Measures whether responses remain stable.",
            weight: "25%",
        },
        {
            name: "Hallucination Resistance",
            description: "Measures whether important information is preserved without fabrication.",
            weight: "25%",
        },
        {
            name: "Information Retention",
            description: "Measures how much information survives repeated summarization.",
            weight: "25%",
        },
        {
            name: "Prompt Robustness",
            description: "Measures how reliably the model handles prompt variations.",
            weight: "25%",
        },
    ];

    return (

        <Layout>

            <div className="settings-container">

                {/* =========================
                    Header
                ========================= */}

                <section className="settings-header">

                    <div>

                        <div className="settings-eyebrow">

                            <FaCog />

                            PLATFORM CONFIGURATION

                        </div>

                        <h1>
                            Settings
                        </h1>

                        <p>
                            Inspect the configuration behind your reliability
                            experiments.
                        </p>

                    </div>

                    <div className="settings-status">

                        <span className="settings-status-dot"></span>

                        Configuration active

                    </div>

                </section>


                {/* =========================
                    Platform
                ========================= */}

                <section className="settings-section">

                    <div className="settings-section-heading">

                        <div className="section-number">
                            01
                        </div>

                        <div>

                            <h2>
                                Platform
                            </h2>

                            <p>
                                Current runtime configuration.
                            </p>

                        </div>

                    </div>


                    <div className="settings-grid">

                        <div className="settings-card">

                            <div className="settings-card-icon purple">
                                <FaServer />
                            </div>

                            <div>

                                <span className="settings-label">
                                    API Status
                                </span>

                                <strong>
                                    Online
                                </strong>

                                <small>
                                    Backend API responding normally
                                </small>

                            </div>

                        </div>


                        <div className="settings-card">

                            <div className="settings-card-icon blue">
                                <FaServer />
                            </div>

                            <div>

                                <span className="settings-label">
                                    API Base URL
                                </span>

                                <strong>
                                    localhost:5000/api
                                </strong>

                                <small>
                                    Local development environment
                                </small>

                            </div>

                        </div>


                        <div className="settings-card">

                            <div className="settings-card-icon green">
                                <FaChartPie />
                            </div>

                            <div>

                                <span className="settings-label">
                                    Reliability Weights
                                </span>

                                <strong>
                                    Equal weighting
                                </strong>

                                <small>
                                    25% assigned to each benchmark
                                </small>

                            </div>

                        </div>


                        <div className="settings-card">

                            <div className="settings-card-icon orange">
                                <FaRobot />
                            </div>

                            <div>

                                <span className="settings-label">
                                    Active Providers
                                </span>

                                <strong>
                                    4 models
                                </strong>

                                <small>
                                    Real model providers available
                                </small>

                            </div>

                        </div>

                    </div>

                </section>


                {/* =========================
                    Models
                ========================= */}

                <section className="settings-section">

                    <div className="settings-section-heading">

                        <div className="section-number">
                            02
                        </div>

                        <div>

                            <h2>
                                Model Providers
                            </h2>

                            <p>
                                Models currently available to the platform.
                            </p>

                        </div>

                    </div>


                    <div className="provider-list">

                        {models.map((model) => (

                            <div
                                className="provider-row"
                                key={model.name}
                            >

                                <div className="provider-main">

                                    <div className="provider-icon">
                                        {model.icon}
                                    </div>

                                    <div>

                                        <strong>
                                            {model.name}
                                        </strong>

                                        <span>
                                            {model.provider}
                                        </span>

                                    </div>

                                </div>


                                <div className="provider-meta">

                                    <span className="provider-type">
                                        {model.type}
                                    </span>

                                    <span className="provider-status">

                                        <FaCheckCircle />

                                        {model.status}

                                    </span>

                                </div>

                            </div>

                        ))}

                    </div>

                </section>


                {/* =========================
                    Benchmarks
                ========================= */}

                <section className="settings-section">

                    <div className="settings-section-heading">

                        <div className="section-number">
                            03
                        </div>

                        <div>

                            <h2>
                                Reliability Benchmarks
                            </h2>

                            <p>
                                Metrics contributing to the overall reliability
                                score.
                            </p>

                        </div>

                    </div>


                    <div className="benchmark-settings-list">

                        {benchmarks.map((benchmark) => (

                            <div
                                className="benchmark-setting-row"
                                key={benchmark.name}
                            >

                                <div>

                                    <strong>
                                        {benchmark.name}
                                    </strong>

                                    <p>
                                        {benchmark.description}
                                    </p>

                                </div>

                                <span className="weight-badge">
                                    {benchmark.weight}
                                </span>

                            </div>

                        ))}

                    </div>

                </section>


                {/* =========================
                    About
                ========================= */}

                <section className="settings-about">

                    <div className="about-icon">
                        <FaInfoCircle />
                    </div>

                    <div>

                        <h3>
                            LLM Reliability Benchmark Platform
                        </h3>

                        <p>
                            A model evaluation platform for measuring
                            consistency, hallucination resistance, information
                            retention and prompt robustness across multiple
                            LLM providers.
                        </p>

                        <span>
                            Local development build • Reliability Lab
                        </span>

                    </div>

                </section>

            </div>

        </Layout>
    );
}

export default Settings;