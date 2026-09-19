from pydantic import BaseModel

class ResearchRequest(BaseModel):
    legal_question: str
    jurisdiction: str
    facts: str