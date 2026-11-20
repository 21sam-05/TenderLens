
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from embedding_service import generate_embedding
from retriever import retrieve_chunks
from rag_service import build_context

question = "How much revenue must a bidder have to qualify financially?"

tender_id=4

query_embedding=generate_embedding(question)

chunks=retrieve_chunks(query_embedding=query_embedding,
                      document_id=tender_id,
                      top_k=3)

context=build_context(chunks)

print("\n===== RETRIEVED CONTEXT =====\n")

for chunk in chunks:
    print("Page:", chunk.page)
    print("Section:", chunk.section)
    print("Distance:", chunk.distance)
    print("Text:", chunk.text)
    print("\n----------------------\n")

