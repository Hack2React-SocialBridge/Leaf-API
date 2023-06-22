from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class Like(TimestampedMixin, Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="likes", uselist=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="likes", uselist=False)
