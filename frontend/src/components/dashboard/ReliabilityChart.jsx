import {
    BarChart,
    Bar,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

import "./Dashboard.css";

function ReliabilityChart({ data }) {

    return (

        <div className="chart-card">

            <div className="chart-wrapper">

                <ResponsiveContainer
                    width="100%"
                    height={340}
                >

                    <BarChart
                        data={data}
                        margin={{
                            top: 10,
                            right: 10,
                            left: 0,
                            bottom: 10,
                        }}
                        barCategoryGap="28%"
                    >

                        <CartesianGrid
                            strokeDasharray="4 4"
                            vertical={false}
                            stroke="rgba(255,255,255,0.06)"
                        />

                        <XAxis
                            dataKey="name"
                            axisLine={false}
                            tickLine={false}
                            tick={{
                                fill: "#8f9aae",
                                fontSize: 12,
                            }}
                        />

                        <YAxis
                            domain={[0, 100]}
                            axisLine={false}
                            tickLine={false}
                            tick={{
                                fill: "#667085",
                                fontSize: 11,
                            }}
                        />

                        <Tooltip
                            cursor={{
                                fill: "rgba(124,92,255,0.05)"
                            }}
                            contentStyle={{
                                background: "#151b28",
                                border: "1px solid rgba(255,255,255,0.08)",
                                borderRadius: "10px",
                                color: "#f5f7fb",
                                boxShadow:
                                    "0 12px 30px rgba(0,0,0,0.35)"
                            }}
                            labelStyle={{
                                color: "#9aa4b6",
                                marginBottom: "4px"
                            }}
                            formatter={(value) => [
                                `${value}%`,
                                "Reliability"
                            ]}
                        />

                        <Bar
                            dataKey="score"
                            fill="#7c5cff"
                            radius={[7, 7, 0, 0]}
                            maxBarSize={70}
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>

    );

}

export default ReliabilityChart;