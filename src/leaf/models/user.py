from __future__ import annotations

import enum
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class PermissionsType(enum.Enum):
    read_users = 1
    modify_users = 2
    grant_permissions = 4
    revoke_permissions = 8
    read_threats = 16
    modify_threats = 32


class GroupMembership(TimestampedMixin, Base):
    __tablename__ = "groups_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    # user: Mapped["User"] = relationship()
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    # group: Mapped["Group"] = relationship()


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
    profile_image: Mapped[str] = mapped_column(nullable=True)
    posts: Mapped["Post"] = relationship(back_populates="user")
    comments: Mapped["Comment"] = relationship(back_populates="user")
    likes: Mapped["Like"] = relationship(back_populates="user")
    permissions: Mapped[int] = mapped_column(default=0)
    groups: Mapped["Group"] = relationship(
        secondary="groups_users",
        back_populates="users",
    )

    def check_permissions(self, permission: int) -> bool:
        """Checks if User have specified permission using & byte operator

        Args:
            permission (int): Permission to check,
            Should be a value from PermissionsType Enum

        Returns: True if user have permission, False if User doesn't have
        """
        return bool(self.permissions & permission)

    @property
    def mapped_permissions(self) -> dict:
        """Returns dict with mapped permission_name: bool
        for example if user have permissions read_users and grant_permissions returns dict:
        {
            'read_users': True,
            'modify_users': False,
            'grant_permissions': True,
            'revoke_permissions': False,
            'read_threats': False,
            'modify_threats': False,
        }

        Returns: dict with mapped permissions

        """
        return {
            permission.name: self.check_permissions(permission.value)
            for permission in PermissionsType
        }


class Group(TimestampedMixin, Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    permissions: Mapped[int]
    users: Mapped["User"] = relationship(
        secondary="groups_users",
        back_populates="groups",
    )
