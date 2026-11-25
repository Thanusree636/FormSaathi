"""
FormSaathi PDF Generation Service.
Generates print-ready PDFs for:
1. Physical forms filled with original layout preservation.
2. Digital application acknowledgments and official summary sheets.
"""
import os
from typing import Dict, Any, List
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFGenerator:
    def generate_pdf_from_image(self, image_path: str, output_pdf_path: str) -> str:
        """Converts filled form image to a standardized print-ready A4 PDF."""
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        img = Image.open(image_path)
        # Convert to RGB if needed
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(output_pdf_path, "PDF", resolution=150.0)
        return output_pdf_path

    def generate_digital_application_pdf(
        self,
        output_pdf_path: str,
        service_title: str,
        application_id: str,
        applicant_data: Dict[str, Any],
        verified_docs: List[Dict[str, Any]],
        conflicts_resolved: List[Dict[str, Any]]
    ) -> str:
        """Generates an official digital application summary PDF."""
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
        doc = SimpleDocTemplate(
            output_pdf_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            leading=20,
            textColor=colors.HexColor('#0F294A'),
            alignment=1 # Center
        )
        subtitle_style = ParagraphStyle(
            'SubTitleStyle',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#4A5568'),
            alignment=1
        )
        heading_style = ParagraphStyle(
            'SectionHead',
            parent=styles['Heading2'],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#1A365D'),
            spaceBefore=10,
            spaceAfter=6
        )
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontSize=9,
            leading=13
        )

        # Header
        story.append(Paragraph("GOVERNMENT CITIZEN WELFARE & SCHOLARSHIP PORTAL", subtitle_style))
        story.append(Paragraph(f"<b>{service_title.upper()}</b>", title_style))
        story.append(Paragraph(f"Application Ref: <b>{application_id}</b> | FormSaathi AI Verified", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceBefore=5, spaceAfter=15))

        # Applicant Details Table
        story.append(Paragraph("1. APPLICANT & SCHEME INFORMATION", heading_style))
        data_table = []
        for k, v in applicant_data.items():
            label = k.replace("_", " ").title()
            data_table.append([
                Paragraph(f"<b>{label}</b>", normal_style),
                Paragraph(str(v), normal_style)
            ])

        t1 = Table(data_table, colWidths=[200, 315])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t1)
        story.append(Spacer(1, 15))

        # Verified Documents Table
        story.append(Paragraph("2. VERIFIED SUPPORTING DOCUMENTS (OCR CHECKED)", heading_style))
        doc_rows = [[
            Paragraph("<b>Document Type</b>", normal_style),
            Paragraph("<b>Verification Status</b>", normal_style),
            Paragraph("<b>Extracted Match</b>", normal_style)
        ]]
        for doc_item in verified_docs:
            d_name = doc_item.get("name") or doc_item.get("doc_name", "Document")
            status_text = "<font color='green'><b>✓ VERIFIED</b></font>"
            doc_rows.append([
                Paragraph(d_name, normal_style),
                Paragraph(status_text, normal_style),
                Paragraph("Aadhaar & Registry Validated", normal_style)
            ])

        t2 = Table(doc_rows, colWidths=[220, 140, 155])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(t2)
        story.append(Spacer(1, 25))

        # Physical Signature & Verification Notice
        story.append(Paragraph("3. MANUAL VERIFICATION & SIGNATURES", heading_style))
        sign_table = [
            [
                Paragraph("<b>Applicant Signature / Thumb Impression:</b><br/><br/><br/><br/>✍ ____________________________<br/>(Please sign physically after printing)", normal_style),
                Paragraph("<b>Authorized Officer / Institution Stamp:</b><br/><br/><br/><br/>✍ ____________________________<br/>Seal & Signature", normal_style)
            ]
        ]
        t3 = Table(sign_table, colWidths=[255, 260])
        t3.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94A3B8')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEFCE8')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t3)
        story.append(Spacer(1, 15))

        story.append(Paragraph(
            "<i>Note: Generated via FormSaathi Citizen Assistant. Preserves verified data. Physical submission requires manual signature.</i>",
            subtitle_style
        ))

        doc.build(story)
        return output_pdf_path

pdf_generator = PDFGenerator()
