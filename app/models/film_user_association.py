from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.base import Base

favorite_films_table = Table(
    "favorite_films",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True),
)
