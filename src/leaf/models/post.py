from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class Post(TimestampedMixin, Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts", uselist=False)
    content: Mapped[str] = mapped_column(String(255))
    image: Mapped[int] = mapped_column(String)
    is_visible: Mapped[bool] = mapped_column(String)
    comments: Mapped["Comment"] = relationship(back_populates="post")
    likes: Mapped["Likes"] = relationship(back_populates="post")
    threat_id: Mapped[int] = mapped_column(ForeignKey("threats.id"))
    threat: Mapped["Threat"] = relationship(back_populates="posts", uselist=False)
