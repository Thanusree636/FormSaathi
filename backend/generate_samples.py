"""
Generates crisp, high-resolution sample physical forms and mock KYC documents for FormSaathi demos.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int = 18, bold: bool = False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()

def create_bank_form(output_path: str):
    # A4 proportion: 850 x 1150
    w, h = 850, 1150
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(15, 30, 60), width=3)
    draw.rectangle([25, 25, w - 25, h - 25], outline=(180, 190, 205), width=1)

    # Header Banner
    draw.rectangle([25, 25, w - 25, 95], fill=(16, 52, 110))
    title_font = get_font(22, bold=True)
    draw.text((45, 36), "ANDHRA PRAGATHI GRAMEENA BANK", fill=(255, 255, 255), font=title_font)
    sub_font = get_font(13)
    draw.text((45, 66), "A Scheduled Bank Owned by Govt. of India, State Govt. & Canara Bank | Head Office: Kadapa", fill=(220, 235, 255), font=sub_font)

    # Form Title
    form_head_font = get_font(18, bold=True)
    draw.rectangle([25, 105, 650, 145], fill=(240, 244, 250))
    draw.text((45, 115), "APPLICATION FORM FOR OPENING RESIDENT SAVINGS BANK ACCOUNT", fill=(16, 52, 110), font=form_head_font)

    note_font = get_font(12)
    draw.text((45, 155), "Branch: VIJAYAWADA MAIN (02194)  |  Customer CIF / KYC Type: REGULAR CITIZEN", fill=(50, 60, 80), font=note_font)
    draw.text((45, 175), "Note: Fill in CAPITAL letters. Fields marked with (*) are mandatory under RBI KYC norms.", fill=(180, 40, 40), font=note_font)

    # Photo Box on top right
    draw.rectangle([680, 100, 820, 260], outline=(100, 110, 130), width=2, fill=(250, 250, 250))
    photo_font = get_font(12)
    draw.text((700, 150), "AFFIX RECENT", fill=(120, 130, 140), font=photo_font)
    draw.text((705, 170), "PASSPORT SIZE", fill=(120, 130, 140), font=photo_font)
    draw.text((705, 190), "PHOTOGRAPH", fill=(120, 130, 140), font=photo_font)
    draw.text((720, 210), "HERE", fill=(120, 130, 140), font=photo_font)

    # Section 1: Personal Details
    sec_font = get_font(14, bold=True)
    draw.rectangle([40, 220, 650, 245], fill=(220, 230, 245))
    draw.text((50, 225), "SECTION A — APPLICANT PERSONAL INFORMATION", fill=(16, 52, 110), font=sec_font)

    lbl_font = get_font(13, bold=True)
    box_border = (160, 170, 185)

    # 1. Full Name
    draw.text((45, 275), "1. Full Name of Applicant * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 270, 720, 300], outline=box_border, width=1, fill=(255, 255, 255))

    # 2. DOB & Gender
    draw.text((45, 330), "2. Date of Birth (DD/MM/YYYY) * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 325, 460, 355], outline=box_border, width=1, fill=(255, 255, 255))
    draw.text((480, 330), "Gender * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([560, 325, 720, 355], outline=box_border, width=1, fill=(255, 255, 255))

    # 3. Mobile Number
    draw.text((45, 385), "3. Mobile No. (for SMS Alerts) * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 380, 510, 410], outline=box_border, width=1, fill=(255, 255, 255))

    # 4. Aadhaar & PAN
    draw.text((45, 440), "4. Aadhaar Card Number * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 435, 560, 465], outline=box_border, width=1, fill=(255, 255, 255))
    draw.text((570, 440), "PAN :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([620, 435, 800, 465], outline=box_border, width=1, fill=(255, 255, 255))

    # 5. Address
    draw.text((45, 495), "5. Full Residential Address * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 490, 800, 545], outline=box_border, width=1, fill=(255, 255, 255))

    # 6. Occupation & Income
    draw.text((45, 570), "6. Occupation / Profession * :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 565, 510, 595], outline=box_border, width=1, fill=(255, 255, 255))
    draw.text((520, 570), "Income (₹) :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([600, 565, 800, 595], outline=box_border, width=1, fill=(255, 255, 255))

    # Section 2: Account Features & Nominee
    draw.rectangle([40, 610, w - 40, 635], fill=(220, 230, 245))
    draw.text((50, 615), "SECTION B — NOMINATION & ACCOUNT SERVICES", fill=(16, 52, 110), font=sec_font)

    # 7. Nominee
    draw.text((45, 650), "7. Add Nominee? (Yes/No) :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 645, 380, 675], outline=box_border, width=1, fill=(255, 255, 255))
    draw.text((400, 650), "Nominee Name & Rel :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([550, 645, 800, 675], outline=box_border, width=1, fill=(255, 255, 255))

    # 8. ATM Card
    draw.text((45, 700), "8. Debit Card / ATM Facility? :", fill=(20, 30, 50), font=lbl_font)
    draw.rectangle([260, 695, 380, 725], outline=box_border, width=1, fill=(255, 255, 255))

    # Section 3: Declaration & Signatures
    draw.rectangle([40, 740, w - 40, 765], fill=(220, 230, 245))
    draw.text((50, 745), "SECTION C — DECLARATION & PHYSICAL SIGNATURES", fill=(16, 52, 110), font=sec_font)

    decl_font = get_font(11)
    draw.text((45, 770), "I hereby declare that the details furnished above are true and correct to the best of my knowledge.", fill=(60, 70, 85), font=decl_font)

    # Signature Boxes
    draw.rectangle([60, 810, 400, 910], outline=(100, 110, 130), width=1, fill=(255, 255, 255))
    draw.text((70, 920), "Signature / Thumb Impression of Applicant *", fill=(20, 30, 50), font=lbl_font)
    draw.text((70, 820), "✍ SIGN HERE (PHYSICAL SIGNATURE)", fill=(180, 180, 190), font=get_font(13))

    draw.rectangle([450, 810, 790, 910], outline=(100, 110, 130), width=1, fill=(255, 255, 255))
    draw.text((460, 920), "Signature of Verifying Bank Official & Stamp", fill=(20, 30, 50), font=lbl_font)
    draw.text((460, 820), "OFFICIAL BANK STAMP & SEAL", fill=(180, 180, 190), font=get_font(13))

    # Footer
    draw.line([30, 970, w - 30, 970], fill=(200, 210, 220), width=1)
    draw.text((45, 985), "FormSaathi Physical Form Assistant Engine | Form Code: APGB-SB-2026/V1", fill=(120, 130, 140), font=get_font(11))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"Generated bank form: {output_path}")

def create_sample_aadhaar(output_path: str):
    w, h = 600, 380
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline=(200, 40, 40), width=2)
    # Header tri-color stripe
    draw.rectangle([10, 10, w - 10, 30], fill=(255, 153, 51))
    draw.rectangle([10, 30, w - 10, 50], fill=(255, 255, 255))
    draw.rectangle([10, 50, w - 10, 70], fill=(19, 136, 8))

    draw.text((120, 25), "GOVERNMENT OF INDIA - UNIQUE IDENTIFICATION AUTHORITY", fill=(10, 30, 80), font=get_font(12, bold=True))
    draw.text((180, 45), "భారత విశిష్ట గుర్తింపు ప్రాధికార సంస్థ - ఆధార్", fill=(10, 30, 80), font=get_font(12, bold=True))

    # Photo Box
    draw.rectangle([35, 90, 155, 235], outline=(150, 150, 150), width=1, fill=(235, 240, 248))
    draw.text((50, 150), "PHOTO", fill=(140, 150, 170), font=get_font(16, bold=True))

    # Details
    draw.text((180, 100), "Name / పేరు:", fill=(80, 80, 80), font=get_font(12))
    draw.text((180, 118), "Sai Praneetha K", fill=(10, 20, 40), font=get_font(16, bold=True))

    draw.text((180, 145), "DOB / పుట్టిన తేదీ:", fill=(80, 80, 80), font=get_font(12))
    draw.text((180, 163), "15/06/2005", fill=(10, 20, 40), font=get_font(15, bold=True))

    draw.text((180, 190), "Gender / లింగం: Female / స్త్రీ", fill=(10, 20, 40), font=get_font(14))

    # Aadhaar Number Banner
    draw.rectangle([10, 260, w - 10, 310], fill=(245, 248, 255))
    draw.text((170, 272), "XXXX  XXXX  8921", fill=(180, 20, 20), font=get_font(22, bold=True))

    draw.text((120, 335), "నా ఆధార్, నా గుర్తింపు | Mera Aadhaar, Meri Pehchan", fill=(50, 60, 70), font=get_font(12))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"Generated Aadhaar card: {output_path}")

def create_sample_income_cert(output_path: str):
    w, h = 650, 850
    img = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.rectangle([15, 15, w - 15, h - 15], outline=(16, 52, 110), width=2)
    draw.rectangle([20, 20, w - 20, 90], fill=(240, 245, 255))

    draw.text((140, 30), "GOVERNMENT OF ANDHRA PRADESH", fill=(16, 52, 110), font=get_font(16, bold=True))
    draw.text((190, 55), "REVENUE DEPARTMENT - MEESEVA", fill=(40, 60, 90), font=get_font(14, bold=True))

    draw.rectangle([120, 110, w - 120, 145], fill=(230, 240, 255))
    draw.text((170, 118), "INCOME CERTIFICATE / ఆదాయ ధ్రువీకరణ పత్రం", fill=(16, 52, 110), font=get_font(14, bold=True))

    draw.text((40, 170), "Certificate No: IC-AP-2026-981245", fill=(30, 40, 60), font=get_font(13, bold=True))
    draw.text((420, 170), "Date: 12/01/2026", fill=(30, 40, 60), font=get_font(13))

    body_text = (
        "This is to certify that Kum. Sai Praneetha D/o Sri K. Venkateshwarlu,\n"
        "residing at Plot 42, Gayatri Nagar, Vijayawada Urban Mandal, Krishna District.\n\n"
        "The total annual income of the applicant's family from all sources is:\n\n"
        "        Rs. 1,80,000/-  (Rupees One Lakh Eighty Thousand Only)\n\n"
        "This certificate is issued for educational scholarship and welfare scheme purposes."
    )
    draw.text((40, 220), body_text, fill=(30, 30, 30), font=get_font(13))

    draw.rectangle([40, 420, 300, 480], outline=(180, 190, 200), fill=(250, 252, 255))
    draw.text((50, 430), "Annual Family Income:", fill=(60, 70, 80), font=get_font(12))
    draw.text((50, 450), "₹ 1,80,000 / year", fill=(16, 52, 110), font=get_font(18, bold=True))

    # Official Seal & Signature
    draw.text((430, 650), "Tahsildar / Authorized Signatory", fill=(20, 30, 50), font=get_font(12, bold=True))
    draw.text((430, 670), "Revenue Department, Vijayawada", fill=(50, 60, 70), font=get_font(11))
    draw.ellipse([450, 560, 550, 640], outline=(20, 60, 150), width=2)
    draw.text((465, 590), "OFFICIAL SEAL\nREVENUE DEPT", fill=(20, 60, 150), font=get_font(10))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG", quality=95)
    print(f"Generated Income certificate: {output_path}")

if __name__ == "__main__":
    base_dir = r"C:\Users\siddi\.gemini\antigravity\scratch\FormSaathi\data\sample_forms"
    create_bank_form(os.path.join(base_dir, "bank_application_form.jpg"))
    create_sample_aadhaar(os.path.join(base_dir, "sample_aadhaar.jpg"))
    create_sample_income_cert(os.path.join(base_dir, "sample_income_cert.jpg"))
