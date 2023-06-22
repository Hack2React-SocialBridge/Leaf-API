from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from leaf.config.database import Base
from leaf.models.mixins import TimestampedMixin


class ThreatCategory(TimestampedMixin, Base):
    __tablename__ = "threat_categories"

    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255))
