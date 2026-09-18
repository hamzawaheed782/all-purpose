"""Symptom metadata, categories, and red-flag definitions."""

CATEGORIES = {
    "Respiratory": {
        "symptoms": ["Cough", "Fever", "Shortness of breath", "Sore throat", "Runny nose", "Chest tightness", "Wheezing"],
        "risk_multiplier": 1.2,
    },
    "Digestive": {
        "symptoms": ["Nausea", "Vomiting", "Diarrhea", "Abdominal pain", "Bloating", "Constipation", "Heartburn"],
        "risk_multiplier": 1.0,
    },
    "Neurological": {
        "symptoms": ["Headache", "Dizziness", "Blurred vision", "Numbness", "Seizures", "Confusion", "Memory loss"],
        "risk_multiplier": 1.3,
    },
    "Cardiovascular": {
        "symptoms": ["Chest pain", "Palpitations", "Swelling in legs", "Fatigue", "Fainting", "High blood pressure"],
        "risk_multiplier": 1.5,
    },
    "Musculoskeletal": {
        "symptoms": ["Joint pain", "Muscle ache", "Back pain", "Stiffness", "Swelling", "Limited range of motion"],
        "risk_multiplier": 1.0,
    },
    "Dermatological": {
        "symptoms": ["Rash", "Itching", "Skin discoloration", "Hair loss", "Acne", "Dry skin", "Lesions"],
        "risk_multiplier": 0.8,
    },
    "General": {
        "symptoms": ["Fatigue", "Fever", "Weight loss", "Night sweats", "Loss of appetite", "Malaise"],
        "risk_multiplier": 1.0,
    },
}

# Red-flag symptoms that require immediate medical attention
RED_FLAGS = {
    "CRITICAL": [
        "crushing chest pain",
        "sudden severe chest pain",
        "difficulty breathing",
        "shortness of breath at rest",
        "coughing up blood",
        "sudden face drooping",
        "slurred speech",
        "sudden numbness or weakness",
        "confusion",
        "loss of consciousness",
        "severe headache with stiff neck",
        "high fever with stiff neck",
        "seizure",
        "uncontrolled bleeding",
    ],
    "HIGH": [
        "persistent high fever above 103f",
        "severe abdominal pain",
        "sudden vision loss",
        "slurred speech",
        "sudden severe headache",
        "chest tightness",
        "rapid heartbeat",
        "severe dizziness",
        "blood in urine",
        "severe vomiting",
    ],
}

EMERGENCY_CONTACTS = {
    "US": "911",
    "UK": "999",
    "EU": "112",
    "GLOBAL": "Local emergency number",
}

def get_category_risk(category: str) -> float:
    """Get risk multiplier for a category."""
    return CATEGORIES.get(category, {}).get("risk_multiplier", 1.0)

def get_all_red_flag_terms() -> list[str]:
    """Get all red-flag terms across all severity levels."""
    terms = []
    for level_terms in RED_FLAGS.values():
        terms.extend(level_terms)
    return terms
