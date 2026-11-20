from document_processor import extract_and_clean_pdf
from chunker import chunk_document
from embedding_service import generate_embedding
from similarity import cosine_similarity


pdf_path = "tender.pdf"


# Extract and chunk the tender
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


# Generate embeddings for chunks
for chunk in all_chunks:
    chunk["embedding"] = generate_embedding(chunk["text"])


# User's question
query = "What is the minimum annual turnover required?"

query_embedding = generate_embedding(query)


# Calculate similarity
for chunk in all_chunks:
    score = cosine_similarity(
        query_embedding,
        chunk["embedding"]
    )

    chunk["similarity"] = score


# Sort by similarity
all_chunks.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


# Show top 3
print("\nTOP 3 RELEVANT CHUNKS\n")

for chunk in all_chunks[:3]:
    print("=" * 70)
    print("Similarity:", chunk["similarity"])
    print("Section:", chunk["section"])
    print("Page:", chunk["page"])
    print("Text:")
    print(chunk["text"])