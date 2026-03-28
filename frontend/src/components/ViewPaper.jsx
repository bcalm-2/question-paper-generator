import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { getPaperById, downloadPaperPDF } from "../services/paperService.js";

/**
 * ViewPaper Component
 * 
 * Displays a print-ready preview of a generated question paper.
 * Provides actions to:
 * - Edit paper metadata (Title, Duration, Marks)
 * - Download the paper as a PDF
 */
function ViewPaper() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [paper, setPaper] = useState(null);
    const [loading, setLoading] = useState(true);
    const [downloading, setDownloading] = useState(false);

    /**
     * Fetches paper details and its questions on mount.
     */
    useEffect(() => {
        getPaperById(id)
            .then(setPaper)
            .catch(console.error)
            .finally(() => setLoading(false));
    }, [id]);

    /**
     * Triggers the PDF generation and download flow.
     * Communicates with the ReportLab-based backend to receive a byte stream.
     */
    const handleDownload = async () => {
        setDownloading(true);
        try {
            await downloadPaperPDF(id);
        } catch (error) {
            console.error("ViewPaper: PDF download failed", error);
            alert("Failed to download PDF. Please try again.");
        } finally {
            setDownloading(false);
        }
    };

    if (loading) return <div className="spinner-outer"><div className="spinner" /></div>;

    if (!paper) return (
        <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <div className="empty-title">Paper not found</div>
            <button className="btn btn-secondary" onClick={() => navigate("/dashboard")}>Back to Dashboard</button>
        </div>
    );

    let questionCounter = 0;

    return (
        <div className="animate-fade">
            <button className="back-btn" onClick={() => navigate("/dashboard")}>← Back</button>

            {/* Action bar */}
            <div className="flex justify-between" style={{ alignItems: "center", marginBottom: "1.5rem", flexWrap: "wrap", gap: "0.75rem" }}>
                <div>
                    <h1 className="page-title" style={{ marginBottom: "0.2rem" }}>Paper Preview</h1>
                    <p className="page-subtitle" style={{ marginBottom: 0 }}>Review before downloading</p>
                </div>
                <div style={{ display: "flex", gap: "0.75rem" }}>
                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate(`/edit-paper/${id}`)}
                    >✏️ Edit</button>
                    <button
                        className="btn btn-primary"
                        onClick={handleDownload}
                        disabled={downloading}
                    >
                        {downloading ? "Downloading…" : "⬇ Download PDF"}
                    </button>
                </div>
            </div>

            {/* Exam sheet */}
            <div className="exam-sheet">
                <div className="exam-header">
                    <div className="exam-header-left">
                        <h2>{paper.title}</h2>
                        <p>Subject: {paper.subject} · Difficulty: {paper.difficulty}</p>
                    </div>
                    <div className="exam-header-right">
                        <div className="meta-val">{paper.marks}</div>
                        <div className="meta-label">Total Marks</div>
                        <div style={{ marginTop: "0.75rem" }}>
                            <div className="meta-val" style={{ fontSize: "1.1rem" }}>{paper.duration}</div>
                            <div className="meta-label">Duration</div>
                        </div>
                    </div>
                </div>

                <div className="exam-body">
                    {paper.sections?.map((section, idx) => (
                        <div key={idx} className="exam-section">
                            <div className="exam-section-title">
                                {section.name} — {section.marks} Marks
                            </div>
                            {section.questions.map((q) => {
                                questionCounter++;
                                return (
                                    <div key={q.id} className="exam-question">
                                        <p><strong>{questionCounter}.</strong> {q.text}</p>
                                        {q.options && (
                                            <div className="exam-options">
                                                {q.options.map((opt, i) => (
                                                    <span key={i} className="exam-option">
                                                        {String.fromCharCode(97 + i)}) {opt}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                );
                            })}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default ViewPaper;
