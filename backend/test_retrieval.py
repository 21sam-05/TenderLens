import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from embedding_service import generate_embedding
from retriever import retrieve_chunks


query = "What is the minimum annual turnover required?"

query_embedding = generate_embedding(query)

results = retrieve_chunks(
    query_embedding,
    top_k=3
)

print("\nQuery:", query)

for result in results:
    print("\n" + "=" * 70)
    print("Chunk ID:", result.chunk_id)
    print("Section:", result.section)
    print("Distance:", result.distance)
    print("Text:", result.text)