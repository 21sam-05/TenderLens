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

# Create your models here.
