import React, { useEffect, useState } from "react";
import { generatePaper } from "./services/paperService";

const SUBJECTS = ["DBMS", "Operating Systems", "Computer Networks"];

const SUBJECT_TOPICS = {
  DBMS: ["Normalization", "ER Model", "Transactions"],
  "Operating Systems": ["Processes", "Deadlock", "Memory Management"],
  "Computer Networks": ["OSI Model", "TCP/IP", "Routing"]
};

const BLOOM_LEVELS = [
  "Remember",
  "Understand",
  "Apply",
  "Analyze",
  "Evaluate",
  "Create"
];

const CreatePaper = () => {
  const [subject, setSubject] = useState("");
  const [topics, setTopics] = useState([]);
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [blooms, setBlooms] = useState([]);
  const [difficulty, setDifficulty] = useState("");
  const [loading, setLoading] = useState(false);

  // subject change → topics update
  useEffect(() => {
    if (subject) {
      setTopics(SUBJECT_TOPICS[subject]);
      setSelectedTopics([]);
    }
  }, [subject]);

  const handleTopicChange = (topic) => {
    setSelectedTopics((prev) =>
      prev.includes(topic)
        ? prev.filter((t) => t !== topic)
        : [...prev, topic]
    );
  };

  const handleBloomChange = (level) => {
    setBlooms((prev) =>
      prev.includes(level)
        ? prev.filter((b) => b !== level)
        : [...prev, level]
    );
  };

  const isFormValid =
    subject && selectedTopics.length > 0 && blooms.length > 0 && difficulty;

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const payload = {
        subject,
        topics: selectedTopics,
        blooms,
        difficulty
      };

      const response = await generatePaper(payload);
      console.log("Generated Paper:", response.data);

      alert("Question Paper Generated Successfully!");
    } catch (error) {
      alert("Error generating question paper");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "25px" }}>
      <h2>Create Question Paper</h2>

      {/* SUBJECT */}
      <label><b>Select Subject</b></label><br />
      <select value={subject} onChange={(e) => setSubject(e.target.value)}>
        <option value="">-- Select Subject --</option>
        {SUBJECTS.map((sub) => (
          <option key={sub} value={sub}>{sub}</option>
        ))}
      </select>

      {/* TOPICS */}
      {topics.length > 0 && (
        <>
          <h3>Topics</h3>
          {topics.map((topic) => (
            <div key={topic}>
              <input
                type="checkbox"
                checked={selectedTopics.includes(topic)}
                onChange={() => handleTopicChange(topic)}
              />
              {topic}
            </div>
          ))}
        </>
      )}

      {/* BLOOM LEVELS */}
      <h3>Bloom’s Taxonomy Levels</h3>
      {BLOOM_LEVELS.map((level) => (
        <div key={level}>
          <input
            type="checkbox"
            checked={blooms.includes(level)}
            onChange={() => handleBloomChange(level)}
          />
          {level}
        </div>
      ))}

      {/* DIFFICULTY */}
      <h3>Difficulty</h3>
      {["Easy", "Medium", "Hard"].map((d) => (
        <div key={d}>
          <input
            type="radio"
            name="difficulty"
            checked={difficulty === d}
            onChange={() => setDifficulty(d)}
          />
          {d}
        </div>
      ))}

      <br />
      <button disabled={!isFormValid || loading} onClick={handleGenerate}>
        {loading ? "Generating..." : "Generate Question Paper"}
      </button>
    </div>
  );
};

export default CreatePaper;
