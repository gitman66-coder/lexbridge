from typing import TypedDict

class IntakeState(TypedDict, total=False):
    conversation: list[dict]

    legal_issue: str
    jurisdiction: str
    facts: str

    missing_information: list[str]
    intake_complete: bool
