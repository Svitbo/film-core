from enum import Enum


class GenreEnum(str, Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    HORROR = "Horror"
    SCIENCE_FICTION = "Science fiction"
