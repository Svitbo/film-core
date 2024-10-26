from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="reviews")
    film = relationship("Film", back_populates="reviews")
