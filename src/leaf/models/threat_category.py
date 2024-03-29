from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class ThreatCategory(TimestampedMixin, Base):
    __tablename__ = "threat_categories"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    threats: Mapped["Threat"] = relationship(back_populates="category")
