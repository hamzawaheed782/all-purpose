"""Enhanced Gemini API client with structured analysis."""
import os
import json
import re
import google.genai as genai
from google.genai import types
from config import MODEL_NAME
from emergency_detector import detect_emergencies
from analytics import compute_composite_severity

def analyze_health(payload: dict) -> dict:
    """Send structured health payload to Gemini for analysis.

    Args:
        payload: Dict with user_id, age, gender, category, selected_symptoms,
                 symptom_notes, duration_days, user_severity_rating,
                 computed_severity_score, emergency_flags

    Returns:
        Dict with status, analysis, raw_response, model_used, emergency_info
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    model = client.models

    # Extract data
    user_id = payload.get("user_id", "anonymous")
    age = payload.get("age")
    gender = payload.get("gender", "")
    category = payload.get("category", "")
    symptoms = payload.get("selected_symptoms", [])
    symptom_notes = payload.get("symptom_notes", "")
    duration_days = payload.get("duration_days", 0)
    user_severity = payload.get("user_severity_rating", 5)
    computed_score = payload.get("computed_severity_score", 0)
    emergency_flags = payload.get("emergency_flags", [])

    # Build prompt
    prompt = f"""You are a medical analysis assistant. Provide a structured health analysis. NEVER provide a definitive diagnosis. ALWAYS recommend seeing a qualified healthcare professional. Respond in this exact JSON format:

{{
  "emergency_warning": "None or specific red-flag notice",
  "possible_causes": [
    {{"name": "Condition Name", "likelihood": "High/Medium/Low", "description": "Brief description"}}
  ],
  "composite_severity": "Low|Moderate|High",
  "immediate_recommendations": ["Recommendation 1", "Recommendation 2"],
  "when_to_see_doctor": "Specific guidance on when to seek medical attention",
  "general_tips": ["Tip 1", "Tip 2"]
}}

PATIENT INFORMATION:
- Age: {age}
- Gender: {gender}
- Category: {category}
- Symptoms: {', '.join(symptoms)}
- Symptom details: {symptom_notes}
- Duration: {duration_days} days
- User severity rating: {user_severity}/10
- Computed severity score: {computed_score}
- Red flags detected: {', '.join(emergency_flags) if emergency_flags else 'None'}

IMPORTANT: This is for informational purposes only and is NOT a substitute for professional medical advice, diagnosis, or treatment."""

    try:
        response = model.generate_content(
            model=f"models/{MODEL_NAME}",
            contents=prompt,
        )
        text = response.text

        # Try to extract JSON
        analysis = _parse_json_response(text)

        return {
            "status": "success",
            "analysis": analysis,
            "raw_response": text,
            "model_used": MODEL_NAME,
            "emergency_info": {
                "flags": emergency_flags,
                "score": computed_score,
                "severity_level": _get_severity_level(computed_score),
            },
        }

    except Exception as e:
        # Fallback to rule-based analysis
        return {
            "status": "fallback",
            "analysis": _rule_based_fallback(symptoms, category, computed_score),
            "error": str(e),
        }

def _parse_json_response(text: str) -> dict:
    """Parse JSON from Gemini response with markdown wrappers."""
    try:
        # Try direct JSON
        start = text.rfind("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass

    # Try extracting with regex (handle markdown code blocks)
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group()
            # Fix common issues
            json_str = json_str.replace("'", '"')  # single quotes
            return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass

    return {"raw_response": text, "possible_causes": [], "severity": "unknown"}

def _get_severity_level(score: float) -> str:
    """Map numeric score to severity level."""
    if score >= 7:
        return "High"
    elif score >= 4:
        return "Moderate"
    else:
        return "Low"

def _rule_based_fallback(symptoms: list[str], category: str, score: float) -> dict:
    """Rule-based analysis when API fails."""
    severity = _get_severity_level(score)
    return {
        "possible_causes": [
            {"name": f"{category} issue", "likelihood": "Possible", "description": f"Symptoms suggest a possible {category.lower()} condition"}
        ],
        "severity": severity,
        "immediate_recommendations": ["Rest", "Stay hydrated", "Monitor symptoms"],
        "when_to_see_doctor": "Consult a healthcare professional if symptoms worsen or persist beyond 3 days",
        "general_tips": ["Get adequate rest", "Maintain hydration", "Avoid strenuous activity"],
    }
