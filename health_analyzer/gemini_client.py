"""Gemini API client for health analysis."""
import os
import json
import google.genai as genai
from google.genai import types

def get_client():
    """Get authenticated Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    return genai.Client(api_key=api_key)

def analyze_health(symptoms: list[str], age: int = None, duration_days: int = None) -> dict:
    """Send health symptoms to Gemini for analysis.

    Args:
        symptoms: List of symptom descriptions
        age: Patient age (optional)
        duration_days: How long symptoms have persisted (optional)

    Returns:
        Parsed analysis dict with recommendations
    """
    client = get_client()
    model = client.models

    # Build prompt
    prompt_parts = [
        "You are a medical analysis assistant. Given the following symptoms, "
        "provide a structured health analysis. NEVER provide a definitive diagnosis. "
        "ALWAYS recommend seeing a qualified healthcare professional. "
        "Respond in this exact JSON format:",
        "",
        '{"possible_causes": ["...", "..."], "severity": "low|medium|high", '
        '"immediate_recommendations": ["...", "..."], '
        '"when_to_see_doctor": "...", "general_tips": ["...", "..."]}',
        "",
        "SYMPTOMS:",
    ]
    for s in symptoms:
        prompt_parts.append(f"  - {s}")

    if age:
        prompt_parts.append(f"Patient age: {age}")
    if duration_days:
        prompt_parts.append(f"Symptoms duration: {duration_days} days")

    prompt_parts.append(
        "\nIMPORTANT: This is for informational purposes only and is NOT a "
        "substitute for professional medical advice."
    )

    try:
        # Use Gemini 3.6 Flash for text analysis
        response = model.generate_content(
            model="models/gemini-3.6-flash",
            contents=prompt_parts,
        )
        text = response.text

        # Try to extract JSON from response
        try:
            # Find JSON block
            start = text.rfind("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                analysis = json.loads(json_str)
            else:
                analysis = {"raw_response": text, "possible_causes": [], "severity": "unknown"}
        except (json.JSONDecodeError, ValueError):
            analysis = {"raw_response": text, "possible_causes": [], "severity": "unknown"}

        return {
            "status": "success",
            "analysis": analysis,
            "raw_response": text,
            "model_used": "gemini-3.6-flash",
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }
