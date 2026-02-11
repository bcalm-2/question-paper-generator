import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import CreatePaper from "./components/CreatePaper";
import Dashboard from "./components/Dashboard";
import ViewPaper from "./components/ViewPaper";
import "./App.css";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <BrowserRouter>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<Navigate to="/auth" />} />

          <Route
            path="/auth"
            element={
              <div className="auth-container">
                {isLogin ? (
                  <Login switchToRegister={() => setIsLogin(false)} />
                ) : (
                  <Register switchToLogin={() => setIsLogin(true)} />
                )}
              </div>
            }
          />

          <Route path="/dashboard" element={<Dashboard />} />

          <Route path="/create-paper" element={<CreatePaper />} />
          <Route path="/edit-paper/:id" element={<CreatePaper />} />
          <Route path="/paper/:id" element={<ViewPaper />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
