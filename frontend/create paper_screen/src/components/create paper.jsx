import { useState } from "react";
import "../styles/createPaper.css";

const SUBJECT_TOPICS = {
  DBMS: ["Normalization", "ER Model", "Transactions"],
  OS: ["Processes", "Memory Management", "Deadlocks"],
  CN: ["OSI Model", "TCP/IP", "Routing"]
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
    alert("Request sent to backend");
  };

  const disabled =
    !subject || topics.length === 0 || blooms.length === 0 || !difficulty;

  return (
    <div className="container">
      <h2>Create Question Paper</h2>

      <label>Subject</label>
      <select value={subject} onChange={e => {
        setSubject(e.target.value);
        setTopics([]);
      }}>
        <option value="">Select Subject</option>
        {Object.keys(SUBJECT_TOPICS).map(sub => (
          <option key={sub} value={sub}>{sub}</option>
        ))}
      </select>

      {subject && (
        <>
          <label>Topics</label>
          {SUBJECT_TOPICS[subject].map(topic => (
            <div key={topic}>
              <input
                type="checkbox"
                onChange={() => toggle(topic, topics, setTopics)}
              />
              {topic}
            </div>
          ))}
        </>
      )}

      <label>Bloom's Taxonomy</label>
      {BLOOMS.map(level => (
        <div key={level}>
          <input
            type="checkbox"
            onChange={() => toggle(level, blooms, setBlooms)}
          />
          {level}
        </div>
      ))}

      <label>Difficulty</label>
      {["Easy", "Medium", "Hard"].map(d => (
        <div key={d}>
          <input
            type="radio"
            name="difficulty"
            onChange={() => setDifficulty(d)}
          />
          {d}
        </div>
      ))}

      <button disabled={disabled} onClick={submitHandler}>
        Generate Question Paper
      </button>
    </div>
  );
}

export default CreatePaper;
