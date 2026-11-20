from rest_framework import serializers
from .models import CompanyProfile

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyProfile
        fields = [
        "company_name",
        "industry",
        "description",
        "website",
        "annual_turnover",
        "years_of_experience",
        "similar_projects_count",
        "has_construction_license",
        "has_tax_registration",
]