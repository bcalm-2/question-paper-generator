import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function PaperList() {
  const [papers, setPapers] = useState([]);

  // Dummy fetch (replace with backend API)
  useEffect(() => {
    const dummyPapers = [
      { id: 1, title: "Math Paper 1", date: "2026-01-20" },
      { id: 2, title: "Physics Paper 1", date: "2026-01-21" },
    ];
    setPapers(dummyPapers);
  }, []);

  return (
    <div>
      <h2>Generated Papers</h2>
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Title</th>
            <th>Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {papers.map((paper) => (
            <tr key={paper.id}>
              <td>{paper.title}</td>
              <td>{paper.date}</td>
              <td>
                <Link to={`/paper/${paper.id}`}>View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PaperList;
