"""
FormSaathi Intent Detection Agent.
Detects citizen goal from voice/text across all major Indian languages (Hindi, English, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia).
"""
import re
from typing import Dict, Any, Optional
from app.rag.knowledge_base import rag_retriever, SERVICES_DB

class IntentAgent:
    def process_utterance(self, text: str, language: str = "hi") -> Dict[str, Any]:
        cleaned = text.strip()
        matched_service = rag_retriever.retrieve(cleaned)
        
        entities = {}
        # Entity extraction
        if re.search(r'\bb\.?tech\b|बी\.?टेक|బీటెక్', cleaned, re.IGNORECASE):
            entities["course"] = "B.Tech"
            entities["user_type"] = "Student"
        elif re.search(r'\bdegree\b|डिग्री|డిగ్రీ', cleaned, re.IGNORECASE):
            entities["course"] = "Degree"
            entities["user_type"] = "Student"

        # Localized greetings and prompts map
        greetings = {
            "hi": {
                "reply": "नमस्ते! आप **{service_title}** के लिए आवेदन करना चाहते हैं। मैं आपकी पूरी सहायता करूँगा। आइए कुछ आवश्यक जानकारी एकत्र करते हैं।",
                "audio": "नमस्ते! {service_title} आवेदन शुरू करने के लिए, आधार कार्ड के अनुसार आपका पूरा नाम क्या है?",
                "physical": "नमस्ते! कृपया अपने पेपर फ़ॉर्म की फ़ोटो अपलोड करें। मैं इसे पढ़कर आपको पूरी जानकारी दूँगा।",
                "default": "नमस्ते! क्या आप छात्रवृत्ति, आय प्रमाण पत्र या बैंक फ़ॉर्म भरना चाहते हैं? कृपया बताएं।"
            },
            "en": {
                "reply": "Hello! You would like to apply for **{service_title}**. I will guide you step by step. Let's collect a few necessary details.",
                "audio": "Hello! To start your {service_title} application, what is your full name as per your official documents?",
                "physical": "Please upload a photo or scan of your physical form. I will analyze its fields and assist you.",
                "default": "Hello! Would you like help with a Student Scholarship, Income Certificate, or a Physical Bank Form? Please tell me what you need."
            },
            "te": {
                "reply": "నమస్కారం! మీరు **{service_title}** కోసం దరఖాస్తు చేయాలనుకుంటున్నారు. నేను మీకు సహాయం చేస్తాను. కొన్ని ముఖ్యమైన వివరాలు తెలుసుకుందాం.",
                "audio": "నమస్కారం! మీరు {service_title} కోసం దరఖాస్తు చేయాలనుకుంటున్నారు. మొదటగా, మీ ఆధార్ కార్డు ప్రకారం మీ పూర్తి పేరు ఏమిటి?",
                "physical": "మీ దగ్గర ఉన్న ఫిజికల్ ఫారమ్ ఫోటోను అప్‌లోడ్ చేయండి. నేను చదివి మీకు వివరిస్తాను.",
                "default": "నమస్కారం! మీరు స్కాలర్‌షిప్, ఆదాయ ధ్రువీకరణ పత్రం లేదా బ్యాంక్ ఖాతా ఫారమ్ దరఖాస్తు చేయాలనుకుంటున్నారా? చెప్పండి."
            },
            "ta": {
                "reply": "வணக்கம்! நீங்கள் **{service_title}** விண்ணப்பிக்க விரும்புகிறீர்கள். நான் உங்களுக்கு உதவுகிறேன்.",
                "audio": "வணக்கம்! உங்கள் அதிகாரப்பூர்வ ஆவணங்களின்படி உங்கள் முழு பெயர் என்ன?",
                "physical": "உங்கள் காகித படிவத்தின் புகைப்படத்தைப் பதிவேற்றவும். நான் அதை பகுப்பாய்வு செய்து உதவுகிறேன்.",
                "default": "வணக்கம்! உங்களுக்கு கல்வி உதவித்தொகை, வருமான சான்றிதழ் அல்லது வங்கி படிவம் தேவையா? கூறுங்கள்."
            },
            "kn": {
                "reply": "ನಮಸ್ಕಾರ! ನೀವು **{service_title}** ಗಾಗಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಲು ಬಯಸುತ್ತೀರಿ. ನಾನು ನಿಮಗೆ ಹಂತ ಹಂತವಾಗಿ ಮಾರ್ಗದರ್ಶನ ನೀಡುತ್ತೇನೆ.",
                "audio": "ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಅಧಿಕೃತ ದಾಖಲೆಗಳ ಪ್ರಕಾರ ನಿಮ್ಮ ಪೂರ್ಣ ಹೆಸರು ಏನು?",
                "physical": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಕಾಗದದ ಫಾರ್ಮ್ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. ನಾನು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.",
                "default": "ನಮಸ್ಕಾರ! ನಿಮಗೆ ವಿದ್ಯಾರ್ಥಿವೇತನ ಅಥವಾ ಬ್ಯಾಂಕ್ ಫಾರ್ಮ್ ಸಹಾಯ ಬೇಕೇ? ತಿಳಿಸಿ."
            },
            "mr": {
                "reply": "नमस्कार! आपण **{service_title}** साठी अर्ज करू इच्छिता. मी आपल्याला मदत करतो.",
                "audio": "नमस्कार! आपल्या कागदपत्रांनुसार आपले पूर्ण नाव काय आहे?",
                "physical": "कृपया आपल्या फॉर्मचा फोटो अपलोड करा. मी तो भरण्यास मदत करेन.",
                "default": "नमस्कार! आपल्याला शिष्यवृत्ती किंवा बँक फॉर्म हवा आहे का? कृपया सांगा."
            },
            "bn": {
                "reply": "নমস্কার! আপনি **{service_title}** এর জন্য আবেদন করতে চান। আমি আপনাকে সাহায্য করব।",
                "audio": "নমস্কার! আপনার নথিপত্র অনুযায়ী সম্পূর্ণ নাম কী?",
                "physical": "আপনার ফর্মের ছবি আপলোড করুন। আমি আপনাকে সাহায্য করব।",
                "default": "নমস্কার! আপনার কি স্কলারশিপ বা ব্যাঙ্ক ফর্ম দরকার? বলুন।"
            }
        }

        lang_greet = greetings.get(language, greetings["hi"])

        if matched_service:
            service_id = matched_service["service_id"]
            title_key = f"title_{language}"
            service_title = matched_service.get(title_key) or matched_service.get("title_hi") or matched_service["title_en"]

            q_key = f"question_{language}"
            first_field = matched_service["fields"][0]
            first_q = first_field.get(q_key) or first_field.get("question_hi") or first_field["question_en"]

            reply = lang_greet["reply"].format(service_title=service_title)
            prompt_audio = lang_greet["audio"].format(service_title=service_title)

            return {
                "intent": service_id,
                "confidence": 0.95,
                "detected_language": language,
                "service_id": service_id,
                "service_name": service_title,
                "extracted_entities": entities,
                "reply_text": reply,
                "reply_audio_prompt": prompt_audio,
                "next_question": first_q,
                "field_to_fill": first_field["id"]
            }

        # Physical form upload intent
        if any(w in cleaned.lower() for w in ["form", "photo", "paper", "upload", "फ़ॉर्म", "कागज़", "फोटो", "ఫారం", "కాగితం", "படிவம்", "ಫಾರ್ಮ್"]):
            return {
                "intent": "physical_form",
                "confidence": 0.90,
                "detected_language": language,
                "service_id": "bank_account",
                "service_name": "Physical Form Assistant",
                "extracted_entities": entities,
                "reply_text": lang_greet["physical"],
                "reply_audio_prompt": lang_greet["physical"],
                "next_question": "Upload Form",
                "field_to_fill": None
            }

        # Fallback
        return {
            "intent": "general",
            "confidence": 0.5,
            "detected_language": language,
            "service_id": None,
            "service_name": None,
            "extracted_entities": entities,
            "reply_text": lang_greet["default"],
            "reply_audio_prompt": lang_greet["default"],
            "next_question": None,
            "field_to_fill": None
        }

intent_agent = IntentAgent()
