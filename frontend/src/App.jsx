import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import "./style.css";

function App() {
  const [page, setPage] = useState("login");

  return (
    <div className="app">
      {/* NAVBAR */}
      <div className="navbar">
        <h3>ResolveNow</h3>
        <div className="nav-links">
          <span onClick={() => setPage("login")}>Login</span>
          <span onClick={() => setPage("register")}>SignUp</span>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="main-content">
        {page === "login" && <Login setPage={setPage} />}
        {page === "register" && <Register />}
        {page === "dashboard" && <Dashboard />}
      </div>

      {/* FOOTER */}
      <div className="footer">
        Home • About • Login • SignUp • Contact
      </div>
    </div>
  );
}

export default App;