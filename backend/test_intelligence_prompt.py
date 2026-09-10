
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from documents.models import DocumentChunk
from tender_intelligence import build_extraction_prompt,extract_tender_intelligence,parse_tender_intelligence


tender_id = 4

chunks = DocumentChunk.objects.filter(
    document_id=str(tender_id)
).order_by("chunk_id")


tender_text = "\n\n".join(
    chunk.text
    for chunk in chunks
)


prompt = build_extraction_prompt(tender_text)

print("\n===== EXTRACTION PROMPT =====\n")
print(prompt)

result = extract_tender_intelligence(tender_text)

data = parse_tender_intelligence(result)

print("\n===== PARSED TENDER INTELLIGENCE =====\n")
print(data)