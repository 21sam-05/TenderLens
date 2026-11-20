
from .models import BidAnalysis


def generate_bid_analysis(readiness_analysis):

    critical_blockers = readiness_analysis.critical_missing_requirements
    missing_requirements = readiness_analysis.missing_requirements
    matched_requirements = readiness_analysis.matched_requirements

    if critical_blockers:
        recommendation = "DO_NOT_BID"

    elif readiness_analysis.score >= 80:
        recommendation = "BID"

    else:
        recommendation = "BID_WITH_CAUTION"

    strengths = []

    for requirement in matched_requirements:
        strengths.append(requirement)

    priority_actions = []

    for requirement in missing_requirements:
        priority_actions.append(
            f"Resolve missing requirement: {requirement}"
        )

    if critical_blockers:
        summary = (
            "The company has one or more critical missing requirements "
            "that may prevent bidding."
        )

    elif readiness_analysis.score >= 80:
        summary = (
            "The company satisfies the major tender requirements "
            "and appears well positioned to bid."
        )

    else:
        summary = (
            "The company meets several tender requirements but "
            "some gaps should be addressed before bidding."
        )

    bid_analysis, created = BidAnalysis.objects.update_or_create(
        tender=readiness_analysis.tender,
        company=readiness_analysis.company,
        defaults={
            "recommendation": recommendation,
            "summary": summary,
            "critical_blockers": critical_blockers,
            "priority_actions": priority_actions,
            "strengths": strengths,
        }
    )

    return bid_analysis