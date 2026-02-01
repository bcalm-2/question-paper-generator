import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePaper from "./components/create_paper";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import "./App.css";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <BrowserRouter>
      <Routes>
        {<div className="container">
               {isLogin ? (
                 <Login switchToRegister={() => setIsLogin(false)} />
               ) : (
                 <Register switchToLogin={() => setIsLogin(true)} />
               )}
             </div>}
        <Route path="/" element={<CreatePaper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
