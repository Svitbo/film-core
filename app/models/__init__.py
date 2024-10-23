from .base import Base
from .film import Film
from .film_user_association import favorite_films_table
from .user import User

__all__ = ["Base", "Film", "User", "favorite_films_table"]
