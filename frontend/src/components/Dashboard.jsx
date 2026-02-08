
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { getAllPapers } from "../services/paperService.js";

function Dashboard() {
    const navigate = useNavigate();
    const [papers, setPapers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPapers = async () => {
            try {
                const data = await getAllPapers();
                setPapers(data);
            } catch (err) {
                console.error("Failed to fetch papers:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchPapers();
    }, []);

    return (
        <div className="paper-container animate-fade-in">
            {/* Header Section */}
            <div className="glass-card mb-8">
                <h1 className="title" style={{ textAlign: "left", fontSize: "1.8rem", marginBottom: "0.5rem" }}>
                    Dashboard
                </h1>
                <p className="text-muted">Welcome back, Srashti!</p>

                <div style={{ marginTop: "1.5rem" }}>
                    <button
                        className="btn-primary"
                        onClick={() => navigate("/create-paper")}
                        style={{ width: "auto", padding: "0.8rem 1.5rem" }}
                    >
                        + Create New Paper
                    </button>
                </div>
            </div>

            {/* Existing Papers List */}
            <div className="glass-card" style={{ marginTop: "2rem" }}>
                <h2 className="section-title" style={{ fontSize: "1.2rem", color: "white", marginBottom: "1.5rem" }}>
                    Your Question Papers
                </h2>

                <div className="papers-list">
                    {loading ? (
                        <p className="text-muted">Loading papers...</p>
                    ) : papers.length === 0 ? (
                        <p className="text-muted">No papers found. Create one to get started!</p>
                    ) : (
                        papers.map((paper) => (
                            <div
                                key={paper.id}
                                className="paper-item"
                                style={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    padding: "1rem",
                                    background: "rgba(255, 255, 255, 0.05)",
                                    border: "1px solid var(--border)",
                                    borderRadius: "12px",
                                    marginBottom: "1rem",
                                    transition: "all 0.2s ease"
                                }}
                            >
                                <div>
                                    <h3 style={{ fontSize: "1.1rem", marginBottom: "0.25rem", fontWeight: "600" }}>
                                        {paper.subject}
                                    </h3>
                                    <p className="text-muted" style={{ fontSize: "0.9rem" }}>
                                        {paper.title} • {paper.date}
                                    </p>
                                </div>

                                <Link
                                    to={`/paper/${paper.id}`}
                                    className="btn-primary"
                                    style={{
                                        width: "auto",
                                        padding: "0.5rem 1rem",
                                        fontSize: "0.9rem",
                                        marginTop: 0,
                                        textDecoration: "none",
                                        display: "inline-block"
                                    }}
                                >
                                    View
                                </Link>
                            </div>
                        )))}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
