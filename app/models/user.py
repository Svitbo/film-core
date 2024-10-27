from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from ..enums import RoleEnum
from . import Base
from .film_user_association import favorite_films_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)

    favorite_films = relationship(
        "Film", secondary=favorite_films_table, back_populates="favorited_by"
    )

    reviews = relationship("Review", back_populates="user")
