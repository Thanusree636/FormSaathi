"""
FormSaathi Document Requirement & Missing Document Agent.
Analyzes uploaded documents against required service/form checklist.
"""
from typing import Dict, Any, List
from app.rag.knowledge_base import SERVICES_DB

class DocumentAgent:
    def check_documents(
        self,
        service_id: str,
        uploaded_docs: List[Dict[str, Any]],
        language: str = "te",
        custom_required_docs: List[str] = None
    ) -> Dict[str, Any]:
        req_list = []
        if custom_required_docs is not None:
            # Map strings to standard structure
            for doc_name in custom_required_docs:
                doc_type = doc_name.lower().replace(" ", "_")
                req_list.append({
                    "doc_type": doc_type,
                    "name_en": doc_name,
                    "name_te": doc_name,
                    "required": True
                })
        elif service_id in SERVICES_DB:
            req_list = SERVICES_DB[service_id].get("required_documents", [])

        uploaded_types = {d.get("doc_type"): d for d in uploaded_docs}

        verified_docs = []
        missing_docs = []

        for req in req_list:
            doc_type = req["doc_type"]
            name = req["name_te"] if language == "te" else req["name_en"]
            if doc_type in uploaded_types:
                verified_docs.append({
                    "doc_type": doc_type,
                    "name": name,
                    "status": "verified",
                    "details": uploaded_types[doc_type]
                })
            else:
                if req.get("required", True):
                    missing_docs.append({
                        "doc_type": doc_type,
                        "name": name,
                        "status": "missing"
                    })

        if missing_docs:
            missing_names = ", ".join([d["name"] for d in missing_docs])
            if language == "te":
                summary_msg = f"మీరు కొన్ని పత్రాలు అప్‌లోడ్ చేశారు. అయితే ఇంకా **{missing_names}** అప్‌లోడ్ చేయాల్సి ఉంది."
            else:
                summary_msg = f"Your documents were received, but **{missing_names}** is still required."
        else:
            if language == "te":
                summary_msg = "అవసరమైన అన్ని పత్రాలు విజయవంతంగా పరిశీలించబడ్డాయి!"
            else:
                summary_msg = "All required documents have been verified successfully!"

        return {
            "verified_docs": verified_docs,
            "missing_docs": missing_docs,
            "all_complete": len(missing_docs) == 0,
            "summary_message": summary_msg
        }

document_agent = DocumentAgent()
