from datetime import datetime
import re
from django.utils import timezone


def parse_deadline(deadlines):
    if not deadlines:
        return None

    for deadline in deadlines:
        match = re.search(
            r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4}),\s*(\d{1,2}):(\d{2})\s*(AM|PM)?\s*IST",
            deadline,
            re.IGNORECASE
        )

        if not match:
            continue

        day = int(match.group(1))
        month = match.group(2)
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        meridiem = match.group(6)

        if meridiem:
            meridiem = meridiem.upper()

            if meridiem == "PM" and hour != 12:
                hour += 12
            elif meridiem == "AM" and hour == 12:
                hour = 0

        try:
            deadline_date = datetime.strptime(
                f"{day} {month} {year} {hour}:{minute}",
                "%d %B %Y %H:%M"
            )

            return timezone.make_aware(
                deadline_date,
                timezone.get_current_timezone()
            )

        except ValueError:
            continue

    return None


def calculate_deadline_risk(deadline):
    if not deadline:
        return {
            "level": "Unknown",
            "days_remaining": None,
            "message": "Submission deadline could not be determined."
        }

    now = timezone.now()
    remaining = deadline - now
    days_remaining = remaining.total_seconds() / 86400

    if days_remaining < 0:
        return {
            "level": "Expired",
            "days_remaining": 0,
            "message": "The tender submission deadline has passed."
        }

    if days_remaining <= 7:
        level = "Critical"
    elif days_remaining <= 14:
        level = "High"
    elif days_remaining <= 30:
        level = "Medium"
    else:
        level = "Low"

    return {
        "level": level,
        "days_remaining": round(days_remaining, 1),
        "message": f"{round(days_remaining, 1)} days remaining until submission."
    }


def calculate_risk(intelligence):
    deadlines = intelligence.get("deadlines", [])
    required_documents = intelligence.get("required_documents", [])
    penalties = intelligence.get("penalties", [])
    eligibility = intelligence.get("eligibility_requirements", [])

    deadline = parse_deadline(deadlines)
    deadline_risk = calculate_deadline_risk(deadline)

    risks = []

    if deadline_risk["level"] in ["Critical", "High"]:
        risks.append({
            "type": "Deadline",
            "level": deadline_risk["level"],
            "message": deadline_risk["message"]
        })

    if len(required_documents) >= 7:
        risks.append({
            "type": "Documentation",
            "level": "Medium",
            "message": f"{len(required_documents)} documents are required for submission."
        })

    if penalties:
        risks.append({
            "type": "Penalties",
            "level": "High",
            "message": f"{len(penalties)} penalty condition(s) are specified in the tender."
        })

    if len(eligibility) >= 2:
        risks.append({
            "type": "Eligibility",
            "level": "Medium",
            "message": f"{len(eligibility)} eligibility conditions must be satisfied."
        })

    if not risks:
        overall_level = "Low"
    elif any(risk["level"] == "Critical" for risk in risks):
        overall_level = "Critical"
    elif any(risk["level"] == "High" for risk in risks):
        overall_level = "High"
    elif any(risk["level"] == "Medium" for risk in risks):
        overall_level = "Medium"
    else:
        overall_level = "Low"

    return {
        "overall_risk": overall_level,
        "deadline": {
            "date": deadline.isoformat() if deadline else None,
            **deadline_risk
        },
        "risks": risks
    }