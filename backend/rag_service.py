from embedding_service import generate_embedding
from retriever import retrieve_chunks
from generation_service import generate_answer


def build_context(chunks):
    context_parts=[]

    for chunk in chunks:
        context_parts.append(
            f"""
Page:{chunk.page}
Section:{chunk.section}

{chunk.text}
"""
        )

    return "\n---\n".join(context_parts)

def answer_question(question, tender_id, top_k=5):

    if not question or not question.strip():
        return{
            "answer":"please provide a question",
            "sources":[]
        }
    query_embedding = generate_embedding(question)

    chunks = retrieve_chunks(
        query_embedding=query_embedding,
        document_id=tender_id,
        top_k=top_k
    )

    if not chunks:
        return{
            "answer":"I could not find relevant information in the provided tender",
            "sources":[]
        }

    context = build_context(chunks)

    answer = generate_answer(
        question=question,
        context=context
    )

    sources=[]

    for chunk in chunks:
        sources.append({
            "page":chunk.page,
            "section":chunk.section,
            "chunk_id":chunk.chunk_id
        })

    return {
        "answer":answer,
        "sources":sources
    }

