import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import CreatePaper from "./components/CreatePaper";
import Dashboard from "./components/Dashboard";
import ViewPaper from "./components/ViewPaper";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/auth" />} />

        <Route
          path="/auth"
          element={
            <div className="min-h-screen">
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
          path="/paper/:id"
          element={
            <ProtectedRoute>
              <ViewPaper />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
