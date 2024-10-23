from datetime import datetime

from pydantic import BaseModel

from ..enums import CountryEnum, GenreEnum, ProducerEnum


class FilmBase(BaseModel):
    title: str
    production_year: int
    production_country: CountryEnum
    genre: GenreEnum
    producer: ProducerEnum
    duration_minutes: int
    revenue: int
    description: str
    cover_image: str | None = None


class FilmCreate(FilmBase):
    pass


class Film(FilmBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
