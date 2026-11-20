import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()

from django.contrib.auth import get_user_model
from matching_service import match_company_to_tender


User = get_user_model()

user = User.objects.first()

result = match_company_to_tender(
    user=user,
    tender_id=4
)

print("\n===== DATABASE MATCH RESULT =====\n")
print(result)