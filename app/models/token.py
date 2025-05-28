from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class Token(BaseModel):
    __tablename__ = "tokens"

    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confirm_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    reset_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    verification_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    reset_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    verification_code_expiration: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    reset_code_expiration: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="token")  # noqa: F821
