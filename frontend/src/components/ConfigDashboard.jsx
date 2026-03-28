import { useState, useEffect } from "react";
import adminService from "../services/adminService";

const ConfigDashboard = () => {
    const [activeTab, setActiveTab] = useState("subjects");
    const [subjects, setSubjects] = useState([]);
    const [files, setFiles] = useState([]);
    const [newSubject, setNewSubject] = useState({ name: "", topics: "" });
    const [loading, setLoading] = useState(false);
    const [toast, setToast] = useState(null);

    useEffect(() => { fetchData(); }, [activeTab]);

    const showToast = (msg, type = "success") => {
        setToast({ msg, type });
        setTimeout(() => setToast(null), 3200);
    };

    const fetchData = async () => {
        setLoading(true);
        try {
            if (activeTab === "subjects") setSubjects(await adminService.getAdminSubjects());
            else setFiles(await adminService.getAdminFiles());
        } catch { /* silent */ }
        setLoading(false);
    };

    const handleAddSubject = async (e) => {
        e.preventDefault();
        const topicsArray = newSubject.topics.split(",").map(t => t.trim()).filter(Boolean);
        try {
            await adminService.addSubject({ name: newSubject.name, topics: topicsArray });
            setNewSubject({ name: "", topics: "" });
            showToast("Subject added successfully!");
            fetchData();
        } catch { showToast("Failed to add subject.", "error"); }
    };

    const handleDeleteSubject = async (id) => {
        if (!window.confirm("Delete this subject and all its topics?")) return;
        try {
            await adminService.deleteSubject(id);
            showToast("Subject deleted.");
            fetchData();
        } catch { showToast("Failed to delete.", "error"); }
    };

    const handleDeleteFile = async (filename) => {
        if (!window.confirm(`Delete "${filename}"?`)) return;
        try {
            await adminService.deleteFile(filename);
            showToast("File deleted.");
            fetchData();
        } catch { showToast("Failed to delete file.", "error"); }
    };

    return (
        <div className="animate-fade">
            <h1 className="page-title">Configure</h1>
            <p className="page-subtitle">Manage subjects, topics, and reference files</p>

            {/* Tabs */}
            <div className="tabs">
                <button className={`tab-btn ${activeTab === "subjects" ? "active" : ""}`} onClick={() => setActiveTab("subjects")}>
                    Subjects &amp; Topics
                </button>
                <button className={`tab-btn ${activeTab === "files" ? "active" : ""}`} onClick={() => setActiveTab("files")}>
                    Resource Files
                </button>
            </div>

            {/* Subjects tab */}
            {activeTab === "subjects" && (
                <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
                    {/* Add form */}
                    <div className="card">
                        <h3 style={{ fontSize: "1rem", fontWeight: 600, marginBottom: "1.25rem" }}>Add New Subject</h3>
                        <form onSubmit={handleAddSubject} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                            <div className="form-group" style={{ marginBottom: 0 }}>
                                <label className="form-label">Subject Name</label>
                                <input
                                    type="text"
                                    placeholder="e.g. Distributed Systems"
                                    value={newSubject.name}
                                    onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                                    required
                                />
                            </div>
                            <div className="form-group" style={{ marginBottom: 0 }}>
                                <label className="form-label">Topics <span style={{ fontWeight: 400, textTransform: "none", letterSpacing: 0 }}>(comma-separated)</span></label>
                                <textarea
                                    placeholder="Paxos, Raft, Sharding, CAP Theorem"
                                    value={newSubject.topics}
                                    onChange={(e) => setNewSubject({ ...newSubject, topics: e.target.value })}
                                    required
                                />
                            </div>
                            <div style={{ display: "flex", justifyContent: "flex-end" }}>
                                <button type="submit" className="btn btn-primary">Add Subject</button>
                            </div>
                        </form>
                    </div>

                    {/* Subject list */}
                    <div>
                        <h3 style={{ fontSize: "0.9rem", fontWeight: 600, color: "var(--text-muted)", marginBottom: "1rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                            Existing Subjects ({subjects.length})
                        </h3>
                        {loading ? (
                            <div className="spinner-outer"><div className="spinner" /></div>
                        ) : subjects.length === 0 ? (
                            <div className="empty-state">
                                <div className="empty-icon">📚</div>
                                <div className="empty-title">No subjects yet</div>
                                <p className="empty-desc">Add your first subject above.</p>
                            </div>
                        ) : (
                            <div className="subject-cards-grid">
                                {subjects.map(sub => (
                                    <div key={sub.id} className="subject-card-item">
                                        <div className="subject-card-top">
                                            <span className="subject-card-name">{sub.name}</span>
                                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteSubject(sub.id)}>×</button>
                                        </div>
                                        <div className="topic-tags">
                                            {sub.topics.map(t => (
                                                <span key={t.id} className="topic-tag">{t.name}</span>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* Files tab */}
            {activeTab === "files" && (
                <div className="card">
                    <h3 style={{ fontSize: "1rem", fontWeight: 600, marginBottom: "0.4rem" }}>Uploaded Reference Files</h3>
                    <p className="text-muted" style={{ fontSize: "0.875rem", marginBottom: "1.5rem" }}>
                        These files are used by the AI to generate context-aware questions.
                    </p>
                    {loading ? (
                        <div className="spinner-outer"><div className="spinner" /></div>
                    ) : (
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>Filename</th>
                                    <th>Assigned Subject</th>
                                    <th style={{ width: "80px" }}>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {files.length === 0 ? (
                                    <tr>
                                        <td colSpan="3" style={{ textAlign: "center", padding: "2rem", color: "var(--text-muted)" }}>
                                            No files uploaded yet.
                                        </td>
                                    </tr>
                                ) : files.map((file, idx) => (
                                    <tr key={idx}>
                                        <td style={{ fontWeight: 500 }}>📄 {file.name}</td>
                                        <td><span className="badge badge-subject">{file.subject}</span></td>
                                        <td>
                                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteFile(file.name)}>
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            )}

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
};

export default ConfigDashboard;
