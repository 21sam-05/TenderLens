
from chunker import chunk_document
from document_processor import extract_and_clean_pdf
from embedding_service import generate_embedding

from tender_intelligence import (
    extract_tender_intelligence,
    parse_tender_intelligence,
    save_tender_intelligence,
)

from .models import DocumentChunk

from matching_service import match_company_to_tender
from tenders.models import BidReadinessAnalysis
from tenders.bid_analysis_service import generate_bid_analysis


def process_tender_document(tender):
    pdf_path = tender.document.path

    # =========================================
    # 1. EXTRACT AND CLEAN PDF
    # =========================================

    pages = extract_and_clean_pdf(pdf_path)

    total_saved = 0

    # =========================================
    # 2. CREATE CHUNKS + EMBEDDINGS
    # =========================================

    for page in pages:

        chunks = chunk_document(
            document_id=str(tender.id),
            page=page["page"],
            text=page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk in chunks:

            embedding = generate_embedding(
                chunk["text"]
            )

            DocumentChunk.objects.create(
                document_id=chunk["document_id"],
                page=chunk["page"],
                chunk_id=chunk["chunk_id"],
                section=chunk["section"],
                text=chunk["text"],
                embedding=embedding
            )

            total_saved += 1

    # =========================================
    # 3. GENERATE TENDER INTELLIGENCE
    # =========================================

    tender_text = "\n\n".join(
        page["text"]
        for page in pages
        if page.get("text")
    )

    # Stop processing if PDF has no extractable text
    if not tender_text.strip():
        raise ValueError(
            "No extractable text was found in the PDF. "
            "This may be a scanned or image-based PDF."
        )

    response_text = extract_tender_intelligence(
        tender_text
    )

    intelligence_data = parse_tender_intelligence(
        response_text
    )

    save_tender_intelligence(
        tender.id,
        intelligence_data
    )

    # =========================================
    # 4. GENERATE BID READINESS
    # =========================================

    match_company_to_tender(
        user=tender.user,
        tender_id=tender.id
    )

    readiness_analysis = BidReadinessAnalysis.objects.get(
        tender=tender,
        company__user=tender.user
    )

    # =========================================
    # 5. GENERATE BID ANALYSIS
    # =========================================

    generate_bid_analysis(
        readiness_analysis
    )

    return total_saved