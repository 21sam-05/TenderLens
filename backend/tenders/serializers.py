from rest_framework import serializers
from .models import Tender,TenderIntelligence

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tender
        fields=[
            "id","title",
            "description",
            "deadline",
            "document",
            "created_at",
        ]

class TenderQuestionSerializer(serializers.Serializer):
    question=serializers.CharField(
        required=True,
        allow_blank=False
    )

class TenderIntelligenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=TenderIntelligence
        fields=[
             "eligibility_requirements",
            "financial_requirements",
            "technical_requirements",
            "experience_requirements",
            "required_documents",
            "deadlines",
            "project_duration",
            "penalties",
            "created_at",
            "updated_at",
        ]
        