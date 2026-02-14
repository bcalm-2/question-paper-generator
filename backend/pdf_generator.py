from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CenterTitle',
            parent=self.styles['Heading1'],
            alignment=1,
            spaceAfter=20
        ))
        self.styles.add(ParagraphStyle(
            name='CenterHeader',
            parent=self.styles['Normal'],
            alignment=1,
            fontSize=10,
            spaceAfter=5
        ))
        self.styles.add(ParagraphStyle(
            name='QuestionText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceBefore=10,
            spaceAfter=5,
            leftIndent=20
        ))

    def generate_pdf(self, paper_data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        elements = []

        # 1. College Header (Placeholder)
        elements.append(Paragraph("<b>INSTITUTE OF TECHNOLOGY AND RESEARCH</b>", self.styles['CenterTitle']))
        elements.append(Paragraph("Department of Computer Science and Engineering", self.styles['CenterHeader']))
        elements.append(Spacer(1, 12))

        # 2. Paper Info Table
        info_data = [
            [f"Subject: {paper_data.get('subject')}", f"Date: {paper_data.get('date', '2024-02-12')}"],
            [f"Title: {paper_data.get('title')}", f"Duration: {paper_data.get('duration', '90 Mins')}"],
            [f"Difficulty: {paper_data.get('difficulty')}", f"Max Marks: {paper_data.get('marks')}"]
        ]
        
        info_table = Table(info_data, colWidths=[300, 150])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 24))

        # 3. Sections and Questions
        for section in paper_data.get('sections', []):
            elements.append(Paragraph(f"<b>{section['name']} ({section['marks']} Marks)</b>", self.styles['Heading3']))
            elements.append(Spacer(1, 10))
            
            for i, q in enumerate(section.get('questions', [])):
                q_text = f"{i+1}. {q.get('text')}"
                if 'marks' in q:
                    q_text += f" [{q['marks']} Marks]"
                
                elements.append(Paragraph(q_text, self.styles['QuestionText']))
                
                # Options for MCQs
                if 'options' in q:
                    option_style = ParagraphStyle(
                        name='OptionStyle',
                        parent=self.styles['Normal'],
                        leftIndent=40
                    )
                    for j, opt in enumerate(q['options']):
                        elements.append(Paragraph(f"{chr(97 + j)}) {opt}", option_style))
                
                elements.append(Spacer(1, 5))
            
            elements.append(Spacer(1, 15))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
