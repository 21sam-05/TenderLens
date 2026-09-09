import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_answer(question,context):
    prompt=f"""

You are an AI assistant for a tender analysis system.

Answer the user's question using ONLY the tender context provided below.

If the answer cannot be found in the context,say:
"I could not find this information in the provided tender ."

Tender Context:
{context}

User Question:
{question}

"""
    response=client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


