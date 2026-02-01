import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import CreatePaper from "./components/Paper";
import "./App.css";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <BrowserRouter>
      <div className="app-container">
        <Routes>
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

          <Route path="/" element={<CreatePaper />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
