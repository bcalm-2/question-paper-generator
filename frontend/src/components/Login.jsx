import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService";

function Login({ switchToRegister, theme, onToggleTheme }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email || !password) { setError("All fields are required"); return; }
    setError("");
    setLoading(true);
    try {
      await login({ email, password });
      navigate("/dashboard");
    } catch (err) {
      setError(err.error || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      {/* Left brand panel */}
      <div className="auth-brand">
        <div className="auth-brand-logo">Questify</div>
        <p className="auth-brand-tagline">
          AI-powered question paper generation for educators — fast, smart, and exam-ready.
        </p>
        <div className="auth-brand-features">
          {[
            { icon: "🧠", text: "Bloom's Taxonomy aware questions" },
            { icon: "📄", text: "One-click PDF export" },
            { icon: "⚡", text: "Generate in under 2 seconds" },
          ].map((f) => (
            <div className="auth-brand-feature" key={f.text}>
              <div className="auth-brand-feature-icon">{f.icon}</div>
              <span>{f.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Right form panel */}
      <div className="auth-form">
        <div className="flex justify-between" style={{ marginBottom: "1.75rem", alignItems: "center" }}>
          <div>
            <h2 style={{ fontSize: "1.4rem", marginBottom: "0.2rem" }}>Welcome back</h2>
            <p className="text-muted" style={{ fontSize: "0.875rem" }}>Sign in to continue</p>
          </div>
          <button className="theme-toggle" onClick={onToggleTheme} title="Toggle theme">
            {theme === "dark" ? "☀️" : "🌙"}
          </button>
        </div>

        {error && (
          <div className="alert alert-error">
            <span className="alert-icon">⚠️</span> {error}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
            style={{ marginTop: "1rem" }}
          >
            {loading ? "Signing in…" : "Sign In →"}
          </button>
        </form>

        <p className="text-center mt-md" style={{ fontSize: "0.875rem" }}>
          <span className="text-muted">New here? </span>
          <span className="text-link" onClick={switchToRegister}>Create an account</span>
        </p>
      </div>
    </div>
  );
}

export default Login;
