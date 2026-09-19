from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CaseBrief(Base):
    __tablename__ = "case_briefs"

    id: Mapped[int] = mapped_column(primary_key=True)

    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    facts: Mapped[str | None] = mapped_column(Text,nullable=True)
    legal_issue: Mapped[str | None] = mapped_column(Text, nullable=True)
    research: Mapped[str | None] = mapped_column(Text, nullable=True)
    suggested_next_step: Mapped[str | None] = mapped_column(Text, nullable=True)
    draft: Mapped[str | None] = mapped_column(Text, nullable=True)