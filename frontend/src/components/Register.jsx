
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
    <form className="card" onSubmit={handleRegister}>
      <h2>Register</h2>

      {error && <p className="error">{error}</p>}

      <input
        type="text"
        placeholder="Name"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />

      <input
        type="email"
        placeholder="Email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />

      <input
        type="password"
        placeholder="Password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />

      <select
        value={form.role}
        onChange={(e) => setForm({ ...form, role: e.target.value })}
      >
        <option value="Teacher">Teacher</option>
      </select>

      <button type="submit">Register</button>

      <p>
        Already have an account?{" "}
        <span onClick={switchToLogin}>Login</span>
      </p>
    </form>
  );
}

export default Register;
