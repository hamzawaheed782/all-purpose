"""Emergency detection engine for red-flag symptoms."""
from symptom_data import RED_FLAGS, EMERGENCY_CONTACTS

def detect_emergencies(symptoms_text: str, age: int = None) -> dict:
    """Evaluate symptoms against red-flag rules.

    Returns:
        Dict with is_emergency, severity_level, matched_flags, guidance
    """
    text_lower = symptoms_text.lower()
    matched_critical = []
    matched_high = []

    for term in RED_FLAGS.get("CRITICAL", []):
        if term.lower() in text_lower:
            matched_critical.append(term)

    for term in RED_FLAGS.get("HIGH", []):
        if term.lower() in text_lower:
            matched_high.append(term)

    if matched_critical:
        return {
            "is_emergency": True,
            "severity_level": "CRITICAL",
            "matched_flags": matched_critical,
            "guidance": (
                "🚨 CRITICAL EMERGENCY DETECTED 🚨\n\n"
                "The following critical red-flag symptoms were detected:\n"
                f"{', '.join(matched_critical)}\n\n"
                "IMMEDIATE ACTION REQUIRED:\n"
                "- Call emergency services NOW (911 in US, 999 in UK, 112 in EU)\n"
                "- Do not wait for AI analysis\n"
                "- Seek emergency medical attention immediately\n\n"
                "This tool is NOT a substitute for emergency medical care."
            ),
        }

    if matched_high:
        return {
            "is_emergency": True,
            "severity_level": "HIGH",
            "matched_flags": matched_high,
            "guidance": (
                "⚠️ HIGH-RISK SYMPTOMS DETECTED ⚠️\n\n"
                "The following high-risk symptoms were detected:\n"
                f"{', '.join(matched_high)}\n\n"
                "RECOMMENDED ACTION:\n"
                "- Seek medical attention promptly\n"
                "- Visit an urgent care facility or emergency room\n"
                "- Monitor symptoms closely and do not ignore worsening\n\n"
                "Please consult a healthcare professional as soon as possible."
            ),
        }

    return {
        "is_emergency": False,
        "severity_level": "NORMAL",
        "matched_flags": [],
        "guidance": "No emergency symptoms detected. Continue with regular analysis.",
    }
