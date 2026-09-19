from sqlalchemy import Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from database import Base

class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    legal_area: Mapped[str | None] = mapped_column(String(100), nullable=True)
    legal_issue: Mapped[str | None] = mapped_column(String(200), nullable=True)
    urgency_score: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[str | None] = mapped_column(String(50), nullable=True)
    intake_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


