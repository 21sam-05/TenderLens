from django.db import models
from pgvector.django import VectorField

class DocumentChunk(models.Model):
    document_id=models.CharField(max_length=255)

    page=models.PositiveIntegerField()
    chunk_id=models.PositiveIntegerField()
    section=models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    text=models.TextField()

    embedding=VectorField(

        dimensions=3072
    )
    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.document_id} - Chunk {self.chunk_id}"
