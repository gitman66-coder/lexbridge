from typing import TypedDict 

class ClassificationState(TypedDict, total=False):
    case_id: int
    
    legal_issue: str
    jurisdiction: str
    facts: str

    legal_area: str
    classification_reason: str