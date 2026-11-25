"""
FormSaathi Form Overlay Engine.
Renders user answers and validated document data onto the original physical form image,
preserving 100% of the original document layout, typography, borders, and official appearance.
Explicitly reserves signature/photo boxes for physical completion (no fake signatures).
"""
import os
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Any, List

class FormOverlayEngine:
    def __init__(self):
        pass

    def get_font(self, size: int = 18):
        """Loads default or system truetype font."""
        try:
            # On Windows, try Arial or Segoe UI
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            try:
                return ImageFont.truetype("DejaVuSans.ttf", size)
            except Exception:
                return ImageFont.load_default()

    def overlay_form(
        self,
        base_image_path: str,
        output_image_path: str,
        fields_schema: List[Dict[str, Any]],
        form_data: Dict[str, Any]
    ) -> str:
        """
        Overlays collected values onto the original form image.
        Returns the path to the saved filled form image.
        """
        if not os.path.exists(base_image_path):
            raise FileNotFoundError(f"Base form image not found at {base_image_path}")

        img = Image.open(base_image_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        text_font = self.get_font(18)
        notice_font = self.get_font(14)
        bold_font = self.get_font(20)

        # Realistic dark navy blue ballpoint ink color for filled fields
        ink_color = (20, 50, 130)
        warning_color = (180, 40, 40)
        notice_bg = (255, 248, 230)

        for field in fields_schema:
            field_id = field.get("id") or field.get("name")
            field_type = field.get("type", "text")
            x = field.get("x", 260)
            y = field.get("y", 200)
            w = field.get("width", 300)
            h = field.get("height", 30)

            # Check if this is a manual field (Signature, Photo, Thumb)
            if field_type in ["signature", "photo"] or "manual_notice" in field:
                notice = field.get("manual_notice", "✍ Complete manually upon printing")
                # Draw subtle dashed/highlighted box
                draw.rectangle([x, y, x + w, y + h], outline=warning_color, width=2)
                # Draw clean manual sign banner inside
                draw.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], fill=notice_bg)
                draw.text((x + 8, y + (h // 4)), notice, fill=warning_color, font=notice_font)
                continue

            val = form_data.get(field_id)
            if val is not None and str(val).strip() != "":
                text_to_draw = str(val).strip()

                # Handle multi-line address or textarea
                if field_type == "textarea" or len(text_to_draw) > 45:
                    lines = []
                    words = text_to_draw.split()
                    curr_line = ""
                    for word in words:
                        if len(curr_line + " " + word) < 40:
                            curr_line = (curr_line + " " + word).strip()
                        else:
                            lines.append(curr_line)
                            curr_line = word
                    if curr_line:
                        lines.append(curr_line)

                    for i, line in enumerate(lines[:3]): # max 3 lines
                        draw.text((x + 5, y + 3 + (i * 20)), line, fill=ink_color, font=text_font)
                else:
                    # Clean single line text or checkmark
                    if text_to_draw.lower() in ["yes", "true", "y"]:
                        draw.text((x + 5, y + 4), "✓ YES", fill=ink_color, font=bold_font)
                    elif text_to_draw.lower() in ["no", "false", "n"]:
                        draw.text((x + 5, y + 4), "✗ NO", fill=ink_color, font=bold_font)
                    else:
                        draw.text((x + 5, y + 4), text_to_draw, fill=ink_color, font=text_font)

        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        img.save(output_image_path, "JPEG", quality=95)
        return output_image_path

form_overlay_engine = FormOverlayEngine()
