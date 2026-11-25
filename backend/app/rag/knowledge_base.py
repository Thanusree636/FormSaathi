"""
FormSaathi RAG Knowledge Base.
Contains structured service data, eligibility rules, document requirements, and multilingual conversational prompts
supporting all major Indian languages (Hindi, English, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia).
"""
from typing import Dict, Any, List, Optional
import re

SERVICES_DB: Dict[str, Dict[str, Any]] = {
    "student_scholarship": {
        "service_id": "student_scholarship",
        "title_en": "Post-Matric Student Scholarship (Jagananna Vidya Deevena)",
        "title_hi": "पोस्ट-मैट्रिक छात्रवृत्ति (विद्या दीवेना योजना)",
        "title_te": "పోస్ట్-మెట్రిక్ విద్యార్థి స్కాలర్‌షిప్ (జగనన్న విద్యా దీవెన)",
        "title_ta": "மெட்ரிக் பிந்தைய கல்வி உதவித்தொகை",
        "title_kn": "ಮೆಟ್ರಿಕ್ ನಂತರದ ವಿದ್ಯಾರ್ಥಿವೇತನ ಯೋಜನೆ",
        "title_bn": "পোস্ট-ম্যাট্রিক স্কলারশিপ প্রকল্প",
        "title_mr": "मॅट्रिकोत्तर विद्यार्थी शिष्यवृत्ती योजना",
        "department": "Department of Higher Education & Social Welfare",
        "official_source": "https://jnanabhumi.ap.gov.in / National Scholarship Portal",
        "description_en": "Financial assistance for B.Tech, Degree, and Professional College students covering 100% tuition fees and hostel maintenance.",
        "description_hi": "बी.टेक, डिग्री और व्यावसायिक कॉलेज के छात्रों के लिए 100% ट्यूशन फीस और छात्रावास सहायता हेतु सरकारी योजना।",
        "description_te": "బీటెక్, డిగ్రీ మరియు వృత్తి విద్యా విద్యార్థుల ట్యూషన్ ఫీజు రీయింబర్స్‌మెంట్ మరియు హాస్టల్ ఖర్చుల కోసం ప్రభుత్వం అందించే స్కాలర్‌షిప్ పథకం.",
        "eligibility_en": [
            "Must be enrolled in recognized Polytechnic, ITI, Degree, or B.Tech course",
            "Annual family income must be below ₹2,50,000",
            "Must possess valid Aadhaar card and active bank account",
            "Student must have minimum 75% attendance"
        ],
        "required_documents": [
            {
                "doc_type": "aadhaar",
                "name_en": "Student Aadhaar Card",
                "name_hi": "छात्र आधार कार्ड",
                "name_te": "విద్యార్థి ఆధార్ కార్డు",
                "required": True
            },
            {
                "doc_type": "college_id",
                "name_en": "College ID / Bonafide Certificate",
                "name_hi": "कॉलेज आईडी / बोनाफाइड प्रमाणपत्र",
                "name_te": "కాలేజ్ ఐడీ కార్డు లేదా బోనఫైడ్ సర్టిఫికెట్",
                "required": True
            },
            {
                "doc_type": "income_cert",
                "name_en": "Income Certificate",
                "name_hi": "आय प्रमाण पत्र",
                "name_te": "ఆదాయ ధ్రువీకరణ పత్రం (Income Certificate)",
                "required": True
            },
            {
                "doc_type": "marks_memo",
                "name_en": "Previous Semester / 12th Marks Memo",
                "name_hi": "पिछली कक्षा / 12वीं की अंकतालिका",
                "name_te": "మునుపటి సెమిస్టర్ లేదా ఇంటర్ మార్కుల మెమో",
                "required": True
            }
        ],
        "fields": [
            {
                "id": "full_name",
                "name": "full_name",
                "label_en": "Student Full Name",
                "label_hi": "छात्र का पूरा नाम",
                "label_te": "విద్యార్థి పూర్తి పేరు",
                "type": "text",
                "required": True,
                "question_en": "What is your full name as per your official documents?",
                "question_hi": "आधार कार्ड के अनुसार आपका पूरा नाम क्या है?",
                "question_te": "మీ ఆధార్ కార్డు ప్రకారం మీ పూర్తి పేరు ఏమిటి?",
                "extract_from": "aadhaar.name"
            },
            {
                "id": "dob",
                "name": "dob",
                "label_en": "Date of Birth (DD/MM/YYYY)",
                "label_hi": "जन्म तिथि (दिन/माह/वर्ष)",
                "label_te": "పుట్టిన తేదీ (రోజు/నెల/సంవత్సరం)",
                "type": "date",
                "required": True,
                "question_en": "What is your date of birth?",
                "question_hi": "आपकी जन्म तिथि क्या है? (उदाहरण: 15/06/2004)",
                "question_te": "మీ పుట్టిన తేదీ ఎప్పుడు? (ఉదాహరణకు: 15/06/2004)",
                "extract_from": "aadhaar.dob"
            },
            {
                "id": "course",
                "name": "course",
                "label_en": "Course & Year (e.g. B.Tech 3rd Year)",
                "label_hi": "कोर्स और वर्ष (जैसे B.Tech)",
                "label_te": "కోర్సు మరియు సంవత్సరం (ఉదా: B.Tech)",
                "type": "text",
                "required": True,
                "question_en": "Which course and year are you currently studying?",
                "question_hi": "आप वर्तमान में कौन सा कोर्स और किस वर्ष में पढ़ रहे हैं?",
                "question_te": "మీరు ప్రస్తుతం ఏ కోర్సు, ఏ సంవత్సరం చదువుతున్నారు?",
                "extract_from": "college_id.course"
            },
            {
                "id": "college_name",
                "name": "college_name",
                "label_en": "College / Institute Name",
                "label_hi": "कॉलेज या संस्थान का नाम",
                "label_te": "కళాశాల పేరు",
                "type": "text",
                "required": True,
                "question_en": "What is your college or institute name?",
                "question_hi": "आपके कॉलेज या संस्थान का नाम क्या है?",
                "question_te": "మీ కాలేజీ పేరు చెప్పండి?",
                "extract_from": "college_id.college_name"
            },
            {
                "id": "roll_number",
                "name": "roll_number",
                "label_en": "Roll / Hall Ticket Number",
                "label_hi": "रोल नंबर / हॉल टिकट नंबर",
                "label_te": "రోల్ నంబర్ / హాల్ టికెట్ నంబర్",
                "type": "text",
                "required": True,
                "question_en": "What is your College Roll Number or Hall Ticket Number?",
                "question_hi": "आपका कॉलेज रोल नंबर या हॉल टिकट नंबर क्या है?",
                "question_te": "మీ కాలేజీ రోల్ నంబర్ లేదా హాల్ టికెట్ నంబర్ ఏమిటి?",
                "extract_from": "college_id.roll_number"
            },
            {
                "id": "annual_income",
                "name": "annual_income",
                "label_en": "Annual Family Income (₹)",
                "label_hi": "पारिवारिक वार्षिक आय (रु.)",
                "label_te": "కుటుంబ వార్షిక ఆదాయం (రూ.)",
                "type": "number",
                "required": True,
                "question_en": "What is your annual family income mentioned in your Income Certificate?",
                "question_hi": "आपके आय प्रमाण पत्र में कुल वार्षिक पारिवारिक आय कितनी है?",
                "question_te": "మీ ఆదాయ ధ్రువీకరణ పత్రంలో ఉన్న వార్షిక కుటుంబ ఆదాయం ఎంత?",
                "extract_from": "income_cert.annual_income"
            },
            {
                "id": "bank_account",
                "name": "bank_account",
                "label_en": "Bank Account Number",
                "label_hi": "बैंक खाता संख्या",
                "label_te": "బ్యాంక్ ఖాతా సంఖ్య",
                "type": "text",
                "required": True,
                "question_en": "Please provide your Aadhaar-linked Bank Account number for scholarship disbursement.",
                "question_hi": "छात्रवृत्ति राशि प्राप्त करने हेतु आधार से जुड़ा बैंक खाता नंबर बताएं।",
                "question_te": "స్కాలర్‌షిప్ నగదు జమ కావడానికి మీ ఆధార్ అనుసంధాన బ్యాంక్ ఖాతా సంఖ్య చెప్పండి.",
                "extract_from": "bank_passbook.account_number"
            },
            {
                "id": "is_hosteller",
                "name": "is_hosteller",
                "label_en": "Hostel Resident or Day Scholar?",
                "label_hi": "हॉस्टल में रहते हैं या डे-स्कॉलर?",
                "label_te": "హాస్టల్ లో ఉంటున్నారా లేదా డే స్కాలరా?",
                "type": "select",
                "options": ["Hosteller", "Day Scholar"],
                "required": True,
                "question_en": "Are you staying in a college hostel or are you a day scholar?",
                "question_hi": "क्या आप कॉलेज हॉस्टल में रहते हैं या डे-स्कॉलर हैं?",
                "question_te": "మీరు కాలేజీ హాస్టల్‌లో ఉంటున్నారా లేక డే స్కాలర్‌గా రోజూ ఇంటి నుంచి వస్తున్నారా?",
                "extract_from": None
            }
        ]
    },
    "income_certificate": {
        "service_id": "income_certificate",
        "title_en": "Revenue Income Certificate (State Portal / MeeSeva)",
        "title_hi": "राजस्व आय प्रमाण पत्र (ई-डिस्ट्रिक्ट / मीसेवा)",
        "title_te": "ఆదాయ ధ్రువీకరణ పత్రం (మీసేవ / గ్రామ వార్డు సచివాలయం)",
        "department": "Revenue Department",
        "official_source": "State Revenue Services & e-District Portals",
        "description_en": "Official government certificate certifying annual family income required for scholarships and subsidies.",
        "description_hi": "छात्रवृत्ति, शुल्क छूट और सरकारी योजनाओं के लिए आवश्यक पारिवारिक आय प्रमाण पत्र।",
        "description_te": "స్కాలర్‌షిప్‌లు, సంక్షేమ పథకాలు మరియు ఫీజు రాయితీల కోసం అవసరమైన కుటుంబ వార్షిక ఆదాయ ధ్రువీకరణ పత్రం.",
        "required_documents": [
            {"doc_type": "aadhaar", "name_en": "Aadhaar Card", "name_hi": "आधार कार्ड", "name_te": "ఆధార్ కార్డు", "required": True},
            {"doc_type": "ration_card", "name_en": "Ration Card", "name_hi": "राशन कार्ड", "name_te": "రేషన్ కార్డు", "required": True}
        ],
        "fields": [
            {
                "id": "applicant_name",
                "name": "applicant_name",
                "label_en": "Applicant Full Name",
                "label_hi": "आवेदक का पूरा नाम",
                "label_te": "దరఖాస్తుదారుని పూర్తి పేరు",
                "type": "text",
                "required": True,
                "question_en": "What is the applicant's full name as per Aadhaar?",
                "question_hi": "आधार के अनुसार आवेदक का पूरा नाम क्या है?",
                "question_te": "దరఖాస్తుదారుని పూర్తి పేరు ఆధార్ ప్రకారం చెప్పండి?",
                "extract_from": "aadhaar.name"
            },
            {
                "id": "annual_income_applied",
                "name": "annual_income_applied",
                "label_en": "Declared Annual Income (₹)",
                "label_hi": "घोषित वार्षिक आय (रु.)",
                "label_te": "ప్రకటించిన వార్షిక ఆదాయం (రూ.)",
                "type": "number",
                "required": True,
                "question_en": "What is your total family annual income from all sources in rupees?",
                "question_hi": "सभी स्रोतों से आपके परिवार की कुल वार्षिक आय रुपये में कितनी है?",
                "question_te": "అన్ని మార్గాల ద్వారా మీ కుటుంబానికి వచ్చే వార్షిక ఆదాయం ఎంత?",
                "extract_from": None
            }
        ]
    },
    "bank_account": {
        "service_id": "bank_account",
        "title_en": "Customer Account Opening Form (Savings Bank)",
        "title_hi": "ग्राहक बचत बैंक खाता खोलने का आवेदन पत्र",
        "title_te": "బ్యాంక్ ఖాతా ప్రారంభ దరఖాస్తు పత్రం (సేవింగ్స్ బ్యాంక్)",
        "department": "Banking & Financial Services",
        "official_source": "Reserve Bank of India KYC Guidelines & Bank Standards",
        "description_en": "Standard Bank Customer Account Opening Form for Savings Account with ATM card and mobile banking.",
        "description_hi": "बचत खाता, एटीएम कार्ड और मोबाइल बैंकिंग सुविधाओं हेतु बैंक खाता खोलने का आवेदन पत्र।",
        "description_te": "పొదుపు ఖాతా, ఏటీఎం కార్డు మరియు మొబైల్ బ్యాంకింగ్ సదుపాయాల కోసం బ్యాంక్ ఖాతా దరఖాస్తు ఫారమ్.",
        "required_documents": [
            {"doc_type": "aadhaar", "name_en": "Aadhaar Card", "name_hi": "आधार कार्ड", "name_te": "ఆధార్ కార్డు", "required": True},
            {"doc_type": "pan", "name_en": "PAN Card", "name_hi": "पैन कार्ड", "name_te": "పాన్ కార్డు", "required": True}
        ],
        "fields": [
            {
                "id": "full_name",
                "name": "full_name",
                "label_en": "Full Name of Applicant",
                "label_hi": "आवेदक का पूरा नाम",
                "label_te": "దరఖాస్తుదారు పూర్తి పేరు",
                "type": "text",
                "required": True,
                "question_en": "What is your full name as per official ID documents?",
                "question_hi": "पहचान पत्र के अनुसार आपका पूरा नाम क्या है?",
                "question_te": "మీ అధికారిక పత్రాల ప్రకారం మీ పూర్తి పేరు ఏమిటి?",
                "extract_from": "aadhaar.name"
            },
            {
                "id": "dob",
                "name": "dob",
                "label_en": "Date of Birth (DD/MM/YYYY)",
                "label_hi": "जन्म तिथि (दिन/माह/वर्ष)",
                "label_te": "పుట్టిన తేదీ",
                "type": "date",
                "required": True,
                "question_en": "What is your date of birth?",
                "question_hi": "आपकी जन्म तिथि क्या है?",
                "question_te": "మీ పుట్టిన తేదీ ఎప్పుడు?",
                "extract_from": "aadhaar.dob"
            },
            {
                "id": "mobile",
                "name": "mobile",
                "label_en": "Mobile Number for SMS Alerts",
                "label_hi": "एसएमएस अलर्ट हेतु मोबाइल नंबर",
                "label_te": "మొబైల్ నంబర్",
                "type": "text",
                "required": True,
                "question_en": "What is your 10-digit mobile number for bank alerts?",
                "question_hi": "बैंक अलर्ट्स के लिए अपना 10 अंकों का मोबाइल नंबर बताएं?",
                "question_te": "బ్యాంక్ లావాదేవీల అలర్ట్స్ కోసం మీ 10 అంకెల మొబైల్ నంబర్ చెప్పండి?",
                "extract_from": None
            }
        ]
    }
}

class RAGRetriever:
    """
    Intelligent keyword + semantic entity matcher that maps conversational user utterances
    across ALL Indian languages (Hindi, English, Telugu, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia).
    """
    def __init__(self):
        self.keywords_map = {
            "student_scholarship": [
                # English
                "scholarship", "vidya deevena", "btech", "b.tech", "college", "fee", "student", "studies", "degree",
                # Hindi
                "छात्रवृत्ति", "स्कॉलरशिप", "वजीफा", "कॉलेज", "पढ़ाई", "शिक्षा", "फीस", "हॉस्टल",
                # Telugu
                "స్కాలర్‌షిప్", "చదువు", "కాలేజ్", "ఫీజు", "హాస్టల్", "ట్యూషన్", "విద్యార్థి",
                # Tamil
                "உதவித்தொகை", "படிப்பு", "கல்லூரி", "கட்டணம்",
                # Kannada
                "ವಿದ್ಯಾರ್ಥಿವೇತನ", "ಕಾಲೇಜು", "ಶಿಕ್ಷಣ", "ಶುಲ್ಕ",
                # Bengali
                "স্কলারশিপ", "ছাত্রবৃত্তি", "কলেজ", "পড়াশোনা", "ফি",
                # Marathi
                "शिष्यवृत्ती", "कॉलेज", "शिक्षण", "फी",
                # Gujarati
                "શિષ્યવૃત્તિ", "કોલેજ", "ભણતર", "ફી",
                # Punjabi
                "ਵਜ਼ੀਫ਼ਾ", "ਕਾਲਜ", "ਪੜ੍ਹਾਈ", "ਫੀਸ",
                # Odia
                "ଛାତ୍ରବୃତ୍ତି", "ସ୍କଲାରସିପ୍", "କଲେଜ", "ପାଠପଢ଼ା"
            ],
            "income_certificate": [
                # English
                "income", "income cert", "salary", "revenue", "tahsildar", "meeseva", "certificate",
                # Hindi
                "आय", "आय प्रमाण पत्र", "आमदनी", "वेतन", "तहसील", "तहसीलदार", "प्रमाणपत्र",
                # Telugu
                "ఆదాయం", "ఆదాయ ధ్రువీకరణ", "మీసేవ", "ఆదాయ పత్రం", "సచివాలయం",
                # Tamil
                "வருமான சான்றிதழ்", "வருமானம்", "தாசில்தார்",
                # Kannada
                "ಆದಾಯ ಪ್ರಮಾಣಪತ್ರ", "ಆದಾಯ",
                # Bengali
                "আয়ের সার্টিফিকেট", "আয়", "বেতন",
                # Marathi
                "उत्पन्नाचा दाखला", "उत्पन्न", "पगार",
                # Gujarati
                "આવકનો દાખલો", "આવક", "પગાર",
                # Punjabi
                "ਆਮਦਨ ਸਰਟੀਫਿਕੇਟ", "ਆਮਦਨੀ",
                # Odia
                "ଆୟ ପ୍ରମାଣପତ୍ର", "ଆୟ"
            ],
            "bank_account": [
                # English
                "bank", "account", "savings", "passbook", "atm", "debit card", "sbi", "bank form", "open account",
                # Hindi
                "बैंक", "खाता", "बैंक खाता", "बचत खाता", "पासबुक", "एटीएम", "खाता खोलना",
                # Telugu
                "బ్యాంక్", "ఖాతా", "పాస్‌బుక్", "పాస్ బుక్", "ఏటీఎం", "ఖాతా తెరవడం",
                # Tamil
                "வங்கி", "கணக்கு", "பாஸ்புக்", "வங்கி கணக்கு",
                # Kannada
                "ಬ್ಯಾಂಕ್", "ಖಾತೆ", "ಪಾಸ್‌ಬುಕ್", "ಬ್ಯಾಂಕ್ ಖಾತೆ",
                # Bengali
                "ব্যাংক", "অ্যাকাউন্ট", "ব্যাংক খাতা", "পাসবই",
                # Marathi
                "बँक", "खाते", "बँक खाते", "पासबुक",
                # Gujarati
                "બેંક", "ખાતું", "બેંક ખાતું", "પાસબુક",
                # Punjabi
                "ਬੈਂਕ", "ਖਾਤਾ", "ਪਾਸਬੁੱਕ",
                # Odia
                "ବ୍ୟାଙ୍କ", "ଖାତା", "ବ୍ୟାଙ୍କ ଖାତା", "ପାସବୁକ୍"
            ]
        }

    def retrieve(self, query: str) -> Optional[Dict[str, Any]]:
        clean_query = query.lower()
        
        # Check high-confidence service matches
        scores = {}
        for service_id, keywords in self.keywords_map.items():
            score = 0
            for kw in keywords:
                if kw.lower() in clean_query:
                    score += 2
            scores[service_id] = score

        best_match = max(scores, key=scores.get)
        if scores[best_match] > 0:
            return SERVICES_DB[best_match]
        
        # Fallback to scholarship if query mentions education
        if any(term in clean_query for term in ["btech", "b.tech", "study", "engineering", "कॉलेज", "चదువు"]):
            return SERVICES_DB["student_scholarship"]

        return None

rag_retriever = RAGRetriever()
