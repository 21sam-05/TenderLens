import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def rewrite_question(question, history=None):

    if not history:
        return question.strip()

    conversation_text = ""

    for message in history[-6:]:
        role = message.get("role", "")
        content = message.get("content", "")

        if role and content:
            conversation_text += f"{role.upper()}: {content}\n"

    prompt = f"""
You are a query rewriting component for a tender document search system.

Rewrite the user's latest question into a standalone search query.

Use the conversation history only to resolve references such as:
- it
- that
- this
- that requirement
- what about it
- what about experience

Rules:

1. Do NOT answer the question.
2. Return ONLY the rewritten standalone question.
3. Preserve the user's intended meaning.
4. Use relevant terms from the conversation when necessary.
5. If the question is already standalone, return it unchanged.
6. Do not invent requirements or facts.

Previous Conversation:
{conversation_text}

Latest User Question:
{question}

Standalone Search Query:
"""

    response=client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    rewritten_question = response.text.strip()

    if not rewritten_question:
        return question.strip()

    return rewritten_question


def generate_answer(question, context, history=None):

    if history is None:
        history = []

    conversation_text = ""

    for message in history[-6:]:
        role = message.get("role", "")
        content = message.get("content", "")

        if role and content:
            conversation_text += f"{role.upper()}: {content}\n"

    prompt = f"""
You are TenderLens, an AI tender intelligence assistant.

Your job is to help a contractor understand the current tender accurately
and practically.

You have access to:
1. The current user question
2. Previous conversation messages
3. Retrieved tender document context

RULES:

1. Answer using the tender context as the factual source of truth.
2. Use conversation history to understand references such as:
   "it", "that", "this requirement", "what about experience", etc.
3. Never invent tender requirements, values, dates, documents, penalties,
   eligibility conditions, or company information.
4. Preserve exact numbers, currency values, percentages, dates, durations,
   thresholds, and conditions from the tender.
5. If the requested information cannot be determined from the tender context,
   say clearly that the information is not available in the provided tender.
6. If the user asks a follow-up question, answer it in the context of the
   previous conversation rather than treating it as an unrelated question.
7. If the question asks for multiple requirements, use bullet points.
8. If the question asks about one requirement, answer directly first.
9. Do not claim that the company is eligible or ineligible unless company
   information is explicitly available.
10. Do not use general knowledge to fill missing tender information.
11. Keep the answer professional and easy for a contractor to understand.
12. Do not repeat the entire tender context.
13. If previous conversation conflicts with the retrieved tender context,
    trust the retrieved tender context.

Previous Conversation:
{conversation_text}

Current Question:
{question}

Retrieved Tender Context:
{context}

Answer the current question using the conversation history only to understand
context and the retrieved tender content as the factual source.
"""


    response=client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()


