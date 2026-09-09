import re
import pymupdf

def clean_text(text):
    text=text.strip()
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text

def extract_and_clean_pdf(pdf_path):
    document=pymupdf.open(pdf_path)

    pages=[]

    for page_number,page in enumerate(document,start=1):
        raw_text=page.get_text()
        cleaned_text=clean_text(raw_text)

        page_data={
            "document_id":pdf_path,
            "page":page_number,
            "text":cleaned_text
        }

        pages.append(page_data)

    document.close()

    return pages
