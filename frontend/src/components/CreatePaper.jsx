import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getConfig, generatePaper, uploadFile, getPaperById, updatePaper } from "../services/paperService.js";

const STEPS = ["Subject", "Topics", "Blooms", "Difficulty"];

/**
 * Utility to determine the current step index based on filled form data.
 * @param {string} subjectId - Selected subject ID
 * @param {Array} topics - Selected topics
 * @param {Array} blooms - Selected Bloom's levels
 * @param {string} difficulty - Selected difficulty
 * @returns {number} Current step index (0-4)
 */
function stepIndex(subjectId, topics, blooms, difficulty) {
  // Logic: Step index is determined by the presence of data for each sequential stage.
  if (!subjectId) return 0;         // Step 1: Select Subject
  if (topics.length === 0) return 1; // Step 2: Select Topics
  if (blooms.length === 0) return 2; // Step 3: Select Bloom's Levels
  if (!difficulty) return 3;         // Step 4: Select Difficulty
  return 4;                          // Final: Ready for generation
}

/**
 * CreatePaper Component
 * 
 * A multi-step form for generating or editing question papers.
 * Steps: Subject Selection -> Topic Selection -> Bloom's Level -> Difficulty
 */
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
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  /**
   * Fetches configuration data (subjects, topics) and existing paper data if in Edit Mode.
   */
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch global configuration (subjects, topics, bloom levels) from backend
        const configData = await getConfig();
        setConfig(configData);

        // State Hydration: If editing an existing paper, load its parameters into local state
        if (isEditMode) {
          const paperData = await getPaperById(id);
          setSelectedSubjectId(paperData.subject_id);
          setTopics(paperData.topics || []);
          setBlooms(paperData.blooms || []);
          setDifficulty(paperData.difficulty || "");
        }
      } catch (err) {
        console.error("CreatePaper: Failed to load context data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id, isEditMode]);

  const showToast = (msg, type = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3500);
  };

  const { SUBJECT_TOPICS, SUBJECTS, BLOOMS } = config;
  const currentSubjectObj = SUBJECTS.find(s => s.id == selectedSubjectId);
  const subjectName = currentSubjectObj?.name ?? "";

  const toggle = (value, list, setList) =>
    setList(list.includes(value) ? list.filter(i => i !== value) : [...list, value]);

  /**
   * Handles file selection and immediate upload to the server.
   * Linked to the selected subject to ensure correct material mapping.
   */
  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Safety check: Subject must be selected for mapping
    if (!selectedSubjectId) {
      showToast("Please select a subject first.", "error");
      e.target.value = null;
      return;
    }

    setUploadStatus("uploading");
    try {
      await uploadFile(file, selectedSubjectId);
      setUploadedFile(file.name);
      setUploadStatus("success");
    } catch {
      setUploadStatus("error");
      setUploadedFile(null);
    }
  };

  const submitHandler = async () => {
    setSubmitting(true);
    try {
      if (isEditMode) {
        // Action: Update existing paper metadata and configuration
        await updatePaper(id, { subject_id: selectedSubjectId, topics, blooms, difficulty });
        showToast("Paper updated successfully!");
        navigate(`/paper/${id}`);
      } else {
        // Action: Generate a brand new paper using the AI engine
        const result = await generatePaper({ subject_id: selectedSubjectId, topics, blooms, difficulty });
        showToast("Paper generated successfully!");
        navigate(`/paper/${result.paperId}`);
      }
    } catch (err) {
      // Error handling with dynamic context based on mode (Edit vs Create)
      showToast(`Failed to ${isEditMode ? "update" : "generate"} paper. Please try again.`, "error");
    } finally {
      setSubmitting(false);
    }
  };

  const disabled = !selectedSubjectId || topics.length === 0 || blooms.length === 0 || !difficulty;
  const currentStep = stepIndex(selectedSubjectId, topics, blooms, difficulty);

  if (loading) return <div className="spinner-outer"><div className="spinner" /></div>;

  return (
    <div className="animate-fade">
      <button className="back-btn" onClick={() => navigate("/dashboard")}>← Back</button>

      <h1 className="page-title">{isEditMode ? "Edit Paper" : "Generate Paper"}</h1>
      <p className="page-subtitle">{isEditMode ? "Update paper settings" : "Configure your AI-generated question paper"}</p>

      {/* Step indicator */}
      <div className="steps">
        {STEPS.map((label, i) => (
          <div key={label} className={`step ${i === currentStep ? "active" : ""} ${i < currentStep ? "done" : ""}`}>
            {i > 0 && <div className="step-connector" />}
            <div className="step-num">{i < currentStep ? "✓" : i + 1}</div>
            <span className="step-label">{label}</span>
          </div>
        ))}
      </div>

      <div className="card" style={{ display: "flex", flexDirection: "column", gap: "1.75rem" }}>

        {/* Subject */}
        <div>
          <label className="section-title">Subject</label>
          <select
            value={selectedSubjectId}
            onChange={e => { setSelectedSubjectId(e.target.value); setTopics([]); }}
          >
            <option value="">— Choose a subject —</option>
            {SUBJECTS.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </div>

        {/* Topics */}
        {selectedSubjectId && subjectName && SUBJECT_TOPICS[subjectName] && (
          <div className="animate-fade">
            <label className="section-title">Topics for {subjectName}</label>
            <div className="chips-grid">
              {SUBJECT_TOPICS[subjectName].map(topic => (
                <div
                  key={topic}
                  className={`chip ${topics.includes(topic) ? "active" : ""}`}
                  onClick={() => toggle(topic, topics, setTopics)}
                >{topic}</div>
              ))}
            </div>
          </div>
        )}

        {/* File upload */}
        {selectedSubjectId && (
          <div className="animate-fade">
            <label className="section-title">Reference Material <span style={{ fontWeight: 400, textTransform: "none", letterSpacing: 0 }}>(optional)</span></label>
            <input type="file" accept=".pdf,.txt" onChange={handleFileChange} style={{ display: "none" }} id="file-upload" />
            <label htmlFor="file-upload">
              <div className={`upload-zone ${uploadStatus === "uploading" ? "drag-over" : ""}`}>
                <div className="upload-icon">
                  {uploadStatus === "success" ? "✅" : uploadStatus === "error" ? "❌" : "📄"}
                </div>
                <p style={{ fontWeight: 500 }}>Click to upload PDF or TXT</p>
                <p className="upload-hint">
                  {uploadedFile ? `Selected: ${uploadedFile}` : "Supported: .pdf, .txt"}
                </p>
                {uploadStatus === "success" && <p className="upload-success">Upload successful!</p>}
                {uploadStatus === "error" && <p className="upload-error">Upload failed. Try again.</p>}
                {uploadStatus === "uploading" && <p className="upload-hint">Uploading…</p>}
              </div>
            </label>
          </div>
        )}

        {/* Bloom's */}
        <div>
          <label className="section-title">Bloom's Taxonomy Levels</label>
          <div className="chips-grid">
            {BLOOMS.map(level => (
              <div
                key={level}
                className={`chip ${blooms.includes(level) ? "active" : ""}`}
                onClick={() => toggle(level, blooms, setBlooms)}
              >{level}</div>
            ))}
          </div>
        </div>

        {/* Difficulty */}
        <div>
          <label className="section-title">Difficulty Level</label>
          <div className="difficulty-grid">
            {[
              { label: "Easy", emoji: "🟢" },
              { label: "Medium", emoji: "🟡" },
              { label: "Hard", emoji: "🔴" },
            ].map(({ label, emoji }) => (
              <div
                key={label}
                className={`difficulty-card ${difficulty === label ? "active" : ""}`}
                onClick={() => setDifficulty(label)}
              >
                <span className="emoji">{emoji}</span>
                <span className="label">{label}</span>
              </div>
            ))}
          </div>
        </div>

        <button
          className="btn btn-primary btn-full"
          disabled={disabled || submitting}
          onClick={submitHandler}
        >
          {submitting
            ? (isEditMode ? "Updating…" : "Generating…")
            : disabled
              ? "Complete all steps above"
              : (isEditMode ? "Update Paper" : "Generate Paper ✨")}
        </button>
      </div>

      {/* Toast */}
      {toast && (
        <div className="toast-container">
          <div className={`toast toast-${toast.type}`}>
            {toast.type === "success" ? "✅" : "❌"} {toast.msg}
          </div>
        </div>
      )}
    </div>
  );
}

export default CreatePaper;
