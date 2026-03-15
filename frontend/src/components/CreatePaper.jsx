import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "../App.css";
import { getConfig, generatePaper, uploadFile, getPaperById, updatePaper } from "../services/paperService.js";

function CreatePaper() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = !!id;

  const [selectedSubjectId, setSelectedSubjectId] = useState("");
  const [topics, setTopics] = useState([]);
  const [blooms, setBlooms] = useState([]);
  const [difficulty, setDifficulty] = useState("");

  const [config, setConfig] = useState({ SUBJECT_TOPICS: {}, SUBJECTS: [], BLOOMS: [] });
  const [loading, setLoading] = useState(true);
  const [uploadStatus, setUploadStatus] = useState("");
  const [uploadedFile, setUploadedFile] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const configData = await getConfig();
        setConfig(configData);

        if (isEditMode) {
          const paperData = await getPaperById(id);
          setSelectedSubjectId(paperData.subject_id);
          setTopics(paperData.topics || []);
          setBlooms(paperData.blooms || []);
          setDifficulty(paperData.difficulty || "");
        }
      } catch (err) {
        console.error("Failed to load data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id, isEditMode]);

  const SUBJECT_TOPICS = config.SUBJECT_TOPICS;
  const SUBJECTS = config.SUBJECTS;
  const BLOOMS = config.BLOOMS;

  // Find subject name for UI display and mapping
  const currentSubjectObj = SUBJECTS.find(s => s.id == selectedSubjectId);
  const subjectName = currentSubjectObj ? currentSubjectObj.name : "";

  const toggle = (value, list, setList) => {
    setList(
      list.includes(value)
        ? list.filter(i => i !== value)
        : [...list, value]
    );
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!selectedSubjectId) {
      alert("Please select a subject first.");
      e.target.value = null;
      return;
    }

    setUploadStatus("Uploading...");
    try {
      await uploadFile(file, selectedSubjectId);
      setUploadedFile(file.name);
      setUploadStatus("Upload Successful");
    } catch (err) {
      console.error("Upload failed", err);
      setUploadStatus("Upload Failed");
      setUploadedFile(null);
    }
  };

  const submitHandler = async () => {
    const data = {
      subject_id: selectedSubjectId,
      topics,
      blooms,
      difficulty
    };
    try {
      if (isEditMode) {
        await updatePaper(id, data);
        alert("Paper updated successfully!");
        navigate(`/paper/${id}`);
      } else {
        const result = await generatePaper(data);
        alert("Paper generated successfully!");
        navigate(`/paper/${result.paperId}`);
      }
    } catch (err) {
      console.error(isEditMode ? "Update failed:" : "Generation failed:", err);
      alert(`Failed to ${isEditMode ? "update" : "generate"} paper. Please try again.`);
    }
  };

  const disabled =
    !selectedSubjectId || topics.length === 0 || blooms.length === 0 || !difficulty;

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
        <h2 className="title">{isEditMode ? "Edit Question Paper" : "Generate Question Paper"}</h2>

        {/* Subject Selection */}
        <div className="form-section">
          <label className="section-title">Select Subject</label>
          <select
            value={selectedSubjectId}
            onChange={e => {
              setSelectedSubjectId(e.target.value);
              setTopics([]);
            }}
          >
            <option value="">-- Choose a Subject --</option>
            {SUBJECTS.map(sub => (
              <option key={sub.id} value={sub.id}>{sub.name}</option>
            ))}
          </select>
        </div>

        {/* Topics Selection */}
        {selectedSubjectId && subjectName && SUBJECT_TOPICS[subjectName] && (
          <div className="form-section animate-fade-in">
            <label className="section-title">Select Topics for {subjectName}</label>
            <div className="chips-grid">
              {SUBJECT_TOPICS[subjectName].map(topic => (
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

        {/* File Upload Section */}
        {selectedSubjectId && (
          <div className="form-section animate-fade-in">
            <label className="section-title">Reference Material (Optional)</label>
            <div style={{
              border: '2px dashed var(--border)',
              padding: '2rem',
              borderRadius: '8px',
              textAlign: 'center',
              background: 'rgba(255,255,255,0.02)'
            }}>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={handleFileChange}
                style={{ display: 'none' }}
                id="file-upload"
              />
              <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
                <div style={{ fontSize: '2rem', marginBottom: '1rem' }}>📄</div>
                <p style={{ marginBottom: '0.5rem' }}>Click to upload PDF or TXT</p>
                <p className="text-muted" style={{ fontSize: '0.8rem' }}>
                  {uploadedFile ? `Selected: ${uploadedFile}` : "Supported formats: .pdf, .txt"}
                </p>
              </label>
              {uploadStatus && (
                <p style={{
                  marginTop: '1rem',
                  color: uploadStatus.includes("Failed") ? "#ef4444" : "#22c55e",
                  fontSize: '0.9rem'
                }}>
                  {uploadStatus}
                </p>
              )}
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
          {disabled ? "Complete all fields to proceed" : (isEditMode ? "Update Question Paper" : "Generate Question Paper")}
        </button>
      </div>
    </div>
  );
}

export default CreatePaper;
