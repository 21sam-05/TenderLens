from rest_framework import serializers
from .models import Tender
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