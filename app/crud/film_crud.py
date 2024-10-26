from fastapi import HTTPException, UploadFile
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from ..config import config
from ..gcp import static_bucket
from ..models import Film as FilmModel
from ..models import User as UserModel
from ..schemas import Film as FilmSchema
from ..schemas import FilmCreate


def create_film(db: Session, film: FilmCreate) -> FilmSchema:
    db_film = FilmModel(
        title=film.title,
        production_year=film.production_year,
        production_country=film.production_country,
        genre=film.genre,
        producer=film.producer,
        duration_minutes=film.duration_minutes,
        revenue=film.revenue,
        description=film.description,
        cover_image=None,
    )

    db.add(db_film)
    db.commit()
    db.refresh(db_film)

    return db_film


def update_film_cover_image(
    db: Session, film_id: int, cover_image_url: str
) -> FilmSchema:
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    db_film.cover_image = cover_image_url
    db.commit()
    db.refresh(db_film)

    return db_film


async def upload_to_gcp_bucket(
    file: UploadFile, bucket_name: str, object_name: str
) -> str:
    blob = static_bucket.blob(object_name)

    blob.upload_from_file(file.file, content_type=file.content_type)

    return f"{config.GCP_STORAGE_API_PREFIX}/{bucket_name}/{object_name}"


def get_film_by_id(db: Session, film_id: int) -> FilmSchema:
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    return db_film


def get_films(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    year_start: int | None = None,
    year_end: int | None = None,
    genre: str | None = None,
    sort_by: str | None = None,
    sort_order: str | None = "asc",
) -> list[FilmSchema]:
    query = db.query(FilmModel)

    if year_start is not None:
        query = query.filter(FilmModel.production_year >= year_start)
    if year_end is not None:
        query = query.filter(FilmModel.production_year <= year_end)
    if genre is not None:
        query = query.filter(FilmModel.genre == genre)

    allowed_sort_fields = ["title", "production_year", "created_at"]

    if sort_by in allowed_sort_fields:
        if sort_order == "desc":
            query = query.order_by(desc(getattr(FilmModel, sort_by)))
        else:
            query = query.order_by(asc(getattr(FilmModel, sort_by)))

    return query.offset(skip).limit(limit).all()


def update_film(db: Session, film_id: int, film_data: FilmCreate) -> FilmSchema:
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    db_film.title = film_data.title
    db_film.production_year = film_data.production_year
    db_film.production_country = film_data.production_country
    db_film.genre = film_data.genre
    db_film.producer = film_data.producer
    db_film.duration_minutes = film_data.duration_minutes
    db_film.revenue = film_data.revenue
    db_film.description = film_data.description

    db.commit()
    db.refresh(db_film)

    return db_film


def delete_film(db: Session, film_id: int) -> bool:
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    db.delete(db_film)
    db.commit()

    return True


# "Favorite film" operations


def add_film_to_favorites(db: Session, user_id: int, film_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_user or not db_film:
        raise HTTPException(status_code=404, detail="User or film not found")

    if db_film in db_user.favorite_films:
        raise HTTPException(status_code=400, detail="Film already in favorites")

    db_user.favorite_films.append(db_film)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_favorite_films(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user.favorite_films


def remove_film_from_favorites(db: Session, user_id: int, film_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_user or not db_film:
        raise HTTPException(status_code=404, detail="User or film not found")

    if db_film not in db_user.favorite_films:
        raise HTTPException(status_code=400, detail="Film not in favorites")

    db_user.favorite_films.remove(db_film)
    db.commit()
    db.refresh(db_user)

    return db_user
