
from pydantic import BaseModel


class Opportunity(BaseModel):
    title: str
    business_problem: str
    proposed_solution: str
    expected_business_value: str
    supporting_facts: list[str]


class OpportunityAssessment(BaseModel):
    customer_summary: str
    known_facts: list[str]
    assumptions: list[str]
    opportunities: list[Opportunity]
    discovery_questions: list[str]
    recommended_next_step: str