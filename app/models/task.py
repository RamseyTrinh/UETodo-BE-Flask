from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"

    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=True)
    status = mapped_column(Boolean, nullable=False, default=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    start_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    priority = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete='CASCADE'), nullable=False
    )
    
