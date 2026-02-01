import { BrowserRouter, Routes, Route } from "react-router-dom";
import CreatePaper from "./components/create_paper";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* HOME ROUTE */}
        <Route path="/" element={<CreatePaper />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
