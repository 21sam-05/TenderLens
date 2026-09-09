from document_processor import extract_and_clean_pdf


pdf_path = "tender.pdf"

pages = extract_and_clean_pdf(pdf_path)

print("Total pages:", len(pages))
print("=" * 60)

for page in pages:
    print("\nPAGE:", page["page"])
    print("DOCUMENT:", page["document_id"])
    print("-" * 60)
    print(page["text"])