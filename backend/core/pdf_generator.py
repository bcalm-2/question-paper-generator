from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO


class PDFGenerator:
    """
    Generates formatted question-paper PDFs using ReportLab.

    Responsibilities (SRP):
        - PDF creation and layout only. Does NOT retrieve data from the
          database or filesystem — it receives a pre-assembled ``paper_data``
          dict from the service layer.
    """

    def __init__(self):
        """Initializes ReportLab stylesheet and registers custom paragraph styles."""
        self.styles = getSampleStyleSheet()
        self._register_styles()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_pdf(self, paper_data: dict) -> BytesIO:
        """
        Build a PDF in memory and return a seeked :class:`~io.BytesIO` buffer.

        Args:
            paper_data: Dict produced by :class:`~services.paper_service.PaperService`,
                containing ``title``, ``subject``, ``difficulty``, ``marks``,
                ``duration``, and ``sections``.

        Returns:
            :class:`~io.BytesIO` positioned at the start, ready for streaming.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50,
        )

        elements = []
        elements.extend(self._build_header())
        elements.extend(self._build_info_table(paper_data))
        elements.extend(self._build_sections(paper_data.get("sections", [])))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    # ------------------------------------------------------------------
    # Private — layout builders
    # ------------------------------------------------------------------

    def _register_styles(self) -> None:
        """Registers custom paragraph styles for titles, headers, and questions."""
        self.styles.add(
            ParagraphStyle(
                name="CenterTitle",
                parent=self.styles["Heading1"],
                alignment=1,
                spaceAfter=20,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="CenterHeader",
                parent=self.styles["Normal"],
                alignment=1,
                fontSize=10,
                spaceAfter=5,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="QuestionText",
                parent=self.styles["Normal"],
                fontSize=11,
                spaceBefore=10,
                spaceAfter=5,
                leftIndent=20,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="OptionStyle",
                parent=self.styles["Normal"],
                leftIndent=40,
            )
        )

    def _build_header(self) -> list:
        """Returns the institutional header elements."""
        return [
            Paragraph(
                "<b>INSTITUTE OF TECHNOLOGY AND RESEARCH</b>",
                self.styles["CenterTitle"],
            ),
            Paragraph(
                "Department of Computer Science and Engineering",
                self.styles["CenterHeader"],
            ),
            Spacer(1, 12),
        ]

    def _build_info_table(self, paper_data: dict) -> list:
        """Returns a two-column info table summarizing paper metadata."""
        info_data = [
            [f"Subject: {paper_data.get('subject')}", f"Date: {paper_data.get('date', '—')}"],
            [f"Title: {paper_data.get('title')}", f"Duration: {paper_data.get('duration', '90 Mins')}"],
            [f"Difficulty: {paper_data.get('difficulty')}", f"Max Marks: {paper_data.get('marks')}"],
        ]

        table = Table(info_data, colWidths=[300, 150])
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        return [table, Spacer(1, 24)]

    def _build_sections(self, sections: list) -> list:
        """Iterates over sections and builds question + option elements."""
        elements = []
        q_count = 0

        for section in sections:
            elements.append(
                Paragraph(
                    f"<b>{section['name']} ({section['marks']} Marks)</b>",
                    self.styles["Heading3"],
                )
            )
            elements.append(Spacer(1, 10))

            for q in section.get("questions", []):
                q_count += 1
                q_text = f"{q_count}. {q.get('text')}"
                if "marks" in q:
                    q_text += f" [{q['marks']} Marks]"

                elements.append(Paragraph(q_text, self.styles["QuestionText"]))

                for j, opt in enumerate(q.get("options", [])):
                    elements.append(
                        Paragraph(f"{chr(97 + j)}) {opt}", self.styles["OptionStyle"])
                    )

                elements.append(Spacer(1, 5))

            elements.append(Spacer(1, 15))

        return elements
