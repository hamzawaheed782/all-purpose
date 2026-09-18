"""Persistent session storage manager using JSON files."""
import json
import os
import uuid
from datetime import datetime, timezone
from config import SESSION_DIR

def save_session(user_id: str, session_data: dict) -> str:
    """Save a session record for a user. Returns the record ID."""
    record_id = f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    record = {
        "record_id": record_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **session_data,
    }

    user_file = os.path.join(SESSION_DIR, f"{user_id}.json")
    if os.path.exists(user_file):
        with open(user_file) as f:
            data = json.load(f)
    else:
        data = {"user_id": user_id, "records": []}

    data["records"].append(record)

    with open(user_file, "w") as f:
        json.dump(data, f, indent=2)

    return record_id

def get_user_history(user_id: str) -> list[dict]:
    """Get all records for a user."""
    user_file = os.path.join(SESSION_DIR, f"{user_id}.json")
    if not os.path.exists(user_file):
        return []
    with open(user_file) as f:
        data = json.load(f)
    return data.get("records", [])

def list_all_users() -> list[str]:
    """List all user IDs."""
    users = []
    for fname in os.listdir(SESSION_DIR):
        if fname.endswith(".json"):
            users.append(fname.replace(".json", ""))
    return users

def get_session_by_id(user_id: str, record_id: str) -> dict | None:
    """Get a specific session record."""
    history = get_user_history(user_id)
    for record in history:
        if record.get("record_id") == record_id:
            return record
    return None
