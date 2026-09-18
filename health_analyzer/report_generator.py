"""Report generation module - PDF and Markdown."""
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_markdown_report(session_data: dict) -> str:
    """Generate a Markdown report from session data."""
    md = f"""# Health Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**User ID:** {session_data.get('user_id', 'N/A')}
**Age:** {session_data.get('age', 'N/A')}
**Category:** {session_data.get('category', 'N/A')}
**Symptoms:** {', '.join(session_data.get('selected_symptoms', []))}
**Duration:** {session_data.get('duration_days', 'N/A')} days
**Composite Severity Score:** {session_data.get('composite_score', 'N/A')}

---

## Emergency Assessment
{session_data.get('emergency_guidance', 'No emergency flags detected.')}

## Possible Causes
{chr(10).join(f'- {c.get("name", c)} ({c.get("likelihood", "Unknown")})' for c in session_data.get('analysis_result', {}).get('possible_causes', []))}

## Immediate Recommendations
{chr(10).join(f'- {r}' for r in session_data.get('analysis_result', {}).get('immediate_recommendations', []))}

## When to See a Doctor
{session_data.get('analysis_result', {}).get('when_to_see_doctor', 'Consult a healthcare professional if symptoms persist.')}

## General Tips
{chr(10).join(f'- {t}' for t in session_data.get('analysis_result', {}).get('general_tips', []))}

---

⚠️ **Disclaimer:** This report is for informational purposes only and is NOT a substitute for professional medical advice. Always consult a qualified healthcare professional.
"""
    return md

def generate_pdf_report(session_data: dict, output_path: str):
    """Generate a PDF report using reportlab."""
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=20, spaceAfter=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading1'], fontSize=14, spaceAfter=10)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, spaceAfter=8)

    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    story = []

    story.append(Paragraph("Health Analysis Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
    story.append(Paragraph(f"User ID: {session_data.get('user_id', 'N/A')}", body_style))
    story.append(Spacer(1, 0.5 * inch))

    # Severity
    story.append(Paragraph("Severity Assessment", heading_style))
    severity = session_data.get('analysis_result', {}).get('severity', 'Unknown')
    story.append(Paragraph(f"Severity: {severity}", body_style))
    story.append(Paragraph(f"Composite Score: {session_data.get('composite_score', 'N/A')}", body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Emergency
    story.append(Paragraph("Emergency Assessment", heading_style))
    story.append(Paragraph(session_data.get('emergency_guidance', 'No emergency flags detected.'), body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Causes
    story.append(Paragraph("Possible Causes", heading_style))
    causes = session_data.get('analysis_result', {}).get('possible_causes', [])
    cause_text = "<br/>".join(f"• {c.get('name', c)} ({c.get('likelihood', 'Unknown')})" for c in causes)
    story.append(Paragraph(cause_text, body_style))
    story.append(Spacer(1, 0.3 * inch))

    # Recommendations
    story.append(Paragraph("Immediate Recommendations", heading_style))
    recs = session_data.get('analysis_result', {}).get('immediate_recommendations', [])
    rec_text = "<br/>".join(f"• {r}" for r in recs)
    story.append(Paragraph(rec_text, body_style))
    story.append(Spacer(1, 0.3 * inch))

    # When to see doctor
    story.append(Paragraph("When to See a Doctor", heading_style))
    story.append(Paragraph(session_data.get('analysis_result', {}).get('when_to_see_doctor', 'Consult a professional.'), body_style))
    story.append(Spacer(1, 0.5 * inch))

    # Disclaimer
    disclaimer_style = ParagraphStyle('Disclaimer', parent=body_style, textColor=colors.red)
    story.append(Paragraph("⚠️ This report is for informational purposes only and is NOT a substitute for professional medical advice.", disclaimer_style))

    doc.build(story)
    return output_path

def save_report(session_data: dict, reports_dir: str):
    """Save both PDF and Markdown reports."""
    user_id = session_data.get('user_id', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = f"{user_id}_{timestamp}"

    # Markdown
    md_path = os.path.join(reports_dir, f"{base_name}.md")
    md_content = generate_markdown_report(session_data)
    with open(md_path, 'w') as f:
        f.write(md_content)

    # PDF
    pdf_path = os.path.join(reports_dir, f"{base_name}.pdf")
    generate_pdf_report(session_data, pdf_path)

    return md_path, pdf_path
