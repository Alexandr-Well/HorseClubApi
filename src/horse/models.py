from datetime import datetime
from typing import List, Optional
from sqlalchemy import (TIMESTAMP, ForeignKey, Integer, String, Column)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database import Base



class Horse(Base):
    __tablename__ = "horse"
    __table_args__ = {'extend_existing': True}
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    photo: Mapped[Optional[List["HorsePhoto"]]] = relationship(back_populates="horse")
    # photo_id: Mapped[Optional[List["HorsePhoto"]]] = relationship(back_populates="horse")


class HorsePhoto(Base):
    __tablename__ = "horse_photo"
    __table_args__ = {'extend_existing': True}
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False)
    horse_id: Mapped[int] = mapped_column(ForeignKey("horse.id"))
    horse: Mapped["Horse"] = relationship(back_populates="photo")

    def _model_as_dict(self):
        return self.__dict__
