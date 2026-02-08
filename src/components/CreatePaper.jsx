import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

const SUBJECT_TOPICS = {
  DBMS: ["Normalization", "ER Model", "Transactions", "SQL", "Indexing", "Relational Algebra"],
  OS: ["Processes", "Memory Management", "Deadlocks", "Scheduling", "File Systems", "Virtual Memory"],
  CN: ["OSI Model", "TCP/IP", "Routing", "Network Security", "DNS", "HTTP/HTTPS"]
};

const BLOOMS = [
  "Remember",
  "Understand",
  "Apply",
  "Analyze",
  "Evaluate",
  "Create"
];

function CreatePaper() {
  const navigate = useNavigate();
  const [subject, setSubject] = useState("");
  const [topics, setTopics] = useState([]);
  const [blooms, setBlooms] = useState([]);
  const [difficulty, setDifficulty] = useState("");

  const toggle = (value, list, setList) => {
    setList(
      list.includes(value)
        ? list.filter(i => i !== value)
        : [...list, value]
    );
  };

  const submitHandler = () => {
    const data = { subject, topics, blooms, difficulty };
    console.log("Data sent to backend:", data);
    alert("Request generated successfully!");
  };

  const disabled =
    !subject || topics.length === 0 || blooms.length === 0 || !difficulty;

  return (
    <div className="paper-container animate-fade-in">
      <div className="glass-card">
        <button
          onClick={() => navigate("/dashboard")}
          style={{
            background: "transparent",
            border: "none",
            color: "var(--text-muted)",
            marginBottom: "1rem",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            fontSize: "0.9rem"
          }}
        >
          ← Back to Dashboard
        </button>
        <h2 className="title">Generate Question Paper</h2>

        {/* Subject Selection */}
        <div className="form-section">
          <label className="section-title">Select Subject</label>
          <select
            value={subject}
            onChange={e => {
              setSubject(e.target.value);
              setTopics([]);
            }}
          >
            <option value="">-- Choose a Subject --</option>
            {Object.keys(SUBJECT_TOPICS).map(sub => (
              <option key={sub} value={sub}>{sub}</option>
            ))}
          </select>
        </div>

        {/* Topics Selection */}
        {subject && (
          <div className="form-section animate-fade-in">
            <label className="section-title">Select Topics</label>
            <div className="chips-grid">
              {SUBJECT_TOPICS[subject].map(topic => (
                <div
                  key={topic}
                  className={`chip ${topics.includes(topic) ? 'active' : ''}`}
                  onClick={() => toggle(topic, topics, setTopics)}
                >
                  {topic}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Bloom's Taxonomy */}
        <div className="form-section">
          <label className="section-title">Bloom's Taxonomy Levels</label>
          <div className="chips-grid">
            {BLOOMS.map(level => (
              <div
                key={level}
                className={`chip ${blooms.includes(level) ? 'active' : ''}`}
                onClick={() => toggle(level, blooms, setBlooms)}
              >
                {level}
              </div>
            ))}
          </div>
        </div>

        {/* Difficulty Selection */}
        <div className="form-section">
          <label className="section-title">Difficulty Level</label>
          <div className="difficulty-grid">
            {["Easy", "Medium", "Hard"].map(d => (
              <div
                key={d}
                className={`difficulty-card ${difficulty === d ? 'active' : ''}`}
                onClick={() => setDifficulty(d)}
              >
                <span className="label">{d}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <button
          className="btn-primary"
          disabled={disabled}
          onClick={submitHandler}
          style={{ marginTop: '2rem' }}
        >
          {disabled ? "Complete all fields to generate" : "Generate Question Paper"}
        </button>
      </div>
    </div>
  );
}

export default CreatePaper;
