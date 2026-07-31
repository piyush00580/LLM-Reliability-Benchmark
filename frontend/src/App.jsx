import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Benchmark from "./pages/Benchmark";
import Reports from "./pages/Reports";
import Compare from "./pages/Compare";
import Settings from "./pages/Settings";

function App(){

    return(

        <Routes>

            <Route
                path="/"
                element={<Dashboard/>}
            />

            <Route
                path="/benchmark"
                element={<Benchmark/>}
            />

            <Route
                path="/reports"
                element={<Reports/>}
            />

            <Route
                path="/compare"
                element={<Compare/>}
            />

            <Route
                path="/settings"
                element={<Settings/>}
            />

        </Routes>

    )

}

export default App;