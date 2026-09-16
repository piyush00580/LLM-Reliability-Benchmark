import { NavLink } from "react-router-dom";

import {
    FaChartBar,
    FaPlay,
    FaFolderOpen,
    FaBalanceScale,
    FaCog
} from "react-icons/fa";

function Sidebar() {

    const navigation = [
        {
            path: "/",
            label: "Dashboard",
            icon: <FaChartBar />
        },
        {
            path: "/benchmark",
            label: "Benchmark",
            icon: <FaPlay />
        },
        {
            path: "/compare",
            label: "Compare",
            icon: <FaBalanceScale />
        },
        {
            path: "/reports",
            label: "Reports",
            icon: <FaFolderOpen />
        },
        {
            path: "/settings",
            label: "Settings",
            icon: <FaCog />
        }
    ];

    return (
        <aside className="sidebar">

            <nav>

                {navigation.map((item) => (

                    <NavLink
                        key={item.path}
                        to={item.path}
                        end={item.path === "/"}
                    >

                        {item.icon}

                        <span>
                            {item.label}
                        </span>

                    </NavLink>

                ))}

            </nav>

        </aside>
    );
}

export default Sidebar;