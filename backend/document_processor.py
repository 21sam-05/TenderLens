import re

import pymupdf

from ocr_service import extract_text_from_image


def clean_text(text):

    if not text:
        return ""

    text = text.strip()

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text


def extract_and_clean_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        # =========================================
        # 1. TRY NORMAL TEXT EXTRACTION
        # =========================================

        raw_text = page.get_text()
        cleaned_text = clean_text(raw_text)

        # =========================================
        # 2. OCR FALLBACK
        # =========================================

        if not cleaned_text:

            pix = page.get_pixmap(
                matrix=pymupdf.Matrix(2, 2)
            )

            image_bytes = pix.tobytes("png")

            ocr_text = extract_text_from_image(
                image_bytes
            )

            cleaned_text = clean_text(
                ocr_text
            )

        page_data = {
            "document_id": pdf_path,
            "page": page_number,
            "text": cleaned_text
        }

        pages.append(page_data)

    document.close()

    return pages