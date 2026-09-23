import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_text_from_image(image_bytes):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": "image/png",
                    "data": image_bytes
                }
            },
            """
            Extract all readable text from this document image.

            Preserve the wording and structure as accurately as possible.
            Do not summarize.
            Do not explain anything.
            Return only the extracted text.
            """
        ]
    )

    return response.text