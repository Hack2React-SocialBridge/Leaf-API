from geoalchemy2 import Geometry
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from leaf.config.database import Base


class Threat(Base):
    __tablename__ = "threats"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    location = Column(Geometry("POINT"))
    category_id: Mapped[int] = mapped_column(ForeignKey("threat_categories.id"))
    category: Mapped["ThreatCategory"] = relationship(
        back_populates="threats",
        uselist=False,
    )
    posts: Mapped["Post"] = relationship(back_populates="threat")
