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

    


