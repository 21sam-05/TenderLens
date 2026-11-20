from document_processor import extract_and_clean_pdf
from chunker import chunk_document
from embedding_service import generate_embedding


pdf_path = "tender.pdf"

pages = extract_and_clean_pdf(pdf_path)

all_chunks = []

for page in pages:
    chunks = chunk_document(
        document_id=page["document_id"],
        page=page["page"],
        text=page["text"],
        chunk_size=500,
        overlap=100
    )

    all_chunks.extend(chunks)


# Generate embeddings
for chunk in all_chunks:
    chunk["embedding"] = generate_embedding(chunk["text"])


print("Total chunks:", len(all_chunks))

for chunk in all_chunks:
    print("\n" + "=" * 70)
    print("Chunk ID:", chunk["chunk_id"])
    print("Page:", chunk["page"])
    print("Section:", chunk["section"])
    print("Embedding dimensions:", len(chunk["embedding"]))
    print("Text:", chunk["text"][:150])