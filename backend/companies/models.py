from django.db import models
from django.conf import settings

class CompanyProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_profile"
    )
    company_name=models.CharField(max_length=255)
    industry=models.CharField(max_length=100,blank=True)
    description=models.TextField(blank=True)
    website=models.URLField(blank=True)

    annual_turnover=models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )
    years_of_experience = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    similar_projects_count = models.PositiveIntegerField(
        default=0
    )

    has_construction_license = models.BooleanField(
        default=False
    )

    has_tax_registration = models.BooleanField(
        default=False
    )

    


