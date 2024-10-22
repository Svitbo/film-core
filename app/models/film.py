from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from ..enums import CountryEnum, GenreEnum, ProducerEnum
from . import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    production_year = Column(Integer, nullable=False)
    production_country = Column(Enum(CountryEnum), nullable=False)
    genre = Column(Enum(GenreEnum), nullable=False)
    producer = Column(Enum(ProducerEnum), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    revenue = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    cover_image = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
