"""
Direct unit and workflow test for FormSaathi backend components.
"""
import sys
import os

sys.path.append(r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\backend")

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
from app.schemas.schemas import IntentRequest, ConflictResolutionRequest

def run_tests():
    print("1. Testing RAG Knowledge Base...")
    assert "student_scholarship" in SERVICES_DB
    res = rag_retriever.retrieve("Naaku scholarship apply cheyyali. Nenu B.Tech student ni.")
    assert res is not None
    assert res["service_id"] == "student_scholarship"
    print("✓ RAG Retriever successfully identified:", res["title_en"])

    print("\n2. Testing Intent Agent...")
    intent_res = intent_agent.process_utterance("Naaku scholarship apply cheyyali. Nenu B.Tech student ni.", "te")
    assert intent_res["intent"] == "student_scholarship"
    assert "B.Tech" in intent_res["extracted_entities"].get("course", "")
    print("✓ Intent Agent detected course:", intent_res["extracted_entities"])

    print("\n3. Testing Database & Session Management...")
    session = db.create_session("digital", "te", "student_scholarship")
    s_id = session["session_id"]
    assert db.get_session(s_id) is not None
    print("✓ Session created with ID:", s_id)

    print("\n4. Testing Question Agent...")
    q1 = question_agent.get_next_question("student_scholarship", {}, "te")
    assert q1 is not None
    print("✓ First conversational question:", q1["question"])

    print("\n5. Testing Document OCR Engine...")
    aadhaar_path = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\data\sample_forms\sample_aadhaar.jpg"
    ocr_res = ocr_engine.process_document(aadhaar_path, "sample_aadhaar.jpg", "aadhaar")
    assert ocr_res["doc_type"] == "aadhaar"
    assert "dob" in ocr_res["extracted_data"]
    print("✓ Aadhaar OCR Extracted:", ocr_res["extracted_data"])

    print("\n6. Testing Conflict Detection Agent (User DOB 15/06/2006 vs Aadhaar 15/06/2005)...")
    user_form = {"full_name": "Sai Praneetha", "dob": "15/06/2006"}
    conflicts = validation_agent.detect_conflicts(user_form, [ocr_res], "te")
    assert len(conflicts) > 0
    dob_conflict = conflicts[0]
    assert dob_conflict["field_id"] == "dob"
    assert dob_conflict["user_value"] == "15/06/2006"
    assert dob_conflict["document_value"] == "15/06/2005"
    print("✓ Conflict Warning Message:\n ", dob_conflict["warning_message_te"])

    print("\n7. Testing Physical Form Analyzer...")
    bank_path = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\data\sample_forms\bank_application_form.jpg"
    analysis = form_analyzer.analyze_form(bank_path, "bank_application_form.jpg")
    assert len(analysis["fields"]) > 10
    print(f"✓ Form Analyzer detected {len(analysis['fields'])} fields in: {analysis['form_title']}")

    print("\n8. Testing Physical Form Image Overlay Engine...")
    out_img = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\backend\generated\test_overlay.jpg"
    filled_path = form_overlay_engine.overlay_form(
        base_image_path=bank_path,
        output_image_path=out_img,
        fields_schema=analysis["fields"],
        form_data={
            "full_name": "Sai Praneetha K",
            "dob": "15/06/2005",
            "gender": "Female",
            "mobile": "9876543210",
            "aadhaar_number": "XXXX XXXX 8921",
            "address": "Plot 42, Gayatri Nagar, Vijayawada",
            "occupation": "Student",
            "annual_income": "1,80,000",
            "has_nominee": "Yes",
            "nominee_name": "K. Venkateshwarlu (Father)",
            "atm_card_required": "Yes"
        }
    )
    assert os.path.exists(filled_path)
    print("✓ Filled Form Image successfully created:", filled_path)

    print("\n9. Testing Print-Ready PDF Generation...")
    out_pdf = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\backend\generated\test_filled.pdf"
    pdf_path = pdf_generator.generate_pdf_from_image(filled_path, out_pdf)
    assert os.path.exists(pdf_path)
    print("✓ Print-Ready PDF generated:", pdf_path)

    print("\n10. Testing Digital Application Summary PDF Generation...")
    out_dig_pdf = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\backend\generated\test_digital_app.pdf"
    dig_pdf_path = pdf_generator.generate_digital_application_pdf(
        output_pdf_path=out_dig_pdf,
        service_title="Post-Matric Student Scholarship (Jagananna Vidya Deevena)",
        application_id="APP-TEST99",
        applicant_data={
            "full_name": "Sai Praneetha",
            "dob": "15/06/2005",
            "course": "B.Tech Computer Science",
            "college_name": "JNTU College of Engineering",
            "roll_number": "22B91A0589",
            "annual_income": "₹1,80,000"
        },
        verified_docs=[ocr_res],
        conflicts_resolved=[]
    )
    assert os.path.exists(dig_pdf_path)
    print("✓ Digital Application Summary PDF generated:", dig_pdf_path)

    print("\n=======================================================")
    print("🎉 ALL 10 COMPONENT & WORKFLOW TESTS PASSED 100%! 🎉")
    print("=======================================================")

if __name__ == "__main__":
    run_tests()
