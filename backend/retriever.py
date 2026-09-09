from documents.models import DocumentChunk
from pgvector.django import CosineDistance


def retrieve_chunks(query_embedding, document_id, top_k=3):
    results = (
        DocumentChunk.objects
        .filter(document_id=str(document_id))
        .annotate(
            distance=CosineDistance(
                "embedding",
                query_embedding
            )
        )
        .order_by("distance")[:top_k]
    )

    return results