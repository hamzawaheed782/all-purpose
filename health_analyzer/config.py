"""Configuration for Health Issue Analyzer."""
import os

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8...B8rw")
MODEL_NAME = "gemini-3.6-flash"

# App
APP_TITLE = "Health Issue Analyzer"
SESSION_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "health_sessions")
os.makedirs(SESSION_DIR, exist_ok=True)
