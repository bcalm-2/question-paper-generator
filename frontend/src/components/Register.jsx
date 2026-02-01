
import { useState } from "react";

function Register({ switchToLogin }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "Teacher",
  });

  const [error, setError] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    if (!form.name || !form.email || !form.password) {
      setError("All fields are required");
      return;
    }

    setError("");
    console.log("Register Data:", form);

  };

  return (
    <div className="auth-card animate-fade-in">
      <form className="glass-card" onSubmit={handleRegister}>
        <h2 className="title">Create Account</h2>

        {error && (
          <div className="error-msg">
            <span>⚠️</span> {error}
          </div>
        )}

        <div className="form-group">
          <input
            type="text"
            placeholder="Full Name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
        </div>

        <div className="form-group">
          <input
            type="email"
            placeholder="Email Address"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </div>

        <div className="form-group">
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
        </div>

        <button type="submit" className="btn-primary">
          Sign Up
        </button>

        <p className="text-center mt-4">
          <span className="text-muted" style={{ color: 'var(--text-muted)' }}>Already have an account? </span>
          <span className="text-link" onClick={switchToLogin}>
            Log in
          </span>
        </p>
      </form>
    </div>
  );
}

export default Register;
