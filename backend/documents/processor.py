from chunker import chunk_document
from document_processor import extract_and_clean_pdf
from embedding_service import generate_embedding

from .models import DocumentChunk


def process_tender_document(tender):
    pdf_path = tender.document.path

    pages = extract_and_clean_pdf(pdf_path)

    total_saved = 0

    for page in pages:

        chunks = chunk_document(
            document_id=str(tender.id),
            page=page["page"],
            text=page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk in chunks:

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

    return total_saved