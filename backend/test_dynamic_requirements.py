import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


from matching_service import (
    check_license_requirement,
    check_tax_requirement,
    parse_project_requirement,
)


requirements = [
    "Must be legally registered entities",
    "Must have valid tax registration",
]

experience_requirements = [
    "2 similar completed projects in the last 5 years",
]


print(
    "License required:",
    check_license_requirement(requirements)
)

print(
    "Tax required:",
    check_tax_requirement(requirements)
)

print(
    "Projects required:",
    parse_project_requirement(
        experience_requirements[0]
    )
)