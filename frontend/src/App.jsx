import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import CreatePaper from "./components/CreatePaper";
import Dashboard from "./components/Dashboard";
import ViewPaper from "./components/ViewPaper";
import ConfigDashboard from "./components/ConfigDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./components/Navbar";
import "./App.css";

function AuthedLayout({ theme, onToggleTheme, children }) {
  return (
    <div className="app-root">
      <Navbar theme={theme} onToggleTheme={onToggleTheme} />
      <div className="page-shell">{children}</div>
    </div>
  );
}

function App() {
  const [isLogin, setIsLogin] = useState(true);

  // Theme: read from localStorage, default to system preference
  const getInitialTheme = () => {
    const saved = localStorage.getItem("qpg-theme");
    if (saved) return saved;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  };

  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("qpg-theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === "dark" ? "light" : "dark");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" />} />

        <Route
          path="/auth"
          element={
            <div className="auth-shell animate-fade">
              {isLogin
                ? <Login switchToRegister={() => setIsLogin(false)} theme={theme} onToggleTheme={toggleTheme} />
                : <Register switchToLogin={() => setIsLogin(true)} theme={theme} onToggleTheme={toggleTheme} />
              }
            </div>
          }
        />

        <Route path="/dashboard" element={
          <ProtectedRoute>
            <AuthedLayout theme={theme} onToggleTheme={toggleTheme}>
              <Dashboard />
            </AuthedLayout>
          </ProtectedRoute>
        } />

        <Route path="/create-paper" element={
          <ProtectedRoute>
            <AuthedLayout theme={theme} onToggleTheme={toggleTheme}>
              <CreatePaper />
            </AuthedLayout>
          </ProtectedRoute>
        } />

        <Route path="/edit-paper/:id" element={
          <ProtectedRoute>
            <AuthedLayout theme={theme} onToggleTheme={toggleTheme}>
              <CreatePaper />
            </AuthedLayout>
          </ProtectedRoute>
        } />

        <Route path="/paper/:id" element={
          <ProtectedRoute>
            <AuthedLayout theme={theme} onToggleTheme={toggleTheme}>
              <ViewPaper />
            </AuthedLayout>
          </ProtectedRoute>
        } />

        <Route path="/config" element={
          <ProtectedRoute>
            <AuthedLayout theme={theme} onToggleTheme={toggleTheme}>
              <ConfigDashboard />
            </AuthedLayout>
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
