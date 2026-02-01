
import { useParams, useNavigate } from "react-router-dom";

function ViewPaper() {
    const { id } = useParams();
    const navigate = useNavigate();

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

                <h1 className="title" style={{ textAlign: "left" }}>Paper Details</h1>

                <div style={{ marginTop: "2rem" }}>
                    <p className="section-title">Paper ID</p>
                    <p style={{ fontSize: "1.2rem" }}>#{id}</p>
                </div>

                <div style={{ marginTop: "2rem", padding: "2rem", background: "rgba(0,0,0,0.2)", borderRadius: "8px", textAlign: "center" }}>
                    <p className="text-muted">
                        Paper preview content would go here. <br />
                        (Title, Questions, Total Marks, etc.)
                    </p>
                </div>

                <div style={{ marginTop: "2rem", display: "flex", gap: "1rem" }}>
                    <button className="btn-primary" style={{ width: "auto" }}>Download PDF</button>
                    <button className="btn-primary" style={{ width: "auto", background: "rgba(255,255,255,0.1)" }}>Edit</button>
                </div>
            </div>
        </div>
    );
}

export default ViewPaper;
