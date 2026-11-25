"""
FormSaathi FastAPI Route Handlers.
Implements endpoints for:
- Intent Detection & Voice/Text Conversational Q&A
- Document Upload & OCR
- Physical Form Analysis & Field Detection
- Conflict Detection & Resolution
- Filled Form Image & Print-Ready PDF Generation
"""
import os
import shutil
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse

from app.schemas.schemas import (
    ChatMessage, IntentRequest, IntentResponse,
    ApplicationSession, ConflictResolutionRequest
)
from app.models.database import db
from app.rag.knowledge_base import SERVICES_DB, rag_retriever
from app.agents.intent_agent import intent_agent
from app.agents.question_agent import question_agent
from app.agents.document_agent import document_agent
from app.agents.validation_agent import validation_agent
from app.ocr.ocr_engine import ocr_engine
from app.form_processing.form_analyzer import form_analyzer
from app.form_processing.form_overlay import form_overlay_engine
from app.pdf.pdf_generator import pdf_generator

router = APIRouter(prefix="/api")

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "uploads")
GENERATED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "generated")
SAMPLE_FORMS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "data", "sample_forms")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(SAMPLE_FORMS_DIR, exist_ok=True)

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FormSaathi Backend",
        "demo_mode": True,
        "ocr_engine": "active"
    }

@router.get("/services")
def list_services():
    """Returns available RAG services (Scholarship, Income Certificate, Bank Account)."""
    return list(SERVICES_DB.values())

@router.post("/session/create")
def create_session(mode: str = "digital", language: str = "hi", service_id: Optional[str] = None):
    session = db.create_session(mode=mode, language=language, service_id=service_id)
    return session

@router.get("/session/{session_id}")
def get_session(session_id: str):
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/chat")
def handle_chat(req: IntentRequest):
    """
    Core conversational agent endpoint.
    Handles user speech/text input, detects intent if new, or processes answer for active question.
    """
    session = None
    if req.session_id:
        session = db.get_session(req.session_id)

    if not session:
        session = db.create_session(mode="digital", language=req.language or "te")

    session_id = session["session_id"]
    lang = req.language or session.get("language", "te")
    user_text = req.user_input.strip()

    # Record user message
    db.add_chat_message(session_id, "user", user_text, lang)

    # 1. If session has no service assigned yet, run Intent Agent
    if not session.get("service_id"):
        intent_res = intent_agent.process_utterance(user_text, lang)
        service_id = intent_res.get("service_id")
        
        updates = {
            "language": lang,
            "service_id": service_id,
            "service_name": intent_res.get("service_name")
        }
        
        # Merge any extracted entities
        if intent_res.get("extracted_entities"):
            session["form_data"].update(intent_res["extracted_entities"])
            updates["form_data"] = session["form_data"]

        db.update_session(session_id, updates)

        bot_reply = intent_res["reply_text"]
        if intent_res.get("next_question"):
            bot_reply += f"\n\n👉 **{intent_res['next_question']}**"

        db.add_chat_message(session_id, "assistant", bot_reply, lang)

        return {
            "session_id": session_id,
            "intent": intent_res["intent"],
            "reply_text": bot_reply,
            "audio_prompt": intent_res.get("reply_audio_prompt"),
            "service_id": service_id,
            "next_field": intent_res.get("field_to_fill"),
            "session": db.get_session(session_id)
        }

    # 2. If service is active, determine which field was answered and ask next
    service_id = session["service_id"]
    form_data = session.get("form_data", {})
    custom_fields = session.get("detected_fields")

    # Find currently pending field
    curr_q = question_agent.get_next_question(
        service_id=service_id,
        current_form_data=form_data,
        language=lang,
        custom_fields=custom_fields
    )

    if curr_q:
        # Save user's answer into form_data
        field_id = curr_q["field_id"]
        form_data[field_id] = user_text
        session["form_data"] = form_data
        db.update_session(session_id, {"form_data": form_data})

    # Check for next question
    next_q = question_agent.get_next_question(
        service_id=service_id,
        current_form_data=form_data,
        language=lang,
        custom_fields=custom_fields
    )

    if next_q:
        q_text = next_q["question"]
        thanks_prefix = {
            "hi": "धन्यवाद। ",
            "te": "ధన్యవాదాలు. ",
            "ta": "நன்றி. ",
            "kn": "ಧನ್ಯವಾದಗಳು. ",
            "ml": "നന്ദി. ",
            "mr": "धन्यवाद. ",
            "bn": "ধন্যবাদ। ",
            "gu": "આભાર. ",
            "pa": "ਧੰਨਵਾਦ। ",
            "or": "ଧନ୍ୟବାଦ। ",
            "en": "Thank you. "
        }.get(lang, "Thank you. ")
        bot_reply = f"{thanks_prefix}{q_text}"
        audio_prompt = q_text
        db.add_chat_message(session_id, "assistant", bot_reply, lang)
        return {
            "session_id": session_id,
            "reply_text": bot_reply,
            "audio_prompt": audio_prompt,
            "next_field": next_q["field_id"],
            "all_answered": False,
            "session": db.get_session(session_id)
        }
    else:
        # All conversational questions completed!
        completion_msgs = {
            "hi": "सभी आवश्यक विवरण दर्ज कर लिए गए हैं! अब कृपया सत्यापन हेतु दस्तावेज़ (आधार आदि) अपलोड करें या पूर्वावलोकन देखें।",
            "te": "అవసరమైన అన్ని వివరాలు నమోదు చేయబడ్డాయి! ఇప్పుడు దయచేసి ధ్రువీకరణ పత్రాలను (ఆధార్, మొదలైనవి) అప్‌లోడ్ చేయండి లేదా ప్రివ్యూ చూడండి.",
            "ta": "தேவையான அனைத்து விவரங்களும் பெறப்பட்டன! தயவுசெய்து சரிபார்ப்பு ஆவணங்களை பதிவேற்றவும்.",
            "kn": "ಎಲ್ಲಾ ಅಗತ್ಯ ವಿವರಗಳನ್ನು ಸಂಗ್ರಹಿಸಲಾಗಿದೆ! ದಯವಿಟ್ಟು ಪರಿಶೀಲನಾ ದಾಖಲೆಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
            "mr": "सर्व आवश्यक माहिती नोंदवली गेली आहे! कृपया पडताळणीसाठी कागदपत्रे अपलोड करा.",
            "bn": "সমস্ত প্রয়োজনীয় তথ্য সংগ্রহ করা হয়েছে! অনুগ্রহ করে যাচাইকরণের জন্য নথি আপलोड করুন।",
            "en": "All required details have been collected! Please upload supporting documents to verify or review your preview."
        }
        bot_reply = completion_msgs.get(lang, completion_msgs["hi"])
        audio_prompt = bot_reply

        db.add_chat_message(session_id, "assistant", bot_reply, lang)
        db.update_session(session_id, {"status": "ready_for_preview"})
        return {
            "session_id": session_id,
            "reply_text": bot_reply,
            "audio_prompt": audio_prompt,
            "next_field": None,
            "all_answered": True,
            "session": db.get_session(session_id)
        }

@router.post("/forms/upload-physical")
async def upload_physical_form(
    session_id: str = Form(...),
    language: str = Form("te"),
    file: UploadFile = File(...)
):
    """
    Mode 2: Uploads a physical paper form (bank account form / scholarship form).
    Runs OCR and Form Analyzer to detect form title, instructions, fields, and required documents.
    """
    session = db.get_session(session_id)
    if not session:
        session = db.create_session(mode="physical", language=language)
        session_id = session["session_id"]

    # Save uploaded file
    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"form_{session_id}_{uuid.uuid4().hex[:6]}{file_ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Analyze Form
    analysis = form_analyzer.analyze_form(saved_path, file.filename)
    
    # Update Session
    db.update_session(session_id, {
        "mode": "physical",
        "form_id": analysis["form_id"],
        "service_name": analysis["form_title"],
        "service_id": "bank_account" if "bank" in analysis["form_id"] else "student_scholarship",
        "original_form_path": saved_path,
        "original_form_url": f"/api/uploads/{saved_filename}",
        "detected_fields": analysis["fields"],
        "required_documents_list": analysis["required_documents"],
        "instructions_en": analysis["instructions_en"],
        "instructions_te": analysis["instructions_te"]
    })

    explanations = {
        "hi": f"नमस्ते! आपके द्वारा अपलोड किए गए **{analysis['form_title']}** फ़ॉर्म को पहचान लिया गया है। इसमें {len(analysis['fields'])} फ़ील्ड्स हैं। मैं आपसे कुछ सरल प्रश्न पूछूँगा।",
        "en": f"Form successfully recognized as **{analysis['form_title']}** with {len(analysis['fields'])} fields detected. I will guide you through answering them.",
        "te": f"నమస్కారం! మీరు అప్‌లోడ్ చేసిన **{analysis['form_title']}** ఫారమ్‌ను విజయవంతంగా గుర్తించాను. ఇందులో {len(analysis['fields'])} ఫీల్డులు ఉన్నాయి. నేను మిమ్మల్ని కొన్ని సులభమైన ప్రశ్నలు అడుగుతాను.",
        "ta": f"வணக்கம்! நீங்கள் பதிவேற்றிய **{analysis['form_title']}** படிவம் வெற்றிகரமாக அடையாளம் காணப்பட்டது.",
        "kn": f"ನಮಸ್ಕಾರ! ನಿಮ್ಮ **{analysis['form_title']}** ಫಾರ್ಮ್ ಅನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಗುರುತಿಸಲಾಗಿದೆ.",
        "mr": f"नमस्कार! आपण अपलोड केलेला **{analysis['form_title']}** फॉर्म ओळखला गेला आहे.",
        "bn": f"নমস্কার! আপনার আপলোড করা **{analysis['form_title']}** ফর্মটি সফলভাবে সনাক্ত করা হয়েছে।"
    }
    explanation_text = explanations.get(language, explanations["hi"])

    db.add_chat_message(session_id, "assistant", explanation_text, language)

    return {
        "session_id": session_id,
        "analysis": analysis,
        "explanation": explanation_text,
        "session": db.get_session(session_id)
    }

@router.post("/documents/upload-doc")
async def upload_supporting_document(
    session_id: str = Form(...),
    doc_hint: Optional[str] = Form(None),
    language: str = Form("hi"),
    file: UploadFile = File(...)
):
    """
    Uploads supporting documents (Aadhaar, Income cert, College ID, etc.),
    performs OCR extraction, maps data to form fields, evaluates missing documents,
    and checks for conflicts (e.g. DOB mismatch).
    """
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    file_ext = os.path.splitext(file.filename)[1]
    saved_filename = f"doc_{session_id}_{uuid.uuid4().hex[:6]}{file_ext}"
    saved_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process Document with OCR
    ocr_result = ocr_engine.process_document(saved_path, file.filename, doc_hint=doc_hint)
    ocr_result["file_url"] = f"/api/uploads/{saved_filename}"

    uploaded_docs = session.get("uploaded_documents", [])
    uploaded_docs.append(ocr_result)

    # Intelligent Auto-fill mapping
    form_data = session.get("form_data", {})
    ext_data = ocr_result.get("extracted_data", {})

    # Auto-map extracted fields if not already manually entered
    if "dob" in ext_data and "dob" not in form_data:
        form_data["dob"] = ext_data["dob"]
    if "name" in ext_data and "full_name" not in form_data and "applicant_name" not in form_data:
        form_data["full_name"] = ext_data["name"]
    if "aadhaar_number" in ext_data and "aadhaar_number" not in form_data:
        form_data["aadhaar_number"] = ext_data["aadhaar_number"]
    if "annual_income" in ext_data and "annual_income" not in form_data:
        form_data["annual_income"] = ext_data["annual_income"]
    if "college_name" in ext_data and "college_name" not in form_data:
        form_data["college_name"] = ext_data["college_name"]
    if "course" in ext_data and "course" not in form_data:
        form_data["course"] = ext_data["course"]

    # Check missing documents
    service_id = session.get("service_id", "student_scholarship")
    custom_reqs = session.get("required_documents_list")
    doc_status = document_agent.check_documents(
        service_id=service_id,
        uploaded_docs=uploaded_docs,
        language=language,
        custom_required_docs=custom_reqs
    )

    # Detect Conflicts (e.g. user entered DOB vs Document OCR DOB)
    conflicts = validation_agent.detect_conflicts(
        form_data=form_data,
        uploaded_docs=uploaded_docs,
        language=language
    )

    db.update_session(session_id, {
        "uploaded_documents": uploaded_docs,
        "form_data": form_data,
        "missing_documents": [d["name"] for d in doc_status["missing_docs"]],
        "conflicts": conflicts
    })

    return {
        "session_id": session_id,
        "ocr_result": ocr_result,
        "document_status": doc_status,
        "conflicts": conflicts,
        "session": db.get_session(session_id)
    }

@router.post("/validation/resolve-conflict")
def resolve_conflict(req: ConflictResolutionRequest):
    """
    User resolves a detected discrepancy by choosing user-provided value,
    document-extracted value, or custom edit.
    """
    session = db.get_session(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    form_data = session.get("form_data", {})
    form_data[req.field_id] = req.selected_value

    conflicts = session.get("conflicts", [])
    updated_conflicts = []
    for c in conflicts:
        if c.get("field_id") == req.field_id:
            c["resolution_status"] = "resolved"
            c["selected_value"] = req.selected_value
        else:
            updated_conflicts.append(c)

    db.update_session(req.session_id, {
        "form_data": form_data,
        "conflicts": updated_conflicts
    })

    return {
        "success": True,
        "resolved_field": req.field_id,
        "final_value": req.selected_value,
        "remaining_conflicts": updated_conflicts,
        "session": db.get_session(req.session_id)
    }

@router.post("/forms/fill-physical")
def fill_physical_form(session_id: str = Form(...)):
    """
    Fills the original physical form with collected and validated answers.
    Generates:
    1. Filled form image overlay (preserving exact layout).
    2. Print-ready PDF.
    """
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    base_form_path = session.get("original_form_path")
    # If no original form uploaded, use sample bank form image
    if not base_form_path or not os.path.exists(base_form_path):
        base_form_path = os.path.join(SAMPLE_FORMS_DIR, "bank_application_form.jpg")

    fields = session.get("detected_fields", [])
    if not fields:
        analysis = form_analyzer.analyze_form(base_form_path, "bank_application_form.jpg")
        fields = analysis["fields"]

    form_data = session.get("form_data", {})

    output_img_name = f"filled_form_{session_id}.jpg"
    output_pdf_name = f"filled_form_{session_id}.pdf"
    output_img_path = os.path.join(GENERATED_DIR, output_img_name)
    output_pdf_path = os.path.join(GENERATED_DIR, output_pdf_name)

    # 1. Generate Overlay Image
    form_overlay_engine.overlay_form(
        base_image_path=base_form_path,
        output_image_path=output_img_path,
        fields_schema=fields,
        form_data=form_data
    )

    # 2. Convert to print-ready PDF
    pdf_generator.generate_pdf_from_image(
        image_path=output_img_path,
        output_pdf_path=output_pdf_path
    )

    # Save to history
    app_id = db.save_application({
        "mode": "physical",
        "service_name": session.get("service_name", "Bank Account Opening Form"),
        "applicant_name": form_data.get("full_name", "Applicant"),
        "session_id": session_id,
        "filled_image_url": f"/api/generated/{output_img_name}",
        "pdf_url": f"/api/generated/{output_pdf_name}",
        "form_data": form_data
    })

    db.update_session(session_id, {
        "status": "completed",
        "filled_form_image_path": output_img_path,
        "filled_form_image_url": f"/api/generated/{output_img_name}",
        "generated_pdf_path": output_pdf_path,
        "generated_pdf_url": f"/api/generated/{output_pdf_name}",
        "application_id": app_id
    })

    return {
        "success": True,
        "application_id": app_id,
        "filled_image_url": f"/api/generated/{output_img_name}",
        "pdf_url": f"/api/generated/{output_pdf_name}",
        "session": db.get_session(session_id)
    }

@router.post("/forms/generate-digital-pdf")
def generate_digital_pdf(session_id: str = Form(...)):
    """
    Generates an official digital application summary PDF for scholarships/certificates.
    """
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    output_pdf_name = f"application_{session_id}.pdf"
    output_pdf_path = os.path.join(GENERATED_DIR, output_pdf_name)

    service_title = session.get("service_name", "Citizen Welfare Application")
    app_id = "APP-" + session_id.upper()
    form_data = session.get("form_data", {})
    verified_docs = session.get("uploaded_documents", [])
    conflicts = session.get("conflicts", [])

    pdf_generator.generate_digital_application_pdf(
        output_pdf_path=output_pdf_path,
        service_title=service_title,
        application_id=app_id,
        applicant_data=form_data,
        verified_docs=verified_docs,
        conflicts_resolved=conflicts
    )

    db.save_application({
        "mode": "digital",
        "service_name": service_title,
        "applicant_name": form_data.get("full_name") or form_data.get("applicant_name", "Applicant"),
        "session_id": session_id,
        "pdf_url": f"/api/generated/{output_pdf_name}",
        "form_data": form_data
    })

    db.update_session(session_id, {
        "status": "completed",
        "generated_pdf_url": f"/api/generated/{output_pdf_name}",
        "application_id": app_id
    })

    return {
        "success": True,
        "application_id": app_id,
        "pdf_url": f"/api/generated/{output_pdf_name}",
        "session": db.get_session(session_id)
    }

@router.get("/applications/history")
def get_applications():
    return db.list_applications()

@router.get("/uploads/{filename}")
def serve_upload(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="File not found")

@router.get("/generated/{filename}")
def serve_generated(filename: str):
    path = os.path.join(GENERATED_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="File not found")

@router.get("/sample-forms/{filename}")
def serve_sample(filename: str):
    path = os.path.join(SAMPLE_FORMS_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Sample form not found")
