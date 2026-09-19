from pydantic import BaseModel

class LegalSearch(BaseModel):
    query: str
    top_k: int = 5