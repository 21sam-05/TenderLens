import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from tenders.models import Tender, TenderIntelligence
from companies.models import CompanyProfile
from matching_service import match_company_to_tender


company = CompanyProfile.objects.first()

tender = Tender.objects.create(
    user=company.user,
    title="Dynamic Requirement Test Tender"
)

TenderIntelligence.objects.create(
    tender=tender,

    eligibility_requirements=[
        "Must be legally registered entities",
        "Must have valid tax registration"
    ],

    financial_requirements={
        "average_annual_turnover": "At least INR 2 Crore"
    },

    technical_requirements=[],

    experience_requirements=[
        "2 similar completed projects in the last 5 years"
    ],

    required_documents=[],

    deadlines=[],

    project_duration=None,

    penalties=[]
)


result = match_company_to_tender(
    user=company.user,
    tender_id=tender.id,
    
)

print("\n===== DYNAMIC MATCH RESULT =====")
print(result)