from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class Comment(TimestampedMixin, Base):
    __tablename__ = "comments"

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments", uselist=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments", uselist=False)
    content: Mapped[str] = mapped_column(String(255))
