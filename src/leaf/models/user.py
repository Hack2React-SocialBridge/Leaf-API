from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class User(TimestampedMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
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
    posts: Mapped["Post"] = relationship(back_populates="user")
