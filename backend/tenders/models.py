from django.db import models
from django.conf import settings

class Tender(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tenders"
    )

    title=models.CharField(max_length=255)
    description=models.TextField(blank=True)
    deadline=models.DateTimeField(null=True,blank=True)
    document=models.FileField(
        upload_to="tenders/",
        blank=True,
        null=True
    )
    created_at=models.DateTimeField(auto_now_add=True)

class TenderIntelligence(models.Model):
    tender=models.OneToOneField(
        Tender,
        on_delete=models.CASCADE,
        related_name="Intelligence"
    )

    eligibility_requirements = models.JSONField(default=list)

    financial_requirements = models.JSONField(default=dict)

    technical_requirements = models.JSONField(default=list)

    experience_requirements = models.JSONField(default=list)

    required_documents = models.JSONField(default=list)

    deadlines = models.JSONField(default=list)

    penalties = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    project_duration = models.JSONField(
    default=list,
    null=True,
    blank=True
)


class BidReadinessAnalysis(models.Model):
    tender=models.ForeignKey(
        Tender,
        on_delete=models.CASCADE,
        related_name="bid_Readiness_analyses"
    )

    matched_requirements=models.JSONField(default=list)

    missing_requirements=models.JSONField(default=list)

    critical_missing_requirements = models.JSONField(default=list)

    score = models.PositiveIntegerField()

    readiness = models.CharField(
        max_length=20
    )

    bid_ready = models.BooleanField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    company = models.ForeignKey(
    "companies.CompanyProfile",
        on_delete=models.CASCADE,
        related_name="bid_readiness_analyses",
        
)

