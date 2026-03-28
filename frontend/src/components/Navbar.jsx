import { useState } from "react";
import { useNavigate, useLocation, NavLink } from "react-router-dom";
import { logout } from "../services/authService";

function Navbar({ theme, onToggleTheme }) {
    const navigate = useNavigate();
    const location = useLocation();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const userName = localStorage.getItem("userName") || "User";
    const initials = userName.slice(0, 2).toUpperCase();

    const handleLogout = () => {
        logout();
        navigate("/auth");
    };

    const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
    const closeMenu = () => setIsMenuOpen(false);

    const isActive = (path) => location.pathname === path || location.pathname.startsWith(path + "/");

    return (
        <nav className={`navbar ${isMenuOpen ? "menu-open" : ""}`}>
            <NavLink to="/dashboard" className="navbar-logo" onClick={closeMenu}>Questify</NavLink>

            <button className="menu-toggle" onClick={toggleMenu} aria-label="Toggle menu">
                <span className="hamburger"></span>
            </button>

            <div className={`navbar-links ${isMenuOpen ? "show" : ""}`}>
                <NavLink to="/dashboard" className={`navbar-link ${isActive("/dashboard") ? "active" : ""}`} onClick={closeMenu}>
                    📋 <span className="link-text">Dashboard</span>
                </NavLink>
                <NavLink to="/create-paper" className={`navbar-link ${isActive("/create-paper") ? "active" : ""}`} onClick={closeMenu}>
                    ✏️ <span className="link-text">Create Paper</span>
                </NavLink>
                <NavLink to="/config" className={`navbar-link ${isActive("/config") ? "active" : ""}`} onClick={closeMenu}>
                    ⚙️ <span className="link-text">Configure</span>
                </NavLink>

                {/* Mobile-only logout */}
                <button className="navbar-link mobile-only logout-mobile" onClick={handleLogout}>
                    🚪 <span className="link-text">Sign Out</span>
                </button>
            </div>

            <div className="navbar-right">
                <button className="theme-toggle" onClick={onToggleTheme} title="Toggle theme">
                    {theme === "dark" ? "☀️" : "🌙"}
                </button>
                <div className="navbar-user">
                    <div className="avatar">{initials}</div>
                    <span className="user-name">{userName}</span>
                </div>
                <button className="btn-logout desktop-only" onClick={handleLogout}>
                    Sign Out
                </button>
            </div>
        </nav>
    );
}

export default Navbar;
