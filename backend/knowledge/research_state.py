from typing import TypedDict 

class ResearchState(TypedDict, total=False):
    case_id: int
    legal_issue: str
    jurisdiction: str
    facts: str

    research_queries: list[str]
    retrieved_chunks: list[dict]

    findings: str
    relevant_sections: list[str]
    sources: list[str]
    unresolved_questions: list[str]

