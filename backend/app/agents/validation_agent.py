"""
FormSaathi Validation & Conflict Detection Agent.
Compares user-entered answers with OCR-extracted document values across Indian languages.
Identifies discrepancies (DOB, Name, Income, etc.) and prompts user to resolve them explicitly.
"""
from typing import Dict, Any, List

class ValidationAgent:
    def detect_conflicts(
        self,
        form_data: Dict[str, Any],
        uploaded_docs: List[Dict[str, Any]],
        language: str = "hi"
    ) -> List[Dict[str, Any]]:
        conflicts = []
        
        # Aggregate document extracted data
        doc_extracted = {}
        doc_sources = {}
        for doc in uploaded_docs:
            source_name = doc.get("doc_name", "Uploaded Document")
            data = doc.get("extracted_data", {})
            for k, v in data.items():
                if v:
                    doc_extracted[k] = str(v).strip()
                    doc_sources[k] = source_name

        # 1. Date of Birth Check
        user_dob = form_data.get("dob")
        doc_dob = doc_extracted.get("dob")
        if user_dob and doc_dob:
            clean_u_dob = str(user_dob).strip().replace("-", "/")
            clean_d_dob = str(doc_dob).strip().replace("-", "/")
            if clean_u_dob != clean_d_dob:
                source = doc_sources.get("dob", "Aadhaar Card")
                
                # Multilingual warning messages
                warn_hi = f"⚠️ आपकी जन्म तिथि में अंतर पाया गया। आपने {user_dob} दर्ज किया है, लेकिन आपके {source} में {doc_dob} है। कौन सा मान उपयोग करें?"
                warn_te = f"⚠️ మీ పుట్టిన తేదీలో తేడా గమనించాను. మీరు {user_dob} అని చెప్పారు, కానీ మీ {source} లో {doc_dob} అని ఉంది. దేనిని ఉపయోగించమంటారు?"
                warn_en = f"⚠️ I found a difference in your date of birth. You entered {user_dob}, but your {source} shows {doc_dob}. Which one should I use?"
                warn_ta = f"⚠️ உங்கள் பிறந்த தேதியில் வேறுபாடு உள்ளது. நீங்கள் {user_dob} என உள்ளிட்டீர்கள், ஆனால் {source} இல் {doc_dob} உள்ளது. எதைப் பயன்படுத்த வேண்டும்?"

                chosen_warn = warn_hi if language == "hi" else (warn_te if language == "te" else (warn_ta if language == "ta" else warn_en))

                conflicts.append({
                    "field_id": "dob",
                    "field_name": "dob",
                    "label_en": "Date of Birth",
                    "label_hi": "जन्म तिथि",
                    "label_te": "పుట్టిన తేదీ",
                    "user_value": str(user_dob),
                    "document_value": str(doc_dob),
                    "document_source": source,
                    "resolution_status": "pending",
                    "selected_value": None,
                    "warning_message_en": warn_en,
                    "warning_message_te": warn_te,
                    "warning_message_hi": warn_hi,
                    "warning_message": chosen_warn
                })

        # 2. Full Name Check
        user_name = form_data.get("full_name") or form_data.get("applicant_name")
        doc_name = doc_extracted.get("name") or doc_extracted.get("full_name")
        if user_name and doc_name:
            u_clean = "".join(str(user_name).lower().split())
            d_clean = "".join(str(doc_name).lower().split())
            if u_clean != d_clean and u_clean not in d_clean and d_clean not in u_clean:
                source = doc_sources.get("name", "Document")
                field_id = "full_name" if "full_name" in form_data else "applicant_name"
                
                warn_hi = f"⚠️ नाम में अंतर: आपने '{user_name}' दर्ज किया है, लेकिन आपके {source} में '{doc_name}' दर्ज है। कृपया सही नाम चुनें।"
                warn_te = f"⚠️ పేరులో వ్యత్యాసం ఉంది: మీరు '{user_name}' అని చెప్పారు, కానీ మీ {source} లో '{doc_name}' అని ఉంది."
                warn_en = f"⚠️ Name mismatch: You entered '{user_name}', but your {source} shows '{doc_name}'."
                chosen_warn = warn_hi if language == "hi" else (warn_te if language == "te" else warn_en)

                conflicts.append({
                    "field_id": field_id,
                    "field_name": "full_name",
                    "label_en": "Full Name",
                    "label_hi": "पूरा नाम",
                    "label_te": "పూర్తి పేరు",
                    "user_value": str(user_name),
                    "document_value": str(doc_name),
                    "document_source": source,
                    "resolution_status": "pending",
                    "selected_value": None,
                    "warning_message_en": warn_en,
                    "warning_message_te": warn_te,
                    "warning_message_hi": warn_hi,
                    "warning_message": chosen_warn
                })

        return conflicts

validation_agent = ValidationAgent()
