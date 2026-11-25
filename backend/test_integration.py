"""
End-to-end integration test for FormSaathi backend.
Tests chat, intent detection, physical form upload, OCR, conflict detection, overlay image, and PDF generation.
"""
import os
import sys

# Add backend to sys.path
sys.path.append(r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\backend")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_all():
    print("--- 1. Testing Health Endpoint ---")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("Health check OK:", res.json())

    print("\n--- 2. Testing Services List ---")
    res = client.get("/api/services")
    assert res.status_code == 200
    services = res.json()
    print(f"Retrieved {len(services)} services: {[s['service_id'] for s in services]}")

    print("\n--- 3. Testing Mode 1: Digital Scholarship Chat & Intent ---")
    chat_res = client.post("/api/chat", json={
        "user_input": "Naaku scholarship apply cheyyali. Nenu B.Tech student ni.",
        "language": "te"
    })
    assert chat_res.status_code == 200
    data = chat_res.json()
    session_id = data["session_id"]
    print("Intent Detected:", data.get("intent"))
    print("Assistant Reply:\n", data.get("reply_text"))

    print("\n--- 4. Testing Answering Next Question ---")
    ans_res = client.post("/api/chat", json={
        "session_id": session_id,
        "user_input": "Sai Praneetha",
        "language": "te"
    })
    assert ans_res.status_code == 200
    print("After Name:", ans_res.json().get("reply_text"))

    # User answers DOB as 15/06/2006 (intentional mismatch with Aadhaar 15/06/2005)
    dob_res = client.post("/api/chat", json={
        "session_id": session_id,
        "user_input": "15/06/2006",
        "language": "te"
    })
    assert dob_res.status_code == 200
    print("After DOB:", dob_res.json().get("reply_text"))

    print("\n--- 5. Testing Supporting Document Upload & Conflict Detection ---")
    sample_aadhaar_path = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\data\sample_forms\sample_aadhaar.jpg"
    with open(sample_aadhaar_path, "rb") as f:
        doc_res = client.post("/api/documents/upload-doc", data={
            "session_id": session_id,
            "language": "te",
            "doc_hint": "aadhaar"
        }, files={"file": ("sample_aadhaar.jpg", f, "image/jpeg")})

    assert doc_res.status_code == 200
    doc_data = doc_res.json()
    conflicts = doc_data.get("conflicts", [])
    print(f"Conflicts detected: {len(conflicts)}")
    for c in conflicts:
        print(f"  Field: {c['field_name']} | User: {c['user_value']} | Doc: {c['document_value']}")
        print(f"  Warning: {c['warning_message_te']}")

    assert len(conflicts) > 0, "Expected DOB conflict to be detected!"

    print("\n--- 6. Testing Conflict Resolution ---")
    resolve_res = client.post("/api/validation/resolve-conflict", json={
        "session_id": session_id,
        "field_id": "dob",
        "selected_value": "15/06/2005",
        "source_choice": "document"
    })
    assert resolve_res.status_code == 200
    print("Conflict Resolved Successfully! Value confirmed:", resolve_res.json().get("final_value"))

    print("\n--- 7. Testing Digital PDF Generation ---")
    pdf_res = client.post("/api/forms/generate-digital-pdf", data={"session_id": session_id})
    assert pdf_res.status_code == 200
    print("Digital Application PDF generated:", pdf_res.json().get("pdf_url"))

    print("\n--- 8. Testing Mode 2: Physical Paper Form Upload ---")
    bank_form_path = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\data\sample_forms\bank_application_form.jpg"
    with open(bank_form_path, "rb") as f:
        form_res = client.post("/api/forms/upload-physical", data={
            "session_id": session_id,
            "language": "te"
        }, files={"file": ("bank_application_form.jpg", f, "image/jpeg")})

    assert form_res.status_code == 200
    form_data = form_res.json()
    analysis = form_data.get("analysis", {})
    print("Form Title:", analysis.get("form_title"))
    print(f"Fields detected count: {len(analysis.get('fields', []))}")

    print("\n--- 9. Testing Physical Form Overlay & Print-Ready PDF ---")
    fill_res = client.post("/api/forms/fill-physical", data={"session_id": session_id})
    assert fill_res.status_code == 200
    fill_data = fill_res.json()
    print("Filled Form Image URL:", fill_data.get("filled_image_url"))
    print("Print-Ready PDF URL:", fill_data.get("pdf_url"))

    print("\n--- 10. Testing Application History ---")
    hist_res = client.get("/api/applications/history")
    assert hist_res.status_code == 200
    apps = hist_res.json()
    print(f"Total Applications in History: {len(apps)}")

    print("\n==========================================")
    print("🎉 ALL 10 INTEGRATION TESTS PASSED 100%! 🎉")
    print("==========================================")

if __name__ == "__main__":
    test_all()
