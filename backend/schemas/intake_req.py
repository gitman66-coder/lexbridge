from pydantic import BaseModel

class IntakeMessage(BaseModel):
    role: str
    content: str


class IntakeRequest(BaseModel):
    conversation: list[IntakeMessage]