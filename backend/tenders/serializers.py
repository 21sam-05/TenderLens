from rest_framework import serializers
from .models import Tender,TenderIntelligence,BidReadinessAnalysis,BidAnalysis

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
    history=serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
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

class BidReadinessAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = BidReadinessAnalysis
        fields = [
            "tender",
            "company",
            "matched_requirements",
            "missing_requirements",
            "critical_missing_requirements",
            "score",
            "readiness",
            "bid_ready",
            "created_at",
            "updated_at",
        ]   

class BidAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = BidAnalysis
        fields = [
            "tender",
            "company",
            "recommendation",
            "summary",
            "critical_blockers",
            "priority_actions",
            "strengths",
            "created_at",
            "updated_at",
        ]