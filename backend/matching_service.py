import re
from decimal import Decimal
from companies.models import CompanyProfile
from tenders.models import TenderIntelligence
from tenders.models import BidReadinessAnalysis

def check_turnover_requirement(
        company_turnover,
        required_turnover
):
    if company_turnover is None:
        return False

    if required_turnover is None:
        return None

    return company_turnover>=required_turnover

def parse_turnover_requirement(text):

    if not text:
        return None

    text = text.lower().replace(",", "").strip()

    crore_match = re.search(
        r"([\d.]+)\s*crore",
        text
    )

    if crore_match:
        crore_value=Decimal(crore_match.group(1))
        return crore_value*Decimal("10000000")

    lakh_match = re.search(
        r"([\d.]+)\s*lakh",
        text
    )

    if lakh_match:
        lakh_value = Decimal(lakh_match.group(1))
        return lakh_value * Decimal("100000")

    return None

def check_similar_projects(
    company_projects,
    required_projects
):
    if company_projects is None:
        return False

    if required_projects is None:
        return None

    return company_projects >= required_projects


def check_construction_license(
    company_has_license,
    required
):
    if not required:
        return None

    return company_has_license is True


def check_tax_registration(
    company_has_tax_registration,
    required
):
    if not required:
        return None

    return company_has_tax_registration is True



def analyze_tender_match(
    company_turnover,
    required_turnover,
    company_projects,
    required_projects,
    company_has_license,
    requires_license,
    company_has_tax,
    requires_tax
):
    results = []

    weights={
        "Annual turnover":30,
        "Similar project experience":30,
        "Construction license":25,
        "Tax registration":15
    }

    turnover_result = check_turnover_requirement(
        company_turnover,
        required_turnover
    )
    if turnover_result is True:
        turnover_status="matched"
    elif turnover_result is False:
        turnover_status="missing"
    else:
        turnover_status="needs_verification"


    results.append({
        "requirement": "Annual turnover",
        "status": turnover_status,
        "critical":True
    })

    projects_result = check_similar_projects(
        company_projects,
        required_projects
    )

    if projects_result is True:
        projects_status = "matched"
    elif projects_result is False:
        projects_status = "missing"
    else:
        projects_status = "needs_verification"

    results.append({
    "requirement": "Similar project experience",
    "status": projects_status,
    "critical":True

    })

    license_result = check_construction_license(
        company_has_license,
        requires_license
    )

    if license_result is not None:

        if license_result is True:
            license_status = "matched"
        elif license_result is False:
            license_status = "missing"
        else:
            license_status = "needs_verification"

        results.append({
        "requirement": "Construction license",
        "status": license_status,
        "critical":True
        })

    tax_result = check_tax_registration(
        company_has_tax,
        requires_tax
    )

    if tax_result is not None:
        if tax_result is True:
            tax_status = "matched"
        elif tax_result is False:
            tax_status = "missing"
        else:
            tax_status = "needs_verification"

        results.append({
        "requirement": "Tax registration",
        "status": tax_status,
        "critical":True
        })

    matched = [
        result
        for result in results
        if result["status"] == "matched"
    ]

    missing = [
        result
        for result in results
        if result["status"] == "missing"
    ]

    critical_missing=[
        result
        for result in missing
        if result["critical"] is True
    ]

    total_applicable_weight = 0
    matched_weight = 0

    for result in results:

        total_applicable_weight += weights[result["requirement"]]

        if result["status"] == "matched":
            matched_weight += weights[result["requirement"]]

        if total_applicable_weight > 0:
            score = round(
            (matched_weight / total_applicable_weight) * 100
                )
        else:
            score = 0

    if score>=80:
        readiness="High"
    elif score>=60:
        readiness="Moderate"
    else:
        readiness="Low"

    bid_ready=len(critical_missing)==0

    return {
        "matched_requirements": matched,
        "missing_requirements": missing,
        "score": score,
        "readiness":readiness,
        "critical_missing_requirements":critical_missing,
        "bid_ready":bid_ready
    }


def match_company_to_tender(user,tender_id):
    company=CompanyProfile.objects.get(
        user=user
    )

    intelligence=TenderIntelligence.objects.get(
        tender_id=tender_id

    )

    required_turnover_text=(
        intelligence.financial_requirements.get("average_annual_turnover")

    )

    required_turnover=parse_turnover_requirement(
        required_turnover_text
    )
    required_projects=None

    for requirement in intelligence.experience_requirements:
        parsed_projects=parse_project_requirement(requirement)

        if parsed_projects is not None:
            required_projects=parsed_projects

            break

    requires_llicense=check_license_requirement(intelligence.eligibility_requirements)
    requires_tax = check_tax_requirement(
    intelligence.eligibility_requirements
)


    result=analyze_tender_match(
        company_turnover=company.annual_turnover,
        required_turnover=required_turnover,

        company_projects=company.similar_projects_count,
        required_projects=required_projects,

        company_has_license=company.has_construction_license,
        requires_license=requires_llicense,

        company_has_tax=company.has_tax_registration,
        requires_tax=requires_tax,
    )
    analysis, created =BidReadinessAnalysis.objects.update_or_create(
        tender_id=tender_id,
        company=company,
        defaults={
        "matched_requirements": result["matched_requirements"],
        "missing_requirements": result["missing_requirements"],
        "critical_missing_requirements": result[
            "critical_missing_requirements"
        ],
        "score": result["score"],
        "readiness": result["readiness"],
        "bid_ready": result["bid_ready"],
        }
        
    )

    return result

def parse_project_requirement(text):
    if not text:
        return None
    match = re.search(
        r"(\d+)\s+similar",
        text.lower()
    )

    if match:
        return int(match.group(1))

    return None

def check_license_requirement(requirements):
    for requirement in requirements:
        text=requirement.lower()

        if "construction license" in text or "construction licenses" in text:
            return True

    return False

def check_tax_requirement(requirements):

    for requirement in requirements:

        text = requirement.lower()

        if "tax registration" in text:
            return True

    return False