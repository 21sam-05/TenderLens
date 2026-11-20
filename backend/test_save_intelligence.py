import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from documents.models import DocumentChunk
from tender_intelligence import (
    extract_tender_intelligence,
    parse_tender_intelligence,
    save_tender_intelligence
)


tender_id = 4

chunks = DocumentChunk.objects.filter(
    document_id=str(tender_id)
).order_by("chunk_id")

tender_text = "\n\n".join(
    chunk.text
    for chunk in chunks
)

raw_result = extract_tender_intelligence(tender_text)

data = parse_tender_intelligence(raw_result)

intelligence = save_tender_intelligence(
    tender_id=tender_id,
    data=data
)

print("\n===== SAVED INTELLIGENCE =====\n")
print("Tender:", intelligence.tender.id)
print("Financial:", intelligence.financial_requirements)
print("Documents:", intelligence.required_documents)
print("Deadline:", intelligence.deadlines)
print("Project Duration:", intelligence.project_duration)