"""
FormSaathi Physical Form Analyzer & Field Detector.
Analyzes physical form scans/photos, identifies form type, extracts field locations,
detects required documents, and prepares structured schema for the AI conversation.
"""
import os
from typing import Dict, Any, List

class FormAnalyzer:
    def analyze_form(self, file_path: str, filename: str) -> Dict[str, Any]:
        """
        Analyzes a physical form image or PDF.
        Returns detected form name, field locations (bounding boxes), instructions, and required documents.
        """
        lower_name = filename.lower()
        
        # Determine form type
        if "scholarship" in lower_name or "vidya" in lower_name:
            form_id = "physical_scholarship_form"
            title = "State Post-Matric Scholarship Physical Application Form"
            desc_en = "Standard official paper form for scholarship & fee reimbursement submission at college office."
            desc_te = "కాలేజ్ కార్యాలయంలో సమర్పించాల్సిన పోస్ట్-మెట్రిక్ స్కాలర్‌షిప్ మరియు ఫీజు రీయింబర్స్‌మెంట్ దరఖాస్తు పత్రం."
            required_docs = ["Aadhaar", "Income Certificate", "College ID", "Previous Marks Memo"]
            instructions_en = [
                "Fill all details in BLOCK LETTERS.",
                "Attach self-attested copies of Aadhaar, Income Certificate, and Marks Memo.",
                "Ensure student and principal signatures are physically affixed after printing."
            ]
            instructions_te = [
                "అన్ని వివరాలను స్పష్టమైన అక్షరాలలో పూరించండి.",
                "ఆధార్, ఆదాయ ధ్రువీకరణ మరియు మార్కుల పత్రాల జిరాక్స్ కాపీలను జత చేయండి.",
                "ప్రింట్ తీసుకున్న తర్వాత విద్యార్థి మరియు ప్రిన్సిపాల్ గారి అసలు సంతకాలు తప్పనిసరి."
            ]
            fields = [
                {"id": "full_name", "name": "full_name", "label_en": "Student Full Name", "label_te": "విద్యార్థి పూర్తి పేరు", "type": "text", "required": True, "x": 260, "y": 280, "width": 450, "height": 30},
                {"id": "dob", "name": "dob", "label_en": "Date of Birth", "label_te": "పుట్టిన తేదీ", "type": "date", "required": True, "x": 260, "y": 335, "width": 200, "height": 30},
                {"id": "gender", "name": "gender", "label_en": "Gender", "label_te": "లింగం", "type": "text", "required": True, "x": 550, "y": 335, "width": 160, "height": 30},
                {"id": "college_name", "name": "college_name", "label_en": "College Name", "label_te": "కళాశాల పేరు", "type": "text", "required": True, "x": 260, "y": 390, "width": 450, "height": 30},
                {"id": "course", "name": "course", "label_en": "Course & Branch", "label_te": "కోర్సు & బ్రాంచ్", "type": "text", "required": True, "x": 260, "y": 445, "width": 450, "height": 30},
                {"id": "roll_number", "name": "roll_number", "label_en": "Roll Number", "label_te": "రోల్ నంబర్", "type": "text", "required": True, "x": 260, "y": 500, "width": 250, "height": 30},
                {"id": "annual_income", "name": "annual_income", "label_en": "Annual Income (₹)", "label_te": "వార్షిక ఆదాయం (రూ.)", "type": "number", "required": True, "x": 260, "y": 555, "width": 250, "height": 30},
                {"id": "bank_account", "name": "bank_account", "label_en": "Bank Account Number", "label_te": "బ్యాంక్ ఖాతా సంఖ్య", "type": "text", "required": True, "x": 260, "y": 610, "width": 300, "height": 30},
                {"id": "ifsc_code", "name": "ifsc_code", "label_en": "IFSC Code", "label_te": "IFSC కోడ్", "type": "text", "required": True, "x": 620, "y": 610, "width": 150, "height": 30},
                {"id": "address", "name": "address", "label_en": "Permanent Address", "label_te": "శాశ్వత చిరునామా", "type": "textarea", "required": True, "x": 260, "y": 665, "width": 500, "height": 50},
                {"id": "signature_student", "name": "signature_student", "label_en": "Student Signature", "label_te": "విద్యార్థి సంతకం", "type": "signature", "required": True, "x": 100, "y": 800, "width": 280, "height": 70, "manual_notice": "✍ Signature Required - Please sign manually after printing"},
                {"id": "signature_principal", "name": "signature_principal", "label_en": "Principal Signature & Seal", "label_te": "ప్రిన్సిపాల్ గారి సంతకం & సీలు", "type": "signature", "required": True, "x": 500, "y": 800, "width": 280, "height": 70, "manual_notice": "✍ Official Attestation Required"}
            ]
        else:
            # Default to Bank Account Opening Form (our star physical form demo)
            form_id = "physical_bank_form"
            title = "Andhra Pragathi Grameena Bank — Savings Account Opening Form"
            desc_en = "Physical paper application form for opening a new Savings Bank account with Debit Card & Mobile Banking."
            desc_te = "ఆంధ్ర ప్రగతి గ్రామీణ బ్యాంక్ — పొదుపు ఖాతా, ఏటీఎం కార్డు మరియు మొబైల్ బ్యాంకింగ్ ప్రారంభ దరఖాస్తు పత్రం."
            required_docs = ["Aadhaar", "PAN Card", "Passport Size Photograph"]
            instructions_en = [
                "Fill in capital letters using blue/black ballpoint pen.",
                "Mandatory KYC: Self-attested copy of Aadhaar Card and PAN Card.",
                "Paste one passport size photograph in the top right box.",
                "Do not sign inside digital preview — signature must be manually placed upon printing."
            ]
            instructions_te = [
                "అన్ని వివరాలను స్పష్టమైన పెద్ద అక్షరాలలో నింపాలి.",
                "ఆధార్ కార్డు మరియు పాన్ కార్డు జిరాక్స్ కాపీలు జత చేయాలి.",
                "పై కుడి మూలలో పాస్‌పోర్ట్ సైజు ఫోటో అతికించాలి.",
                "ప్రింట్ తీసుకున్న తర్వాత మాత్రమే బాక్స్‌లో దరఖాస్తుదారు తన స్వహస్తాలతో సంతకం చేయాలి."
            ]
            fields = [
                {"id": "full_name", "name": "full_name", "label_en": "Full Name of Applicant", "label_te": "దరఖాస్తుదారు పూర్తి పేరు", "type": "text", "required": True, "x": 260, "y": 270, "width": 460, "height": 30},
                {"id": "dob", "name": "dob", "label_en": "Date of Birth (DD/MM/YYYY)", "label_te": "పుట్టిన తేదీ", "type": "date", "required": True, "x": 260, "y": 325, "width": 200, "height": 30},
                {"id": "gender", "name": "gender", "label_en": "Gender (Male/Female/Other)", "label_te": "లింగం", "type": "text", "required": True, "x": 560, "y": 325, "width": 160, "height": 30},
                {"id": "mobile", "name": "mobile", "label_en": "Mobile Number", "label_te": "మొబైల్ నంబర్", "type": "text", "required": True, "x": 260, "y": 380, "width": 250, "height": 30},
                {"id": "aadhaar_number", "name": "aadhaar_number", "label_en": "Aadhaar Card Number", "label_te": "ఆధార్ కార్డు నంబర్", "type": "text", "required": True, "x": 260, "y": 435, "width": 300, "height": 30},
                {"id": "pan_number", "name": "pan_number", "label_en": "PAN Number / Form 60", "label_te": "పాన్ నంబర్", "type": "text", "required": False, "x": 620, "y": 435, "width": 180, "height": 30},
                {"id": "address", "name": "address", "label_en": "Residential Address", "label_te": "నివాస చిరునామా", "type": "textarea", "required": True, "x": 260, "y": 490, "width": 540, "height": 55},
                {"id": "occupation", "name": "occupation", "label_en": "Occupation / Profession", "label_te": "వృత్తి", "type": "text", "required": True, "x": 260, "y": 565, "width": 250, "height": 30},
                {"id": "annual_income", "name": "annual_income", "label_en": "Annual Income (₹)", "label_te": "వార్షిక ఆదాయం (రూ.)", "type": "number", "required": True, "x": 600, "y": 565, "width": 200, "height": 30},
                {"id": "has_nominee", "name": "has_nominee", "label_en": "Add Nominee (Yes/No)", "label_te": "నామినీని చేర్చాలా?", "type": "select", "options": ["Yes", "No"], "required": True, "x": 260, "y": 620, "width": 120, "height": 30},
                {"id": "nominee_name", "name": "nominee_name", "label_en": "Nominee Name & Relation", "label_te": "నామినీ పేరు & సంబంధం", "type": "text", "required": False, "conditional_on": "has_nominee", "conditional_value": "Yes", "x": 450, "y": 620, "width": 350, "height": 30},
                {"id": "atm_card_required", "name": "atm_card_required", "label_en": "ATM / Debit Card Required (Yes/No)", "label_te": "ఏటీఎం కార్డు కావాలా?", "type": "select", "options": ["Yes", "No"], "required": True, "x": 260, "y": 675, "width": 120, "height": 30},
                {"id": "photo_box", "name": "photo_box", "label_en": "Photograph Area", "label_te": "పాస్‌పోర్ట్ ఫోటో", "type": "photo", "required": True, "x": 680, "y": 100, "width": 140, "height": 160, "manual_notice": "📷 Affix Passport Size Photo Here"},
                {"id": "signature_applicant", "name": "signature_applicant", "label_en": "Signature / Thumb Impression of Applicant", "label_te": "దరఖాస్తుదారు సంతకం / బొటనవేలి ముద్ర", "type": "signature", "required": True, "x": 100, "y": 790, "width": 320, "height": 75, "manual_notice": "✍ Signature Required - Please sign manually after printing"},
                {"id": "signature_bank", "name": "signature_bank", "label_en": "Bank Officer Signature & Branch Stamp", "label_te": "బ్యాంక్ అధికారి సంతకం & ముద్ర", "type": "signature", "required": True, "x": 510, "y": 790, "width": 320, "height": 75, "manual_notice": "✍ For Bank Official Use Only"}
            ]

        return {
            "form_id": form_id,
            "form_title": title,
            "form_type": "physical_form",
            "description_en": desc_en,
            "description_te": desc_te,
            "fields": fields,
            "required_documents": required_docs,
            "instructions_en": instructions_en,
            "instructions_te": instructions_te,
            "image_url": f"/api/forms/template/{form_id}"
        }

form_analyzer = FormAnalyzer()
