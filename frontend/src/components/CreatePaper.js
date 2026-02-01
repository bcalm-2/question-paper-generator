import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function CreatePaper() {
  const [title, setTitle] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Call backend API to create paper
    console.log("New paper created:", title);
    navigate("/papers");
  };

  return (
    <div>
      <h2>Create New Paper</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Paper Title:
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
          />
        </label>
        <button type="submit">Create Paper</button>
      </form>
    </div>
  );
}

export default CreatePaper;
