import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { getAllPapers } from "../services/paperService.js";

function Dashboard() {
    const navigate = useNavigate();
    const userName = localStorage.getItem("userName") || "User";
    const [papers, setPapers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getAllPapers()
            .then(setPapers)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, []);

    const subjects = [...new Set(papers.map(p => p.subject))];
    const lastDate = papers[0]
        ? new Date(papers[0].created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short" })
        : "—";

    const difficultyBadge = (d) => {
        if (!d) return null;
        const map = { Easy: "badge-easy", Medium: "badge-medium", Hard: "badge-hard" };
        return <span className={`badge ${map[d] || "badge-subject"}`}>{d}</span>;
    };

    return (
        <div className="animate-fade">
            {/* Page header */}
            <div className="flex justify-between" style={{ alignItems: "flex-start", marginBottom: "1.75rem", flexWrap: "wrap", gap: "1rem" }}>
                <div>
                    <h1 className="page-title">Dashboard</h1>
                    <p className="page-subtitle">Welcome back, {userName} 👋</p>
                </div>
                <button className="btn btn-primary" onClick={() => navigate("/create-paper")}>
                    + Create Paper
                </button>
            </div>

            {/* Stats */}
            <div className="stats-grid">
                <div className="stat-card">
                    <span className="stat-label">Total Papers</span>
                    <span className="stat-value">{papers.length}</span>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Subjects</span>
                    <span className="stat-value">{subjects.length}</span>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Last Generated</span>
                    <span className="stat-value" style={{ fontSize: "1.25rem" }}>{lastDate}</span>
                </div>
            </div>

            {/* Papers grid */}
            <div className="flex justify-between" style={{ alignItems: "center", marginBottom: "1rem" }}>
                <h2 style={{ fontSize: "1rem", fontWeight: 600, color: "var(--text)" }}>Your Papers</h2>
                <span style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>{papers.length} total</span>
            </div>

            {loading ? (
                <div className="spinner-outer"><div className="spinner" /></div>
            ) : papers.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">📄</div>
                    <div className="empty-title">No papers yet</div>
                    <p className="empty-desc">Generate your first AI question paper in under 2 seconds.</p>
                    <button className="btn btn-primary" onClick={() => navigate("/create-paper")}>
                        Create First Paper
                    </button>
                </div>
            ) : (
                <div className="papers-grid">
                    {papers.map((paper) => (
                        <div key={paper.id} className="paper-card">
                            <div className="paper-card-header">
                                <div>
                                    <div className="paper-card-badges" style={{ marginBottom: "0.5rem" }}>
                                        <span className="badge badge-subject">{paper.subject}</span>
                                        {difficultyBadge(paper.difficulty)}
                                    </div>
                                    <div className="paper-card-title">{paper.title}</div>
                                </div>
                            </div>
                            <div className="paper-card-meta flex gap-sm" style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                                <span>🎯 {paper.marks} marks</span>
                                <span>•</span>
                                <span>⏱ {paper.duration}</span>
                            </div>
                            {paper.created_at && (
                                <div className="paper-card-meta" style={{ fontSize: "0.78rem" }}>
                                    {new Date(paper.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}
                                </div>
                            )}
                            <div className="paper-card-footer">
                                <button className="btn btn-primary btn-sm" onClick={() => navigate(`/paper/${paper.id}`)}>
                                    View →
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Dashboard;
