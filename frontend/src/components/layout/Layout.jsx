import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

function Layout({ children }) {
    return (
        <div className="layout">

            <Sidebar />

            <div className="content">

                <Navbar />

                <main className="main-content">
                    {children}
                </main>

            </div>

        </div>
    );
}

export default Layout;