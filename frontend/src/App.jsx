import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import CreatePaper from "./components/CreatePaper";
import Dashboard from "./components/Dashboard";
import ViewPaper from "./components/ViewPaper";
import ProtectedRoute from "./components/ProtectedRoute";
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

          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/create-paper"
            element={
              <ProtectedRoute>
                <CreatePaper />
              </ProtectedRoute>
            }
          />
          <Route
            path="/edit-paper/:id"
            element={
              <ProtectedRoute>
                <CreatePaper />
              </ProtectedRoute>
            }
          />
          <Route
            path="/paper/:id"
            element={
              <ProtectedRoute>
                <ViewPaper />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
