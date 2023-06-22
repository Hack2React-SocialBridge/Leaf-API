from __future__ import annotations

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    disabled = Column(Boolean)
    profile_image = Column(String)
