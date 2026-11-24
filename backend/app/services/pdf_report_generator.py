"""
PDF Interview Report Generator
Creates professional downloadable PDF reports from interview sessions.
"""

from datetime import datetime
from html import escape
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFReportGenerator:
    """Generate professional PDF interview reports."""
    
    def __init__(self, filename="interview_report.pdf"):
        self.filename = filename
        self.doc = None
        self.story = []
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report."""
        if not REPORTLAB_AVAILABLE or not self.styles:
            return
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#3498db'),
            borderWidth=2,
            borderPadding=10
        ))
        
        # Score style
        self.styles.add(ParagraphStyle(
            name='ScoreHighlight',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#27ae60'),
            fontName='Helvetica-Bold'
        ))
    
    def _get_performance_level_text(self, score):
        """Get performance level and recommendation based on score."""
        if score >= 8.5:
            return "Excellent", "Strong Candidate - Highly Recommended"
        elif score >= 7:
            return "Good", "Recommended"
        elif score >= 5:
            return "Satisfactory", "Needs Improvement - Further Training Recommended"
        else:
            return "Needs Improvement", "Not Recommended"
    
    def _create_header(self, session_data):
        """Create the report header with candidate and interview information."""
        resume_data = session_data.get("resume_data", {})
        candidate_name = resume_data.get("name", "Candidate")
        skills = resume_data.get("skills", [])
        projects = resume_data.get("projects", [])
        experience = resume_data.get("experience", [])
        ats_score = resume_data.get("ats_score", session_data.get("ats_score", 0))
        resume_score = resume_data.get("resume_score", session_data.get("resume_score", 0))
        interview_score = session_data.get("average_score", 0)
        jd_match_score = resume_data.get("jd_match_score") or session_data.get("jd_match_score") or 0
        
        # Title
        if self.styles:
            title = Paragraph("Interview Report", self.styles['CustomTitle'])
            self.story.append(title)
        
        # Interview info table
        interview_info = [
            ["Candidate Name:", candidate_name],
            ["Email:", resume_data.get("email", "Not provided")],
            ["Department:", resume_data.get("department", "Not specified")],
            ["Interview Date:", self._format_interview_date(session_data)],
            ["ATS Score:", f"{ats_score}/100"],
            ["Resume Score:", f"{resume_score}/100"],
            ["JD Match Score:", f"{jd_match_score}/100"],
            ["Interview Score:", f"{interview_score}/10"],
            ["Total Questions:", str(len(session_data.get("scores", [])))],
            ["Interview Status:", "Completed"]
        ]
        
        info_table = Table(interview_info, colWidths=[2.6*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7'))
        ]))
        
        self.story.append(info_table)
        self.story.append(Spacer(1, 0.2*inch))

        self.story.append(Paragraph(
            self._format_details(resume_data),
            self.styles['Normal']
        ))
        self.story.append(Spacer(1, 0.2*inch))

    def _format_interview_date(self, session_data):
        created_at = session_data.get("created_at")
        if created_at:
            try:
                return datetime.fromisoformat(created_at).strftime("%B %d, %Y %H:%M UTC")
            except (TypeError, ValueError):
                return str(created_at)
        return "Not recorded"

    def _format_value(self, value):
        if value is None or value == "":
            return "Not provided"
        if isinstance(value, (list, tuple, set)):
            return "<br/>".join(f"- {escape(str(item))}" for item in value) or "Not provided"
        if isinstance(value, dict):
            return "<br/>".join(
                f"<b>{escape(str(key))}:</b> {self._format_value(item)}"
                for key, item in value.items()
            ) or "Not provided"
        return escape(str(value)).replace("\n", "<br/>")

    def _format_details(self, details):
        return "<br/>".join(
            f"<b>{escape(str(label))}:</b> {self._format_value(value)}"
            for label, value in details.items()
        )
    
    def _create_scores_section(self, session_data):
        """Create the scores and performance section."""
        scores = session_data.get("scores", [])
        average_score = session_data.get("average_score", 0)
        resume_data = session_data.get("resume_data", {})
        ats_score = resume_data.get("ats_score", 0)
        resume_score = resume_data.get("resume_score", 0)
        jd_match_score = resume_data.get("jd_match_score") or session_data.get("jd_match_score") or 0
        communication_metrics = session_data.get("communication_metrics", [])
        communication_score = 0
        if communication_metrics:
            values = [item.get("score") for item in communication_metrics if item.get("score") is not None]
            communication_score = round(sum(values) / len(values), 1) if values else 0
        
        if not self.styles:
            return
        
        header = Paragraph("Performance Summary", self.styles['SectionHeader'])
        self.story.append(header)
        
        perf_level, recommendation = self._get_performance_level_text(average_score)
        
        scores_data = [
            ["Metric", "Score / Rating"],
            ["ATS Score", f"{ats_score}/100"],
            ["Resume Score", f"{resume_score}/100"],
            ["JD Match Score", f"{jd_match_score}/100"],
            ["Overall Interview Score", f"{average_score}/10"],
            ["Performance Level", perf_level],
            ["Questions Answered", str(len(scores))],
            ["Communication Score", f"{communication_score}/10"],
            ["Recommendation", recommendation]
        ]
        
        scores_table = Table(scores_data, colWidths=[3*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10)
        ]))
        
        self.story.append(scores_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def _create_questions_answers_section(self, session_data):
        """Create detailed questions and answers section."""
        questions = session_data.get("questions", [])
        answers = session_data.get("answers", [])
        scores = session_data.get("scores", [])
        feedback = session_data.get("feedback", [])
        
        if not self.styles:
            return
        
        header = Paragraph("Questions & Answers", self.styles['SectionHeader'])
        self.story.append(header)
        
        for i, question in enumerate(questions, 1):
            answer = answers[i - 1] if i - 1 < len(answers) else "No answer provided"
            score = scores[i - 1] if i - 1 < len(scores) else 0
            fb = feedback[i - 1] if i - 1 < len(feedback) else ""
            q_header = f"Question {i}: Score {score}/10"
            self.story.append(Paragraph(q_header, self.styles['Heading3']))
            self.story.append(Paragraph(f"<b>Q:</b> {self._format_value(question)}", self.styles['Normal']))
            self.story.append(Spacer(1, 0.05*inch))
            answer_text = self._format_value(answer)
            self.story.append(Paragraph(f"<b>A:</b> {answer_text}", self.styles['Normal']))
            self.story.append(Spacer(1, 0.05*inch))
            if fb:
                self.story.append(Paragraph(f"<b>Feedback:</b> {self._format_value(fb)}", self.styles['Normal']))
            self.story.append(Spacer(1, 0.15*inch))
        
        self.story.append(Spacer(1, 0.2*inch))
    
    def _create_strengths_weaknesses_section(self, session_data):
        """Create strengths and weaknesses section."""
        if not self.styles:
            return
        
        header = Paragraph("Technical Analysis", self.styles['SectionHeader'])
        self.story.append(header)
        
        resume_data = session_data.get("resume_data", {})
        skills = resume_data.get("skills", [])
        projects = resume_data.get("projects", [])
        strengths = session_data.get("strengths") or []
        weaknesses = session_data.get("weaknesses") or []
        technical_strengths = resume_data.get("strengths", strengths)
        technical_weaknesses = resume_data.get("weaknesses", weaknesses)
        
        strengths_table_data = [["Category", "Details"]]
        
        if skills:
            strengths_table_data.append(["Technical Skills", self._format_value(skills)])
        
        if projects:
            strengths_table_data.append(["Projects", self._format_value(projects)])

        if technical_strengths:
            strengths_table_data.append(["Strengths", self._format_value(technical_strengths)])
        if technical_weaknesses:
            strengths_table_data.append(["Weaknesses", self._format_value(technical_weaknesses)])
        
        communication_score = session_data.get("communication_score", 0)
        comm_level = "Strong" if communication_score >= 7 else "Moderate" if communication_score >= 5 else "Needs Improvement"
        strengths_table_data.append(["Communication Score", f"{communication_score}/10 ({comm_level})"])

        communication_metrics = session_data.get("communication_metrics", [])
        if communication_metrics:
            strengths_table_data.append(["Communication Performance", self._format_value(communication_metrics)])

        learning_recommendations = (
            session_data.get("learning_recommendations")
            or session_data.get("learning_roadmap")
            or session_data.get("recommendations")
        )
        strengths_table_data.append([
            "Learning Recommendations",
            self._format_value(learning_recommendations) if learning_recommendations else "Not recorded in this session"
        ])
        
        strengths_table = Table(strengths_table_data, colWidths=[2*inch, 3*inch])
        strengths_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
        ]))
        
        self.story.append(strengths_table)
        self.story.append(Spacer(1, 0.2*inch))
    
    def _create_recommendation_section(self, session_data):
        """Create final recommendation section."""
        if not self.styles:
            return
        
        average_score = session_data.get("average_score", 0)
        perf_level, recommendation = self._get_performance_level_text(average_score)
        resume_data = session_data.get("resume_data", {})
        candidate_name = resume_data.get("name", "Candidate")
        
        header = Paragraph("Final Recommendation", self.styles['SectionHeader'])
        self.story.append(header)
        
        rec_text = self._format_details({
            "Candidate": candidate_name,
            "Performance Level": perf_level,
            "Recommendation": recommendation,
            "Interview Result": f"{average_score}/10",
            "ATS Score": f"{resume_data.get('ats_score', 0)}/100",
            "Resume Score": f"{resume_data.get('resume_score', 0)}/100",
            "JD Match Score": f"{resume_data.get('jd_match_score', session_data.get('jd_match_score', 0))}/100",
        })
        
        self.story.append(Paragraph(rec_text, self.styles['Normal']))
        self.story.append(Spacer(1, 0.2*inch))
    
    def _get_recommendation_text(self, score):
        """Get recommendation text based on score."""
        if score >= 8.5:
            return "strong technical skills and are well-suited for the role"
        elif score >= 7:
            return "good technical understanding and are a viable candidate"
        elif score >= 5:
            return "basic technical knowledge but would benefit from additional training"
        else:
            return "limited technical understanding and would need significant development"
    
    def generate_report(self, session_data, output_path=None):
        """
        Generate a complete PDF report from session data.
        
        Args:
            session_data: Interview session data dictionary
            output_path: Optional path to save the PDF file
        
        Returns:
            Path to generated PDF file
        """
        if not REPORTLAB_AVAILABLE:
            return self._generate_text_report(session_data)
        
        output_path = output_path or self.filename
        
        # Create the PDF document
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Build the report
        self._create_header(session_data)
        self._create_scores_section(session_data)
        
        # Add page break if needed
        if session_data.get("questions"):
            self.story.append(PageBreak())
            self._create_questions_answers_section(session_data)
        
        self._create_strengths_weaknesses_section(session_data)
        self._create_recommendation_section(session_data)
        
        # Build PDF
        try:
            self.doc.build(self.story)
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
    
    def _generate_text_report(self, session_data):
        """
        Generate a valid fallback PDF when the reportlab dependency is unavailable.
        This keeps the report openable while preserving the same downloadable route.
        """
        output_path = self.filename
        if not output_path.lower().endswith('.pdf'):
            output_path = output_path.replace('.txt', '.pdf')

        resume_data = session_data.get("resume_data", {})
        candidate_name = resume_data.get("name", "Candidate")
        average_score = session_data.get("average_score", 0)
        perf_level, recommendation = self._get_performance_level_text(average_score)

        def _pdf_escape(value):
            return str(value).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

        report_lines = ["Interview Report", f"Candidate: {candidate_name}", f"Interview Date: {self._format_interview_date(session_data)}"]
        report_lines.extend([
            f"Overall Score: {average_score}/10",
            f"Performance Level: {perf_level}",
            f"Recommendation: {recommendation}",
            "",
            "Candidate Details:",
        ])
        report_lines.extend(f"{key}: {value}" for key, value in resume_data.items())
        report_lines.extend(["", "Questions and Answers:"])
        questions = session_data.get("questions", [])
        answers = session_data.get("answers", [])
        scores = session_data.get("scores", [])
        feedback = session_data.get("feedback", [])
        for index, question in enumerate(questions, 1):
            report_lines.extend([
                f"Question {index}: {question}",
                f"Answer: {answers[index - 1] if index - 1 < len(answers) else 'No answer provided'}",
                f"Score: {scores[index - 1] if index - 1 < len(scores) else 0}/10",
                f"Feedback: {feedback[index - 1] if index - 1 < len(feedback) else ''}",
            ])
        report_lines.extend(["", "Communication Performance:", str(session_data.get("communication_metrics", []))])
        escaped_lines = [f"0 -16 Td ({_pdf_escape(line)}) Tj" for line in report_lines]
        content = "BT\n/F1 10 Tf\n36 756 Td\n" + "\n".join(escaped_lines) + "\nET"

        objects = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            f"<< /Length {len(content.encode('latin-1', 'replace'))} >>\nstream\n{content}\nendstream".encode('latin-1', 'replace'),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        ]

        try:
            pdf = bytearray(b"%PDF-1.4\n")
            offsets = [0]
            for index, obj in enumerate(objects, start=1):
                offsets.append(len(pdf))
                pdf.extend(f"{index} 0 obj\n".encode('latin-1'))
                pdf.extend(obj)
                pdf.extend(b"\nendobj\n")

            xref_offset = len(pdf)
            pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode('latin-1'))
            pdf.extend(b"0000000000 65535 f \n")
            for offset in offsets[1:]:
                pdf.extend(f"{offset:010d} 00000 n \n".encode('latin-1'))
            pdf.extend(f"trailer\n<< /Root 1 0 R /Size {len(objects) + 1} >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin-1'))

            with open(output_path, 'wb') as f:
                f.write(pdf)
            return output_path
        except Exception as e:
            print(f"Error generating fallback PDF: {e}")
            return None


def generate_interview_report_pdf(session_data, output_filename=None):
    """
    Convenience function to generate a PDF report from interview data.
    
    Args:
        session_data: Interview session data
        output_filename: Optional custom filename
    
    Returns:
        Path to the generated PDF file
    """
    filename = output_filename or f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generator = PDFReportGenerator(filename)
    return generator.generate_report(session_data)
