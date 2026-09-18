"""Health Issue Analyzer - Comprehensive Gradio web app with 4 tabs."""
import gradio as gr
import json
import os
from datetime import datetime

from gemini_client import analyze_health
from emergency_detector import detect_emergencies
from storage_manager import save_session, get_user_history, list_all_users, get_session_by_id
from analytics import generate_severity_trend_chart, generate_category_breakdown, compute_composite_severity
from report_generator import save_report, generate_markdown_report
from config import SESSION_DIR, REPORTS_DIR

def run_analysis(user_id: str, age: int, gender: str, category: str,
                 symptoms: list[str], custom_symptoms: str,
                 severity_rating: int, duration_days: int) -> tuple:
    """Run full health analysis pipeline."""

    all_symptoms = [s.strip() for s in symptoms if s.strip()]
    if custom_symptoms.strip():
        all_symptoms.extend(s.strip() for s in custom_symptoms.split("\n") if s.strip())

    if not all_symptoms:
        return None, "⚠️ Please enter at least one symptom.", None, None

    if not user_id.strip():
        return None, "⚠️ Please enter a User ID.", None, None

    # Compute composite severity
    composite_score = compute_composite_severity(all_symptoms, severity_rating, duration_days, category)

    # Check for emergencies
    symptoms_text = " ".join(all_symptoms)
    emergency = detect_emergencies(symptoms_text, age)

    # Build payload for Gemini
    payload = {
        "user_id": user_id,
        "age": age,
        "gender": gender,
        "category": category,
        "selected_symptoms": all_symptoms,
        "symptom_notes": custom_symptoms.strip(),
        "duration_days": duration_days,
        "user_severity_rating": severity_rating,
        "computed_severity_score": composite_score,
        "emergency_flags": emergency.get("matched_flags", []),
    }

    emergency_guidance = emergency.get("guidance", "")

    # Run Gemini analysis (unless critical emergency)
    if emergency["severity_level"] == "CRITICAL":
        analysis = None
        analysis_output = f"🚨 **CRITICAL EMERGENCY** 🚨\n\n{emergency_guidance}\n\nAI analysis skipped. Seek emergency care immediately."
    else:
        result = analyze_health(payload)
        if result["status"] == "success":
            analysis = result["analysis"]
            analysis_output = _build_analysis_markdown(result, composite_score)
        else:
            analysis = None
            analysis_output = f"⚠️ API Error. Using fallback analysis.\n\n{emergency_guidance}\n\n" + _build_fallback_markdown(result)

    # Save session
    session_data = {
        "user_id": user_id,
        "age": age,
        "gender": gender,
        "category": category,
        "selected_symptoms": all_symptoms,
        "symptom_notes": custom_symptoms.strip(),
        "duration_days": duration_days,
        "user_severity": severity_rating,
        "composite_score": composite_score,
        "emergency_alert": emergency["is_emergency"],
        "emergency_guidance": emergency_guidance,
        "analysis_result": analysis if analysis else {},
    }

    record_id = save_session(user_id, session_data)

    # Also save report
    try:
        md_path, pdf_path = save_report(session_data, REPORTS_DIR)
    except Exception:
        md_path = None
        pdf_path = None

    return record_id, analysis_output, composite_score, emergency

def _build_analysis_markdown(result: dict, composite_score: float) -> str:
    """Build markdown output from analysis result."""
    analysis = result["analysis"]
    output = f"# 🏥 Health Analysis Report\n\n"
    output += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    output += f"**Composite Severity Score:** {composite_score}/10\n\n"

    severity = analysis.get("composite_severity", "Unknown").upper()
    severity_emoji = {"LOW": "🟢", "MODERATE": "🟡", "HIGH": "🔴"}.get(severity, "⚪")
    output += f"## Severity Assessment\n{severity_emoji} **{severity}**\n\n"

    if result.get("emergency_info", {}).get("flags"):
        output += f"### ⚠️ Red Flags Detected\n{', '.join(result['emergency_info']['flags'])}\n\n"

    output += "### Possible Causes\n"
    for cause in analysis.get("possible_causes", []):
        name = cause.get("name", cause)
        likelihood = cause.get("likelihood", "Unknown")
        desc = cause.get("description", "")
        output += f"- **{name}** ({likelihood}): {desc}\n"
    output += "\n"

    output += "### Immediate Recommendations\n"
    for rec in analysis.get("immediate_recommendations", []):
        output += f"- {rec}\n"
    output += "\n"

    output += f"### When to See a Doctor\n{analysis.get('when_to_see_doctor', 'Consult a healthcare professional if symptoms persist or worsen.')}\n\n"

    output += "### General Tips\n"
    for tip in analysis.get("general_tips", []):
        output += f"- {tip}\n"
    output += "\n"

    output += "---\n⚠️ *This analysis is for informational purposes only and is NOT a substitute for professional medical advice.*\n"
    return output

def _build_fallback_markdown(result: dict) -> str:
    """Build markdown from fallback analysis."""
    analysis = result.get("analysis", {})
    return f"### Fallback Analysis\n\n- Severity: {analysis.get('severity', 'Unknown')}\n- Possible Causes: {', '.join(a.get('name', str(a)) for a in analysis.get('possible_causes', []))}\n- Recommendations: {', '.join(analysis.get('immediate_recommendations', []))}\n\n⚠️ This is a fallback analysis. Please consult a professional."

def view_history(user_id: str) -> tuple:
    """Load user history and build UI components."""
    if not user_id.strip():
        return None, None, None

    history = get_user_history(user_id)
    if not history:
        return None, "No history found for this user ID.", None, None

    # Build table data
    table_data = [["Date", "Category", "Symptoms", "Score", "Emergency"]]
    for record in history:
        date = record.get("timestamp", "")[:10]
        cat = record.get("category", "")
        syms = ", ".join(record.get("selected_symptoms", []))[:50]
        score = record.get("composite_score", 0)
        emergency = "🚨" if record.get("emergency_alert") else "✅"
        table_data.append([date, cat, syms, score, emergency])

    # Generate charts
    try:
        trend_chart = generate_severity_trend_chart(user_id)
    except Exception:
        trend_chart = None

    try:
        category_chart = generate_category_breakdown(user_id)
    except Exception:
        category_chart = None

    return table_data, f"Found {len(history)} session(s) for {user_id}", trend_chart, category_chart

def export_report(user_id: str, record_id: str) -> tuple:
    """Generate and return report files."""
    if not user_id.strip() or not record_id.strip():
        return None, None

    session = get_session_by_id(user_id, record_id)
    if not session:
        return None, None

    try:
        md_path, pdf_path = save_report(session, REPORTS_DIR)
        return md_path, pdf_path
    except Exception as e:
        return None, None

def main():
    with gr.Blocks(title="Health Issue Analyzer") as demo:
        gr.Markdown("# 🏥 Comprehensive Health Issue Analyzer")
        gr.Markdown("Powered by Gemini 3.6 Flash. Enter your symptoms for a preliminary health assessment.")
        gr.Markdown("⚠️ **Disclaimer:** This tool provides preliminary health insights only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.")

        with gr.Tabs():
            # Tab 1: Symptom Assessment
            with gr.Tab("🩺 Symptom Assessment"):
                with gr.Row():
                    with gr.Column():
                        user_id = gr.Textbox(label="User ID", placeholder="Enter your user ID", value="user_1")
                        age = gr.Number(label="Age", value=30, minimum=1, maximum=120)
                        gender = gr.Dropdown(label="Gender", choices=["Male", "Female", "Other", "Prefer not to say"], value="Prefer not to say")
                        category = gr.Dropdown(
                            label="Health Category",
                            choices=list(__import__("symptom_data").CATEGORIES.keys()),
                            value="General"
                        )
                        severity = gr.Slider(label="Overall Severity (1-10)", minimum=1, maximum=10, value=5)
                        duration = gr.Number(label="Duration (days)", value=2, minimum=1, maximum=365)
                        symptoms_input = gr.CheckboxGroup(
                            label="Common Symptoms",
                            choices=[],
                            value=[]
                        )
                        custom_symptoms = gr.Textbox(label="Additional Symptoms (one per line)", placeholder="e.g. Dizziness\nFatigue", lines=4)

                        with gr.Row():
                            analyze_btn = gr.Button("🔍 Analyze Symptoms", variant="primary", size="lg")
                            clear_btn = gr.Button("Clear")

                    with gr.Column():
                        record_id_output = gr.Textbox(label="Session ID", interactive=False)
                        composite_score_output = gr.Number(label="Composite Severity Score", interactive=False)
                        emergency_box = gr.Markdown(label="🚨 Emergency Alert")
                        analysis_output = gr.Markdown(label="Analysis Report")

                # Load symptom checkboxes dynamically
                def update_symptoms(category_choice):
                    from symptom_data import CATEGORIES
                    syms = CATEGORIES.get(category_choice, {}).get("symptoms", [])
                    return gr.CheckboxGroup.update(choices=syms)

                category.change(update_symptoms, inputs=[category], outputs=[symptoms_input])

                analyze_btn.click(
                    fn=run_analysis,
                    inputs=[user_id, age, gender, category, symptoms_input, custom_symptoms, severity, duration],
                    outputs=[record_id_output, analysis_output, composite_score_output, emergency_box]
                )
                clear_btn.click(lambda: (None, "", None, "", None, None), outputs=[user_id, custom_symptoms, composite_score_output, emergency_box, analysis_output, record_id_output])

            # Tab 2: History & Trends
            with gr.Tab("📊 History & Trends"):
                with gr.Row():
                    with gr.Column():
                        history_user_id = gr.Textbox(label="User ID", placeholder="Enter user ID to view history", value="user_1")
                        load_history_btn = gr.Button("📋 Load History", variant="primary")
                    with gr.Column():
                        history_info = gr.Markdown(label="Info")

                with gr.Row():
                    trend_chart = gr.Plot(label="Severity Trend")
                    category_chart = gr.Plot(label="Category Distribution")

                with gr.Row():
                    history_table = gr.Dataframe(label="Session History", headers=["Date", "Category", "Symptoms", "Score", "Emergency"])

                load_history_btn.click(
                    fn=view_history,
                    inputs=[history_user_id],
                    outputs=[history_table, history_info, trend_chart, category_chart]
                )

            # Tab 3: Emergency Guidelines
            with gr.Tab("🚨 Emergency Guidelines"):
                gr.Markdown("# 🚨 Emergency Contact Information")
                gr.Markdown("""
                | Region | Emergency Number |
                |--------|-----------------|
                | 🇺🇸 United States | 911 |
                | 🇬🇧 United Kingdom | 999 |
                | 🇪🇺 European Union | 112 |
                | 🌍 Global | Local emergency number |
                """)
                gr.Markdown("### Critical Red-Flag Symptoms (Call Emergency Services Immediately):")
                gr.Markdown("""
                - Crushing or sudden severe chest pain
                - Difficulty breathing / shortness of breath at rest
                - Coughing up blood
                - Sudden face drooping, slurred speech, or numbness
                - Loss of consciousness or seizure
                - Severe headache with stiff neck
                - High fever with stiff neck
                """)
                gr.Markdown("### High-Risk Symptoms (Seek Medical Attention Promptly):")
                gr.Markdown("""
                - Persistent high fever above 103°F
                - Severe abdominal pain
                - Sudden vision loss
                - Chest tightness
                - Blood in urine
                """)
                gr.Markdown("⚠️ **If you or someone else is experiencing a medical emergency, call emergency services immediately. Do not wait for AI analysis.**")

            # Tab 4: Export & Download
            with gr.Tab("📄 Export Reports"):
                with gr.Row():
                    with gr.Column():
                        export_user_id = gr.Textbox(label="User ID", placeholder="Enter user ID", value="user_1")
                        export_record_id = gr.Textbox(label="Record ID", placeholder="Enter record ID from history")
                        export_btn = gr.Button("📥 Generate Report", variant="primary")

                    with gr.Column():
                        md_output = gr.File(label="Markdown Report")
                        pdf_output = gr.File(label="PDF Report")

                export_btn.click(
                    fn=export_report,
                    inputs=[export_user_id, export_record_id],
                    outputs=[md_output, pdf_output]
                )

    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
