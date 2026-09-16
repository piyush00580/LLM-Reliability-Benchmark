import { FaCircle } from "react-icons/fa";

function Navbar() {

    return (

        <header className="navbar">

            <div>

                <h2>
                    LLM Reliability Benchmark
                </h2>

            </div>

            <div
                style={{
                    marginLeft: "auto",
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    color: "var(--text-secondary)",
                    fontSize: "12px",
                    fontWeight: 550
                }}
            >

                <FaCircle
                    style={{
                        fontSize: "7px",
                        color: "var(--success)"
                    }}
                />

                Platform Online

            </div>

        </header>

    );

}

export default Navbar;