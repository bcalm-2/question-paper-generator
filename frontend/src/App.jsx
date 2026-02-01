import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePaper from "./create-paper.jsx";

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
