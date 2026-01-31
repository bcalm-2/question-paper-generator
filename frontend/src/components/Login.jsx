
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
    <form className="card" onSubmit={handleLogin}>
      <h2>Login</h2>

      {error && <p className="error">{error}</p>}

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Login</button>

      <p>
        Don't have an account?{" "}
        <span onClick={switchToRegister}>Register</span>
      </p>
    </form>
  );
}

export default Login;
