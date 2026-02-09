
import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { getPaperById } from "../services/paperService.js";
import html2pdf from "html2pdf.js";

function ViewPaper() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [paper, setPaper] = useState(null);
    const [loading, setLoading] = useState(true);
    const paperRef = useRef();

    const handleDownload = () => {
        const element = paperRef.current;
        const opt = {
            margin: 1,
            filename: `${paper.subject.replace(/\s+/g, '_')}_Paper.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    };

    useEffect(() => {
        const fetchPaper = async () => {
            try {
                const data = await getPaperById(id);
                setPaper(data);
            } catch (err) {
                console.error("Failed to fetch paper:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchPaper();
    }, [id]);

    if (loading) return <div className="paper-container"><p className="text-muted">Loading paper...</p></div>;
    if (!paper) return <div className="paper-container"><p className="text-muted">Paper not found.</p></div>;

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

                <div style={{ marginTop: "2rem", textAlign: "left" }}>
                    <div ref={paperRef} style={{ background: "rgba(255,255,255,0.05)", padding: "2rem", borderRadius: "8px", color: "var(--text)" }}>
                        <div style={{ borderBottom: "1px solid var(--border)", paddingBottom: "1rem", marginBottom: "1.5rem", display: "flex", justifyContent: "space-between" }}>
                            <div>
                                <h2 style={{ fontSize: "1.4rem", marginBottom: "0.5rem" }}>{paper.title}</h2>
                                <p className="text-muted">Subject: {paper.subject}</p>
                            </div>
                            <div style={{ textAlign: "right" }}>
                                <p style={{ fontWeight: "bold", fontSize: "1.1rem" }}>Max Marks: {paper.marks}</p>
                                <p className="text-muted">Duration: {paper.duration}</p>
                            </div>
                        </div>

                        <div className="paper-content">
                            {paper.sections && paper.sections.map((section, idx) => (
                                <div key={idx} style={{ marginBottom: "2rem" }}>
                                    <h3 style={{ fontSize: "1.1rem", marginBottom: "1rem", color: "var(--primary)" }}>{section.name} ({section.marks} Marks)</h3>
                                    {section.questions.map((q) => (
                                        <div key={q.id} style={{ marginBottom: "1rem" }}>
                                            <p style={{ marginBottom: "0.5rem" }}>{q.id}. {q.text} {q.options && "(Multiple Choice)"}</p>
                                            {q.options && (
                                                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.5rem", paddingLeft: "1rem", color: "var(--text-muted)" }}>
                                                    {q.options.map((opt, i) => (
                                                        <span key={i}>{String.fromCharCode(97 + i)}) {opt}</span>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div style={{ marginTop: "2rem", display: "flex", gap: "1rem" }}>
                    <button className="btn-primary" style={{ width: "auto" }} onClick={handleDownload}>Download PDF</button>
                    <button className="btn-primary" style={{ width: "auto", background: "rgba(255,255,255,0.1)" }}>Edit</button>
                </div>
            </div>
        </div>
    );
}

export default ViewPaper;
