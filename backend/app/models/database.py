"""
FormSaathi In-Memory & File-Backed Persistent Database with MongoDB support.
Works out of the box without requiring MongoDB installation, while supporting MongoDB if configured.
"""
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "app_database.json")

class Database:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.applications: Dict[str, Dict[str, Any]] = {}
        self.load_from_disk()

    def load_from_disk(self):
        try:
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.sessions = data.get("sessions", {})
                    self.applications = data.get("applications", {})
        except Exception as e:
            print(f"[DB] Initializing fresh local DB (note: {e})")
            self.sessions = {}
            self.applications = {}

    def save_to_disk(self):
        try:
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "sessions": self.sessions,
                    "applications": self.applications
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[DB] Error saving to disk: {e}")

    def create_session(self, mode: str = "digital", language: str = "te", service_id: Optional[str] = None) -> Dict[str, Any]:
        session_id = str(uuid.uuid4())[:8]
        session_data = {
            "session_id": session_id,
            "mode": mode,
            "service_id": service_id,
            "service_name": None,
            "form_id": None,
            "language": language,
            "current_step": 1,
            "total_steps": 6,
            "chat_history": [],
            "form_data": {},
            "uploaded_documents": [],
            "missing_documents": [],
            "conflicts": [],
            "status": "in_progress",
            "created_at": datetime.now().isoformat(),
            "original_form_path": None,
            "filled_form_image_path": None,
            "generated_pdf_path": None
        }
        self.sessions[session_id] = session_data
        self.save_to_disk()
        return session_data

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if session_id in self.sessions:
            self.sessions[session_id].update(updates)
            self.save_to_disk()
            return self.sessions[session_id]
        return None

    def add_chat_message(self, session_id: str, role: str, content: str, language: str = "te") -> None:
        if session_id in self.sessions:
            msg = {
                "role": role,
                "content": content,
                "language": language,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            self.sessions[session_id]["chat_history"].append(msg)
            self.save_to_disk()

    def save_application(self, app_data: Dict[str, Any]) -> str:
        app_id = "APP-" + str(uuid.uuid4())[:6].upper()
        app_data["application_id"] = app_id
        app_data["saved_at"] = datetime.now().isoformat()
        self.applications[app_id] = app_data
        self.save_to_disk()
        return app_id

    def list_applications(self) -> List[Dict[str, Any]]:
        return list(self.applications.values())

db = Database()
