"""
FormSaathi Main FastAPI Application.
Voice-First Multilingual Citizen Form Filling Assistant.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI(
    title="FormSaathi API",
    description="Multilingual Voice-First Citizen Form Assistant Backend",
    version="1.0.0"
)

# CORS configuration for local development and demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow local React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(router)

# Mount static directories for uploads and generated PDFs
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
GENERATED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generated")
SAMPLE_FORMS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "sample_forms")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(SAMPLE_FORMS_DIR, exist_ok=True)

app.mount("/static/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
app.mount("/static/generated", StaticFiles(directory=GENERATED_DIR), name="generated")
app.mount("/static/samples", StaticFiles(directory=SAMPLE_FORMS_DIR), name="samples")

@app.get("/")
def root():
    return {
        "project": "FormSaathi",
        "tagline": "Tell us what you need. Show us the form. FormSaathi helps you complete the rest.",
        "status": "Online & Ready",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
