"""Health Issue Analyzer - Gradio web app."""
import gradio as gr
import json
import os
from gemini_client import analyze_health

def analyze(symptoms_text: str, age: int, duration: int) -> dict:
    """Process health analysis request."""
    symptoms = [s.strip() for s in symptoms_text.split("\n") if s.strip()]

    if not symptoms:
        return {"error": "Please enter at least one symptom"}

    result = analyze_health(
        symptoms=symptoms,
        age=age if age and age > 0 else None,
        duration_days=duration if duration and duration > 0 else None,
    )

    if result["status"] == "error":
        return {"error": f"API Error: {result['error']}"}

    analysis = result["analysis"]

    # Build markdown output
    output = f"# Health Analysis Report\n\n"
    output += f"**Model Used:** {result.get('model_used', 'gemini-3.6-flash')}\n\n"

    severity = analysis.get("severity", "unknown").upper()
    severity_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(severity, "⚪")
    output += f"## Severity Assessment\n{severity_emoji} **{severity}**\n\n"

    output += "### Possible Causes\n"
    for cause in analysis.get("possible_causes", []):
        output += f"- {cause}\n"
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

    output += "---\n⚠️ *This analysis is for informational purposes only and is NOT a substitute for professional medical advice. Always consult a qualified healthcare professional.*\n"

    return output

def main():
    with gr.Blocks(title="Health Issue Analyzer") as demo:
        gr.Markdown("# 🏥 Health Issue Analyzer")
        gr.Markdown("Enter your symptoms and get a preliminary analysis powered by Gemini AI.")

        with gr.Row():
            with gr.Column():
                symptoms = gr.Textbox(
                    label="Symptoms (one per line)",
                    placeholder="e.g. Headache\nFever\nFatigue",
                    lines=5,
                )
                with gr.Row():
                    age = gr.Number(label="Age", value=30, minimum=1, maximum=120)
                    duration = gr.Number(label="Duration (days)", value=2, minimum=1, maximum=365)

                submit_btn = gr.Button("Analyze Health", variant="primary", size="lg")

            with gr.Column():
                result = gr.Markdown(label="Analysis Report")

        gr.Markdown(
            "⚠️ **Disclaimer:** This tool provides preliminary health insights only. "
            "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
            "Always consult a qualified healthcare professional for any medical concerns."
        )

        submit_btn.click(analyze, inputs=[symptoms, age, duration], outputs=result)

    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    main()
