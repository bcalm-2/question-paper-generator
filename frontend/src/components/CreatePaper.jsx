import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";
import { getConfig, generatePaper } from "../services/paperService.js";

function CreatePaper() {
  const navigate = useNavigate();
  const [subject, setSubject] = useState("");
  const [topics, setTopics] = useState([]);
  const [blooms, setBlooms] = useState([]);
  const [difficulty, setDifficulty] = useState("");

  const [config, setConfig] = useState({ SUBJECT_TOPICS: {}, BLOOMS: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const data = await getConfig();
        setConfig(data);
      } catch (err) {
        console.error("Failed to load config:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchConfig();
  }, []);

  const SUBJECT_TOPICS = config.SUBJECT_TOPICS;
  const BLOOMS = config.BLOOMS;

  const toggle = (value, list, setList) => {
    setList(
      list.includes(value)
        ? list.filter(i => i !== value)
        : [...list, value]
    );
  };

  const submitHandler = async () => {
    const data = { subject, topics, blooms, difficulty };
    try {
      const result = await generatePaper(data);
      alert("Paper generated successfully!");
      navigate(`/paper/${result.paperId}`);
    } catch (err) {
      console.error("Generation failed:", err);
      alert("Failed to generate paper. Please try again.");
    }
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
