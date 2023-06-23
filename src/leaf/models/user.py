from __future__ import annotations

import enum
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class PermissionsType(enum.Enum):
    read_users = 1
    create_content = 2
    grant_permissions = 4
    revoke_permissions = 8
    read_threats = 16
    modify_threats = 32


class User(TimestampedMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
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
    comments: Mapped["Comment"] = relationship(back_populates="user")
    likes: Mapped["Like"] = relationship(back_populates="user")
    permissions: Mapped[int]
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="users", uselist=False)


class Group(TimestampedMixin, Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    permissions: Mapped[int]
    users: Mapped["User"] = relationship(back_populates="group")
