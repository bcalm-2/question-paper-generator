import { useState, useEffect } from "react";
import adminService from "../services/adminService";
import "./ConfigDashboard.css";

const ConfigDashboard = () => {
    const [activeTab, setActiveTab] = useState("subjects");
    const [subjects, setSubjects] = useState([]);
    const [files, setFiles] = useState([]);
    const [newSubject, setNewSubject] = useState({ name: "", topics: "" });
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    useEffect(() => {
        fetchData();
    }, [activeTab]);

    const fetchData = async () => {
        setLoading(true);
        try {
            if (activeTab === "subjects") {
                const data = await adminService.getAdminSubjects();
                setSubjects(data);
            } else {
                const data = await adminService.getAdminFiles();
                setFiles(data);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
        setLoading(false);
    };

    const handleAddSubject = async (e) => {
        e.preventDefault();
        try {
            const topicsArray = newSubject.topics.split(",").map(t => t.trim()).filter(t => t !== "");
            await adminService.addSubject({ name: newSubject.name, topics: topicsArray });
            setNewSubject({ name: "", topics: "" });
            setMessage("Subject added successfully!");
            fetchData();
            setTimeout(() => setMessage(""), 3000);
        } catch (error) {
            console.error("Error adding subject:", error);
        }
    };

    const handleDeleteSubject = async (id) => {
        if (window.confirm("Are you sure? This will delete all associated papers and topics.")) {
            try {
                await adminService.deleteSubject(id);
                fetchData();
            } catch (error) {
                console.error("Error deleting subject:", error);
            }
        }
    };

    const handleDeleteFile = async (filename) => {
        if (window.confirm(`Delete ${filename}?`)) {
            try {
                await adminService.deleteFile(filename);
                fetchData();
            } catch (error) {
                console.error("Error deleting file:", error);
            }
        }
    };

    return (
        <div className="config-dashboard">
            <header className="config-header">
                <h1>Configuration Dashboard</h1>
                <p>Manage your AI Question Generator ecosystem</p>
            </header>

            <div className="tabs">
                <button
                    className={activeTab === "subjects" ? "active" : ""}
                    onClick={() => setActiveTab("subjects")}
                >
                    Subjects & Topics
                </button>
                <button
                    className={activeTab === "files" ? "active" : ""}
                    onClick={() => setActiveTab("files")}
                >
                    Resource Files
                </button>
            </div>

            {message && <div className="success-banner">{message}</div>}

            <div className="tab-content">
                {activeTab === "subjects" && (
                    <div className="subjects-section">
                        <div className="add-subject-card">
                            <h3>Add New Subject</h3>
                            <form onSubmit={handleAddSubject}>
                                <input
                                    type="text"
                                    placeholder="Subject Name (e.g. Distributed Systems)"
                                    value={newSubject.name}
                                    onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                                    required
                                />
                                <textarea
                                    placeholder="Topics (comma separated: Paxos, Raft, Sharding)"
                                    value={newSubject.topics}
                                    onChange={(e) => setNewSubject({ ...newSubject, topics: e.target.value })}
                                    required
                                />
                                <button type="submit" className="primary-btn">Add Subject</button>
                            </form>
                        </div>

                        <div className="subject-list">
                            <h3>Existing Subjects</h3>
                            {loading ? <p>Loading...</p> : (
                                <div className="grid">
                                    {subjects.map(sub => (
                                        <div key={sub.id} className="subject-card">
                                            <div className="card-header">
                                                <h4>{sub.name}</h4>
                                                <button onClick={() => handleDeleteSubject(sub.id)} className="delete-icon">×</button>
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

                {activeTab === "files" && (
                    <div className="files-section">
                        <h3>Uploaded Content Files</h3>
                        <p className="subtitle">Reference files used by the AI to generate questions</p>

                        {loading ? <p>Loading...</p> : (
                            <table className="file-table">
                                <thead>
                                    <tr>
                                        <th>Filename</th>
                                        <th>Assigned Subject</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {files.map((file, idx) => (
                                        <tr key={idx}>
                                            <td>{file.name}</td>
                                            <td><span className="subject-label">{file.subject}</span></td>
                                            <td>
                                                <button
                                                    onClick={() => handleDeleteFile(file.name)}
                                                    className="delete-btn-small"
                                                >
                                                    Delete
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    {files.length === 0 && (
                                        <tr>
                                            <td colSpan="3" style={{ textAlign: 'center', padding: '2rem' }}>No files found.</td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ConfigDashboard;
