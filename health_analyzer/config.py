"""Configuration for Health Issue Analyzer."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-3.6-flash"
APP_TITLE = "Comprehensive Health Issue Analyzer"
SESSION_DIR = os.path.join(BASE_DIR, "sessions")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(SESSION_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
