import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePaper from "./pages/CreatePaper";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/create-paper" element={<CreatePaper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
