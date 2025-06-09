from datetime import date

from sqlalchemy import String, Date, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash

from app.models import BaseModel
from datetime import datetime, date


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    avatar_url: Mapped[str] = mapped_column(Text, default="")
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    token: Mapped["Token"] = relationship("Token", uselist=False, back_populates="user", cascade="all, delete-orphan")

    def __init__(self, email, password, name, dob, gender, phone_number):
        is_verified = False
            
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.dob = dob
        self.gender = gender
        self.phone_number = phone_number
        self.is_verified = is_verified

    def as_dict(self):
        return {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
            if c.name != "password_hash"
        }
