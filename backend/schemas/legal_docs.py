from pydantic import BaseModel, Field

class LegalDocumentRequest(BaseModel):
    case_id: int
    name: str
    jurisdiction: str
    source_url: str | None = Field(default=None, description="Optional source URL for the legal document.")

class LegalInformation(BaseModel):
    document_id: int
    section: str | None = Field(default=None, description="Optional section of the legal document.")
    content: str
    embedding: list[float] | None = Field(default=None, description="Optional embedding vector for the legal chunk.")
