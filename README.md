# FormSaathi (फ़ॉर्म साथी / FormSaathi) 🚀
### Multilingual Voice-First Citizen AI Agent for All Indians

> **"Tell us what you need. Show us the form. FormSaathi helps you complete the rest."**

---

## 🌟 1. Project Overview & Vision

**FormSaathi** is an inclusive, multilingual, voice-first AI agent designed for all citizens across India.

Instead of navigating complicated portals, reading fine print in unfamiliar languages, or struggling to fill physical government and bank forms, citizens can simply **speak in their mother tongue** or **show a photo of the form** they received.

### Supported Indian Languages (11 Major Languages):
1. 🇮🇳 **हिंदी (Hindi)**
2. 🇮🇳 **English**
3. 🇮🇳 **తెలుగు (Telugu)**
4. 🇮🇳 **தமிழ் (Tamil)**
5. 🇮🇳 **ಕನ್ನಡ (Kannada)**
6. 🇮🇳 **മലയാളം (Malayalam)**
7. 🇮🇳 **मराठी (Marathi)**
8. 🇮🇳 **বাংলা (Bengali)**
9. 🇮🇳 **ગુજરાતી (Gujarati)**
10. 🇮🇳 **ਪੰਜਾਬੀ (Punjabi)**
11. 🇮🇳 **ଓଡ଼ିଆ (Odia)**

### Designed Specially For:
- 👴 **Elderly Citizens**: Who struggle with typing, small screen fonts, English, and complex online portals.
- 🌾 **Rural Citizens**: Who prefer speaking in their mother tongue (Telugu / Hindi / etc.) rather than filling English forms.
- 👩‍🎓 **Students**: Applying for college scholarships (e.g., Post-Matric Jagananna Vidya Deevena), fee reimbursement, or exam applications.
- 👨‍🌾 **Farmers**: Applying for PM-KISAN, Rythu Bharosa, or revenue certificates.
- 👷 **Workers & Families**: Helping parents and elders fill paper bank forms without standing in queues for hours.

---

## ⚡ 2. The Two Breakthrough Modes

### 🌐 MODE 1 — DIGITAL APPLICATION ASSISTANT
Citizens do not need to know exact department names or portal links.
```text
User Speaks ("Naaku scholarship apply cheyyali. Nenu B.Tech student ni.")
       ↓
Intent Detection & Entity Extraction (B.Tech, Student)
       ↓
RAG Knowledge Base & Service Matching (Post-Matric Scholarship)
       ↓
Sequential Bilingual Voice Questions (Asks 1 question at a time)
       ↓
Supporting Document Upload (Aadhaar, Income Certificate, College ID)
       ↓
OCR Extraction & Intelligent Data Mapping
       ↓
Conflict & Validation Check (e.g., DOB mismatch detection)
       ↓
Digital Application Preview & User Confirmation
       ↓
Official Print-Ready PDF Generation
```

### 📄 MODE 2 — PHYSICAL PAPER FORM ASSISTANT (Key Differentiator)
An elderly person visits a bank or tahsildar office and is handed a paper form. Instead of begging strangers to fill it, they photograph it and open FormSaathi.
```text
Upload Paper Form Scan / Photo
       ↓
Document Analysis & Field Detection (Bounding box coordinates, Labels)
       ↓
AI Explains Form & Required Documents in Telugu / English
       ↓
Sequential Voice Q&A (Answers collected by voice or text)
       ↓
Upload Supporting KYC Documents (Aadhaar, PAN)
       ↓
OCR Extraction & Auto-fill
       ↓
Validation & Conflict Resolution
       ↓
Original Form Overlay Renderer (100% Original Layout Preserved)
       ↓
Signature Area Notice ("✍ Please sign manually after printing")
       ↓
Print-Ready PDF Generation
       ↓
Download / Print and Submit at Bank!
```

---

## 🏛️ 3. Architecture & Modular Agent System

FormSaathi avoids one giant brittle prompt by orchestrating specialized agent modules:

```text
[ Citizen Voice / Upload ]
             │
             ▼
     ┌───────────────┐
     │  Web Speech   │ (STT / TTS in Telugu & English)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │  Intent Agent │ (Routes to Scholarship, Income Cert, or Bank Form)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │  RAG Retriever│ (Structured Service Rules, Eligibility, FAQs)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │Question Agent │ (Sequential conversational queue; conditional logic)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │Document Agent │ (Checks required vs missing documents)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │Validation/OCR │ (Cross-references entered vs OCR extracted values)
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │ Overlay & PDF │ (Pillow canvas overlay + ReportLab Print-Ready PDF)
     └───────────────┘
```

---

## 📂 4. Project Structure

```text
FormSaathi/
│
├── frontend/                     # React + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx        # Navigation, Audio toggle, Language switcher
│   │   │   ├── VoiceControl.jsx  # Large accessible mic, live waveforms, quick chips
│   │   │   ├── ConflictBanner.jsx# Discrepancy detector with 3-way resolution
│   │   │   ├── DocumentChecklist.jsx # Verified vs missing documents
│   │   │   └── FormOverlayViewer.jsx # Original form preview with filled text overlay
│   │   ├── pages/
│   │   │   ├── Home.jsx          # Hero, Target users, Quick Demo triggers
│   │   │   ├── DigitalAssistant.jsx    # Mode 1: Digital workflow
│   │   │   ├── PhysicalFormAssistant.jsx# Mode 2: Paper form workflow
│   │   │   └── ApplicationHistory.jsx  # Records of completed applications
│   │   ├── services/
│   │   │   └── api.js            # Frontend API client
│   │   ├── hooks/
│   │   │   └── useSpeech.js      # Web Speech API STT and TTS hook
│   │   └── utils/
│   │       └── translations.js   # Telugu & English localization
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── backend/                      # FastAPI Python Application
│   ├── app/
│   │   ├── main.py               # FastAPI entry point, CORS, static mounts
│   │   ├── api/
│   │   │   └── routes.py         # REST endpoints for chat, upload, OCR, PDF
│   │   ├── agents/
│   │   │   ├── intent_agent.py   # Intent & Entity detector
│   │   │   ├── question_agent.py # Dynamic sequential question queue
│   │   │   ├── document_agent.py # Missing document analyzer
│   │   │   └── validation_agent.py # Discrepancy & Conflict detection
│   │   ├── rag/
│   │   │   └── knowledge_base.py # Structured knowledge base for services
│   │   ├── ocr/
│   │   │   └── ocr_engine.py     # OCR & Identity document parser
│   │   ├── form_processing/
│   │   │   ├── form_analyzer.py  # Field bounding box & type detector
│   │   │   └── form_overlay.py   # Pillow canvas overlay engine (Navy ink)
│   │   ├── pdf/
│   │   │   └── pdf_generator.py  # ReportLab high-res print-ready PDF generator
│   │   ├── models/
│   │   │   └── database.py       # In-memory / File-backed JSON DB + Mongo support
│   │   └── schemas/
│   │       └── schemas.py        # Pydantic data models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── data/
│   ├── services/                 # Knowledge base configurations
│   └── sample_forms/             # Authentic sample form images & mock KYC docs
│       ├── bank_application_form.jpg # Andhra Pragathi Grameena Bank form
│       ├── sample_aadhaar.jpg        # Demo Aadhaar card
│       └── sample_income_cert.jpg    # Demo MeeSeva income certificate
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## 🚀 5. Quick Start Instructions

### Prerequisites
- **Python 3.10+**
- **Node.js 18+ & npm**

### Step 1: Start Backend (Terminal 1)
```bash
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000`.  
Interactive Swagger docs: `http://localhost:8000/docs`.

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🏆 6. How to Demonstrate at Hackathon

### Demo A — Digital Student Scholarship
1. On the home page, click **"🚀 Demo A: Student Scholarship"** (or click the large **"🎙️ Speak to FormSaathi"** button).
2. The user utterance is sent in Telugu: *"Naaku scholarship apply cheyyali. Nenu B.Tech student ni."*
3. FormSaathi recognizes the intent, maps it to **Post-Matric Student Scholarship (Jagananna Vidya Deevena)**, and speaks out the first question in Telugu.
4. Answer questions naturally using the microphone or quick-reply chips.
5. Click **"+ Test Sample Aadhaar"** in the document checklist.
6. OCR automatically extracts Name, DOB, and Aadhaar number and autofills the form.
7. Click **"Confirm & Generate Print-Ready PDF"** to produce an official application summary sheet.

### Demo B — Physical Bank Form (The Key Differentiator!)
1. Click **"📄 Upload a Form Photo"** or **"Demo B: Bank Form Upload"**.
2. Click **"Use Sample Bank Form (1-Click Demo)"** or upload your own paper form photo.
3. FormSaathi analyzes the form, recognizing **Andhra Pragathi Grameena Bank — Savings Account Opening Form** and identifies 15 distinct fields, bounding boxes, and official instructions.
4. The AI explains the form in Telugu and asks for applicant information step by step.
5. Click **"Fill Original Form & Generate PDF"**.
6. View the **Filled Form Preview**: Notice that the original bank form layout is **100% preserved**, with applicant answers neatly overlaid in realistic blue ballpoint ink.
7. Signature and photograph boxes are clearly labeled:
   - `✍ Signature Required - Please sign manually after printing`
   - `📷 Affix Recent Passport Size Photo Here`
   *(Zero fake signatures are ever created).*
8. Click **"Download PDF"** or **"Print Form"** for physical submission.

### Demo C — Validation & Conflict Detection (DOB Mismatch)
1. On the home page, click **"⚠️ Demo: Conflict Resolution"**.
2. The user tells FormSaathi their DOB is `15/06/2006`.
3. An Aadhaar card is uploaded whose OCR detects DOB as `15/06/2005`.
4. FormSaathi alerts the citizen:
   > ⚠️ *"మీ పుట్టిన తేదీలో తేడా గమనించాను. మీరు 15/06/2006 అని చెప్పారు, కానీ మీ Aadhaar Card లో 15/06/2005 అని ఉంది. దేనిని ఉపయోగించమంటారు?"*
5. Three intuitive action buttons are presented:
   - **[ Use Entered: 15/06/2006 ]**
   - **[ Use Document: 15/06/2005 ]**
   - **[ Edit Custom ]**
6. Select any choice to instantly resolve the conflict and update the application record.

---

## 🔒 7. Security & Privacy Highlights
- **Zero Sensitive Data Stored**: Demo data uses safe synthetic names and masked Aadhaar numbers.
- **No Fake Signatures**: FormSaathi never renders fraudulent biometrics or forged signatures; physical signing areas are explicitly marked for pen completion upon printing.
- **Fail-Safe Offline Demo Mode**: All OCR, RAG retrieval, and form overlays operate out of the box with zero external API dependencies required.

---

## 📜 8. License & Acknowledgments
Built with ❤️ for Indian citizens, students, elderly elders, and rural communities.
