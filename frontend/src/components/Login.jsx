
import { useState } from "react";

function Login({ switchToRegister }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    if (!email || !password) {
      setError("All fields are required");
      return;
    }

    setError("");
    console.log("Login Data:", { email, password });

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
