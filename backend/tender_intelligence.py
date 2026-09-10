import os
from dotenv import load_dotenv
from google import genai
import json


from tenders.models import Tender, TenderIntelligence

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def build_extraction_prompt(tender_text):
    prompt=f"""

You are an AI system that extracts structured intelligence from tenders.

Analyze the tender text provided below.

Extract ONLY information explicitly present in the tender.

Return the result as valid JSON with exactly these fields:

{{
    "eligibility_requirements": [],
    "financial_requirements": {{}},
    "technical_requirements": [],
    "experience_requirements": [],
    "required_documents": [],
    "deadlines": [],
    "penalties": []
    "project_duration":null,
}}

Rules:

1. Do not invent or assume information.
2. If a category is not present, return an empty array [].
3. For financial_requirements, include explicitly stated financial/commercial values such as bid security, estimated project value, turnover, net worth, or other financial conditions.
4. Preserve important numbers, amounts, dates, percentages, and conditions exactly.
5. Separate financial, technical, experience, and eligibility requirements appropriately.
6. Include all explicitly mentioned required documents.
7. Include deadlines only when explicitly stated.
8. Include penalties only when explicitly stated.
9. Return ONLY valid JSON.
10. Do not include markdown code fences.
11. Do not add explanations outside the JSON.
12. Project duration is not a deadline. Store it separately under project_duration.


Tender Text:

{tender_text}

"""
    return prompt

#get gemini output 
# fucntion that takes the prompt and asks gemini to extract the structured json
def extract_tender_intelligence(tender_text):
    prompt=build_extraction_prompt(tender_text)

    response=client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def parse_tender_intelligence(response_text):

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON.")

    required_fields = [
        "eligibility_requirements",
        "financial_requirements",
        "technical_requirements",
        "experience_requirements",
        "required_documents",
        "deadlines",
        "project_duration",
        "penalties"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Missing required field: {field}"
            )

    return data


def save_tender_intelligence(tender_id, data):

    tender = Tender.objects.get(id=tender_id)

    intelligence, created = TenderIntelligence.objects.update_or_create(
        tender=tender,
        defaults={
            "eligibility_requirements": data["eligibility_requirements"],
            "financial_requirements": data["financial_requirements"],
            "technical_requirements": data["technical_requirements"],
            "experience_requirements": data["experience_requirements"],
            "required_documents": data["required_documents"],
            "deadlines": data["deadlines"],
            "project_duration": data["project_duration"],
            "penalties": data["penalties"],
        }
    )

    return intelligence