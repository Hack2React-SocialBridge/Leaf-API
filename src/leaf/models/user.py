from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from leaf.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str]
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    disabled: Mapped[bool]
    profile_image: Mapped[str]
