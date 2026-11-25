"""
FormSaathi Pydantic Schemas
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str # "user", "assistant", "system"
    content: str
    language: Optional[str] = "hi" # "hi", "en", "te", "ta", "kn", "ml", "mr", "bn", "gu", "pa", "or"
    timestamp: Optional[str] = None
    audio_transcript: Optional[bool] = False

class IntentRequest(BaseModel):
    user_input: str
    language: Optional[str] = "hi"
    session_id: Optional[str] = None

class IntentResponse(BaseModel):
    intent: str # "scholarship", "income_certificate", "bank_account", "farmer_scheme", "physical_form", "general"
    confidence: float
    detected_language: str
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    extracted_entities: Dict[str, Any] = {}
    reply_text: str
    reply_audio_prompt: Optional[str] = None
    next_question: Optional[str] = None
    field_to_fill: Optional[str] = None

class FormFieldSchema(BaseModel):
    id: str
    name: str
    label_en: str
    label_te: str
    field_type: str # text, date, number, select, textarea, checkbox, signature
    required: bool = True
    section: Optional[str] = "General"
    value: Optional[Any] = None
    confidence: Optional[float] = 1.0
    source: Optional[str] = "manual" # "user_input", "document_ocr", "manual"
    options: Optional[List[str]] = None
    coordinates: Optional[Dict[str, int]] = None # {"x": int, "y": int, "width": int, "height": int, "page": 1}
    manual_notice: Optional[str] = None # e.g. "✍ Signature required - complete manually"

class FormAnalysisResult(BaseModel):
    form_id: str
    form_title: str
    form_type: str
    description_en: str
    description_te: str
    fields: List[FormFieldSchema]
    required_documents: List[str]
    instructions_en: List[str]
    instructions_te: List[str]
    image_url: Optional[str] = None

class DocumentAnalysisResult(BaseModel):
    doc_id: str
    doc_type: str # "aadhaar", "income_cert", "college_id", "marks_memo", "pan", "bank_passbook", "other"
    doc_name: str
    extracted_data: Dict[str, Any]
    confidence: float
    raw_text: Optional[str] = None
    status: str = "verified" # "verified", "missing", "conflict"

class ConflictItem(BaseModel):
    field_id: str
    field_name: str
    label_en: str
    label_te: str
    user_value: str
    document_value: str
    document_source: str
    resolution_status: str = "pending" # "pending", "resolved"
    selected_value: Optional[str] = None
    warning_message_en: str
    warning_message_te: str

class ApplicationSession(BaseModel):
    session_id: str
    mode: str # "digital" or "physical"
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    form_id: Optional[str] = None
    language: str = "hi" # "hi", "en", "te", "ta", "kn", "ml", "mr", "bn", "gu", "pa", "or"
    current_step: int = 1
    total_steps: int = 6
    chat_history: List[ChatMessage] = []
    form_data: Dict[str, Any] = {} # Key-value of collected answers
    uploaded_documents: List[DocumentAnalysisResult] = []
    missing_documents: List[str] = []
    conflicts: List[ConflictItem] = []
    status: str = "in_progress" # "in_progress", "ready_for_preview", "confirmed", "completed"
    created_at: Optional[str] = None
    original_form_path: Optional[str] = None
    filled_form_image_path: Optional[str] = None
    generated_pdf_path: Optional[str] = None

class ConflictResolutionRequest(BaseModel):
    session_id: str
    field_id: str
    selected_value: str
    source_choice: str # "user", "document", "custom"

class VoiceSynthesisRequest(BaseModel):
    text: str
    language: str = "te"
