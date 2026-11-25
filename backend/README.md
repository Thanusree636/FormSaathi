# FormSaathi Backend

The FastAPI backend powers the multilingual, voice-first form-filling AI agent.

## Features
- **Intent Detection & Routing**: Understands citizen requests in Telugu, English, and Tanglish.
- **RAG Knowledge Base**: Accurate knowledge for scholarships, income certificates, and bank account applications.
- **Sequential Question Agent**: Asks one conversational question at a time.
- **OCR & Document Engine**: Extracts structured data from Aadhaar, PAN, College ID, Marks Memo, and Income Certificates.
- **Conflict & Validation Agent**: Detects discrepancies (e.g., entered DOB vs document OCR DOB) and provides clear resolution options.
- **Physical Form Overlay**: Fills original physical paper forms onto exact field coordinates, preserving original layout.
- **Print-Ready PDF Generation**: Outputs high-resolution PDFs ready for physical bank or college submission.

## Setup & Running

```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`
