import { useNavigate, useLocation, NavLink } from "react-router-dom";
import { logout } from "../services/authService";

function Navbar({ theme, onToggleTheme }) {
    const navigate = useNavigate();
    const location = useLocation();
    const userName = localStorage.getItem("userName") || "User";
    const initials = userName.slice(0, 2).toUpperCase();

    const handleLogout = () => {
        logout();
        navigate("/auth");
    };

    const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + "/");

    return (
        <nav className="navbar">
            <span className="navbar-logo">Questify</span>

            <div className="navbar-links">
                <NavLink to="/dashboard" className={`navbar-link ${isActive("/dashboard") ? "active" : ""}`}>
                    📋 Dashboard
                </NavLink>
                <NavLink to="/create-paper" className={`navbar-link ${isActive("/create-paper") ? "active" : ""}`}>
                    ✏️ Create Paper
                </NavLink>
                <NavLink to="/config" className={`navbar-link ${isActive("/config") ? "active" : ""}`}>
                    ⚙️ Configure
                </NavLink>
            </div>

            <div className="navbar-right">
                <button className="theme-toggle" onClick={onToggleTheme} title="Toggle theme">
                    {theme === "dark" ? "☀️" : "🌙"}
                </button>
                <div className="navbar-user">
                    <div className="avatar">{initials}</div>
                    <span>{userName}</span>
                </div>
                <button className="btn-logout" onClick={handleLogout}>
                    Sign Out
                </button>
            </div>
        </nav>
    );
}

export default Navbar;
