
import pytest
from pydantic import ValidationError

from schemas import Opportunity, OpportunityAssessment
from tools import lookup_service_capabilities
from validators import validate_assessment


REQUIREMENT = """
We operate 120 buildings.
Equipment failures are increasing.
"""


def sample_assessment():
    """Create a sample without calling OpenAI."""

    opportunities = [
        Opportunity(
            title="Predictive Maintenance",
            business_problem="Increasing failures",
            proposed_solution="AI failure prediction",
            expected_business_value="Potentially less downtime",
            supporting_facts=[
                "Equipment failures are increasing"
            ]
        ),
        Opportunity(
            title="Maintenance Reporting",
            business_problem="Maintenance visibility",
            proposed_solution="Operational dashboards",
            expected_business_value="Better visibility",
            supporting_facts=[
                "We operate 120 buildings"
            ]
        )
    ]

    return OpportunityAssessment(
        customer_summary="Building maintenance",
        known_facts=[
            "We operate 120 buildings"
        ],
        assumptions=[],
        opportunities=opportunities,
        discovery_questions=[
            "What equipment data exists?",
            "What is the failure history?",
            "Which buildings are highest priority?"
        ],
        recommended_next_step="Review maintenance data"
    )


def test_valid_assessment_passes():
    assessment = sample_assessment()

    issues = validate_assessment(
        assessment, REQUIREMENT
    )

    assert issues == []


def test_invented_fact_is_detected():
    assessment = sample_assessment()

    assessment.known_facts.append(
        "Annual losses are $5 million"
    )

    issues = validate_assessment(
        assessment, REQUIREMENT
    )

    assert any(
        "$5 million" in issue for issue in issues
    )


def test_missing_evidence_is_detected():
    assessment = sample_assessment()

    assessment.opportunities[0].supporting_facts = []

    issues = validate_assessment(
        assessment, REQUIREMENT
    )

    assert any(
        "no supporting facts" in issue
        for issue in issues
    )


def test_capability_lookup_filters():
    result = lookup_service_capabilities(
        "ai_automation"
    )

    assert len(result["capabilities"]) > 0

    assert all(
        item["category"] == "ai_automation"
        for item in result["capabilities"]
    )


def test_invalid_category_is_rejected():
    with pytest.raises(ValueError):
        lookup_service_capabilities(
            "unknown_category"
        )


def test_pydantic_rejects_missing_fields():
    with pytest.raises(ValidationError):
        Opportunity(
            title="Incomplete Opportunity",
            business_problem="Missing information",
            proposed_solution="Unknown",
            expected_business_value="Unknown"
            # supporting_facts is intentionally missing
        )