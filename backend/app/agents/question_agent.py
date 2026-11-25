"""
FormSaathi Question Agent.
Sequentially asks only required questions, manages conditional logic, and supports all major Indian languages.
"""
from typing import Dict, Any, List, Optional
from app.rag.knowledge_base import SERVICES_DB

class QuestionAgent:
    def get_next_question(
        self,
        service_id: str,
        current_form_data: Dict[str, Any],
        language: str = "hi",
        custom_fields: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        fields = []
        if custom_fields:
            fields = custom_fields
        elif service_id in SERVICES_DB:
            fields = SERVICES_DB[service_id].get("fields", [])

        for field in fields:
            field_id = field.get("id") or field.get("name")
            
            # Check conditional logic
            if "conditional_on" in field:
                parent_id = field["conditional_on"]
                required_val = field.get("conditional_value")
                parent_val = current_form_data.get(parent_id)
                # If parent condition not satisfied, skip this question
                if parent_val != required_val:
                    continue

            # If field is not yet filled or empty
            val = current_form_data.get(field_id)
            if val is None or str(val).strip() == "":
                q_text = field.get(f"question_{language}")
                if not q_text:
                    q_text = field.get("question_hi") or field.get("question_te") or field.get("question_en")

                label = field.get(f"label_{language}") or field.get("label_hi") or field.get("label_te") or field.get("label_en")
                if not q_text:
                    q_text = f"कृपया अपना {label} बताएं?" if language == "hi" else f"Please provide your {label}."

                return {
                    "field_id": field_id,
                    "label": label,
                    "question": q_text,
                    "field_type": field.get("type", "text"),
                    "options": field.get("options", []),
                    "required": field.get("required", True)
                }

        return None # All questions answered!

question_agent = QuestionAgent()
