import pymupdf

pdf_path = "tender.pdf"

document = pymupdf.open(pdf_path)

print("Document ID:", pdf_path)
print("Total Pages:", len(document))
print("=" * 60)

for page_number, page in enumerate(document, start=1):

    text = page.get_text()
    

    metadata = {
        "document_id": pdf_path,
        "page": page_number,
        "text": text
    }

    print(f"\nPAGE {page_number}")
    print("-" * 60)
    print("Document ID:", metadata["document_id"])
    print("Page:", metadata["page"])
    print("Text:")
    print(metadata["text"])
    print(repr(text))

document.close()