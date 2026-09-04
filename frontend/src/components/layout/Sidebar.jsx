import { NavLink } from "react-router-dom";

import {
    FaChartBar,
    FaPlay,
    FaFolderOpen,
    FaBalanceScale,
    FaCog
} from "react-icons/fa";

function Sidebar() {

    return (

        <aside className="sidebar">


            <nav>

                <NavLink to="/">
                    <FaChartBar />
                    <span>Dashboard</span>
                </NavLink>

                <NavLink to="/benchmark">
                    <FaPlay />
                    <span>Benchmark</span>
                </NavLink>

                <NavLink to="/reports">
                    <FaFolderOpen />
                    <span>Reports</span>
                </NavLink>

                <NavLink to="/compare">
                    <FaBalanceScale />
                    <span>Compare</span>
                </NavLink>

                <NavLink to="/settings">
                    <FaCog />
                    <span>Settings</span>
                </NavLink>

            </nav>

        </aside>

    );

}

export default Sidebar;