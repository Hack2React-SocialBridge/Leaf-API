from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    user_id = Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user = Mapped["User"] = relationship(back_populates="posts", uselist=False)
