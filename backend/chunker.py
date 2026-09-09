import re
from document_processor import extract_and_clean_pdf

def split_into_sections(text):
    """
    Split tender text into numbered sections.

    Example:
        1. Scope of Work
        2. Key Requirements
        3. Eligibility Criteria
    """

    pattern = r"(?m)^(?P<section>\d+\.\s+[^\n]+)$"

    matches = list(re.finditer(pattern, text))

    # No numbered sections found
    if not matches:
        return [
            {
                "section": None,
                "text": text.strip()
            }
        ]

    sections = []

    # Text before the first numbered section
    if matches[0].start() > 0:
        intro = text[:matches[0].start()].strip()

        if intro:
            sections.append({
                "section": None,
                "text": intro
            })

    # Extract each section
    for i, match in enumerate(matches):

        section_name = match.group("section").strip()

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        if section_text:
            sections.append({
                "section": section_name,
                "text": section_text
            })

    return sections


def find_boundary(text, start, end):
    """
    Find the best natural boundary before 'end'.

    Priority:
        1. Paragraph boundary
        2. Sentence boundary
        3. Newline
        4. Hard character boundary
    """

    # Paragraph boundary
    boundary = text.rfind("\n\n", start, end)

    if boundary > start:
        return boundary + 2

    # Sentence boundary
    sentence_endings = [".", "?", "!"]

    best_boundary = -1

    for punctuation in sentence_endings:
        position = text.rfind(punctuation, start, end)

        if position > best_boundary:
            best_boundary = position

    if best_boundary > start:
        return best_boundary + 1

    # Newline boundary
    boundary = text.rfind("\n", start, end)

    if boundary > start:
        return boundary + 1

    # No natural boundary found
    return end


def chunk_section(text, chunk_size=500, overlap=100):
    """
    Split one section into overlapping chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        # If remaining text fits in one chunk
        if len(text) - start <= chunk_size:
            chunk = text[start:].strip()

            if chunk:
                chunks.append(chunk)

            break

        # Approximate end
        end = start + chunk_size

        # Find a natural boundary
        end = find_boundary(text, start, end)

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Move forward while maintaining overlap
        next_start = end - overlap

        # Safety check
        if next_start <= start:
            next_start = end

        start = next_start

    return chunks


def chunk_document(
    document_id,
    page,
    text,
    chunk_size=500,
    overlap=100
):
    """
    Complete TenderLens chunking pipeline.

    Input:
        document_id
        page
        cleaned text

    Output:
        List of chunks with metadata.
    """

    sections = split_into_sections(text)

    final_chunks = []

    chunk_id = 0

    for section in sections:

        section_name = section["section"]
        section_text = section["text"]

        chunks = chunk_section(
            section_text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in chunks:

            final_chunks.append({
                "document_id": document_id,
                "page": page,
                "chunk_id": chunk_id,
                "section": section_name,
                "text": chunk
            })

            chunk_id += 1

    return final_chunks

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


print("Total chunks:", len(all_chunks))

for chunk in all_chunks:

    print("\n" + "=" * 70)

    print("Document ID:", chunk["document_id"])
    print("Page:", chunk["page"])
    print("Chunk ID:", chunk["chunk_id"])
    print("Section:", chunk["section"])

    print("-" * 70)

    print(chunk["text"])