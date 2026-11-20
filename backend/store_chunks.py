

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from document_processor import extract_and_clean_pdf
from chunker import chunk_document
from embedding_service import generate_embedding
from documents.models import DocumentChunk


pdf_path = "tender.pdf"

pages = extract_and_clean_pdf(pdf_path)

total_saved = 0
total_skipped = 0

for page in pages:

    chunks = chunk_document(
        document_id=page["document_id"],
        page=page["page"],
        text=page["text"],
        chunk_size=500,
        overlap=100
    )

    for chunk in chunks:

        existing_chunk = DocumentChunk.objects.filter(
            document_id=chunk["document_id"],
            page=chunk["page"],
            chunk_id=chunk["chunk_id"]
        ).first()

        if existing_chunk:
            total_skipped += 1
            continue

        embedding = generate_embedding(chunk["text"])

        DocumentChunk.objects.create(
            document_id=chunk["document_id"],
            page=chunk["page"],
            chunk_id=chunk["chunk_id"],
            section=chunk["section"],
            text=chunk["text"],
            embedding=embedding
        )

        total_saved += 1

        print(
            f"Saved chunk {chunk['chunk_id']} "
            f"from page {chunk['page']}"
        )


print("\nDone!")
print("Chunks saved:", total_saved)
print("Chunks skipped:", total_skipped)