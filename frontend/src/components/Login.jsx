
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/authService";

function Login({ switchToRegister }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError("All fields are required");
      return;
    }

    setError("");
    setError("");

    try {
      await login({ email, password });
      navigate("/dashboard");
    } catch (err) {
      setError(err.error || "Login failed. Please try again.");
    }
  };

  return (
    <div className="auth-card animate-fade-in">
      <form className="glass-card" onSubmit={handleLogin}>
        <h2 className="title">Welcome Back</h2>

        {error && (
          <div className="error-msg">
            <span>⚠️</span> {error}
          </div>
        )}

        <div className="form-group">
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="form-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit" className="btn-primary">
          Sign In
        </button>

        <p className="text-center mt-4">
          <span className="text-muted" style={{ color: 'var(--text-muted)' }}>New here? </span>
          <span className="text-link" onClick={switchToRegister}>
            Create an account
          </span>
        </p>
      </form>
    </div>
  );
}

export default Login;
