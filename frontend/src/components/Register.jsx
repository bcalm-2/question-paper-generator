import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../services/authService";

function Register({ switchToLogin, theme, onToggleTheme }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  /**
   * Orchestrates the registration flow: validation -> API call -> Navigation.
   */
  const handleRegister = async (e) => {
    e.preventDefault();

    // Basic Client-side validation: Ensure all required fields are populated
    if (!form.name || !form.email || !form.password) {
      setError("All fields are required");
      return;
    }

    setError("");
    setLoading(true);

    try {
      // API call via authService; handles password hashing and DB insertion on backend
      await register(form);
      // Redirect to dashboard on successful account creation
      navigate("/dashboard");
    } catch (err) {
      // Extract error message from backend response if available
      setError(err.error || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Higher-order function for clean state updates across multiple form fields
  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  return (
    <div className="auth-wrapper">
      {/* Left brand panel */}
      <div className="auth-brand">
        <div className="auth-brand-logo">Questify</div>
        <p className="auth-brand-tagline">
          Join thousands of educators automating question paper creation with AI.
        </p>
        <div className="auth-brand-features">
          {[
            { icon: "📚", text: "5 subjects pre-configured" },
            { icon: "🎯", text: "Bloom's level targeting" },
            { icon: "📥", text: "Upload your own reference files" },
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
            <h2 style={{ fontSize: "1.4rem", marginBottom: "0.2rem" }}>Create account</h2>
            <p className="text-muted" style={{ fontSize: "0.875rem" }}>Start generating papers in minutes</p>
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

        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input type="text" placeholder="Srashti Dwivedi" value={form.name} onChange={update("name")} autoComplete="name" />
          </div>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input type="email" placeholder="you@example.com" value={form.email} onChange={update("email")} autoComplete="email" />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input type="password" placeholder="Min. 8 characters" value={form.password} onChange={update("password")} autoComplete="new-password" />
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
            style={{ marginTop: "1rem" }}
          >
            {loading ? "Creating account…" : "Create Account →"}
          </button>
        </form>

        <p className="text-center mt-md" style={{ fontSize: "0.875rem" }}>
          <span className="text-muted">Already have an account? </span>
          <span className="text-link" onClick={switchToLogin}>Sign in</span>
        </p>
      </div>
    </div>
  );
}

export default Register;
