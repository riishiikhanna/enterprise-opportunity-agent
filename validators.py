
import re
from schemas import OpportunityAssessment


def normalize_text(text: str) -> str:
    """
    Convert text into comparable words.
    Ignore differences in capitalization,
    punctuation, and whitespace.
    """
    words = re.findall(r"\w+", text.casefold())
    return " ".join(words)


def is_supported_fact(
    fact: str,
    customer_requirement: str
) -> bool:
    """
    Check whether a fact appears as a
    contiguous phrase in customer input.
    """
    fact_text = normalize_text(fact)
    source_text = normalize_text(customer_requirement)

    if not fact_text:
        return False

    return f" {fact_text} " in f" {source_text} "


def validate_assessment(
    assessment: OpportunityAssessment,
    requirement: str
) -> list[str]:
    """
    Return warnings for quality-rule violations.
    An empty list means no violations detected.
    """
    issues = []

    # Rule 1: Check known customer facts
    for fact in assessment.known_facts:
        if not is_supported_fact(fact, requirement):
            issues.append(
                f"Known fact is not a direct quote: {fact}"
            )

    # Rule 2: Require 2 to 4 opportunities
    count = len(assessment.opportunities)

    if not 2 <= count <= 4:
        issues.append(
            f"Expected 2-4 opportunities, received {count}"
        )

    # Rule 3: Check supporting evidence
    for index, opportunity in enumerate(
        assessment.opportunities, start=1
    ):
        if not opportunity.supporting_facts:
            issues.append(
                f"Opportunity {index} has no supporting facts"
            )

        for fact in opportunity.supporting_facts:
            if not is_supported_fact(fact, requirement):
                issues.append(
                    f"Opportunity {index} has an unsupported "
                    f"fact: {fact}"
                )

    # Rule 4: Require discovery questions
    if len(assessment.discovery_questions) < 3:
        issues.append(
            "At least 3 discovery questions are required"
        )

    return issues