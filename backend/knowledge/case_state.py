from typing import TypedDict  

class CaseState(TypedDict, total=False):
    case_id: int
    conversation: list[dict]

    legal_issue: str
    jurisdiction: str
    facts: str

    intake_complete: bool
    missing_information: list[str]

    legal_area: str
    classification_reason: str

    research_queries: list[str]
    retrieved_chunks: list[dict]
    findings: str
    relevant_sections: list[str]
    sources: list[str]
    unresolved_questions: list[str]

    urgency_score: int
    priority: str
    triage_reason: str

    case_brief: str