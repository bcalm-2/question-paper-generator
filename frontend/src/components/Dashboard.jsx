
import { Link, useNavigate } from "react-router-dom";

const MOCK_PAPERS = [
    { id: 1, subject: "DBMS", title: "Mid-Term Examination", date: "2023-10-15" },
    { id: 2, subject: "Operating Systems", title: "Final Semester Paper", date: "2023-12-10" },
    { id: 3, subject: "Computer Networks", title: "Unit Test 1", date: "2024-01-20" },
];

function Dashboard() {
    const navigate = useNavigate();

    return (
        <div className="paper-container animate-fade-in">
            {/* Header Section */}
            <div className="glass-card mb-8">
                <h1 className="title" style={{ textAlign: "left", fontSize: "1.8rem", marginBottom: "0.5rem" }}>
                    Dashboard
                </h1>
                <p className="text-muted">Welcome back, Professor!</p>

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
                    {MOCK_PAPERS.map((paper) => (
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
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
