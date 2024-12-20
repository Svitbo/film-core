from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..auth.auth import get_current_user
from ..config import config
from ..crud.film_crud import *
from ..database import get_db
from ..enums import RoleEnum
from ..models import User as UserModel
from ..schemas import Film, FilmCreate

STATIC_BUCKET = config.GCP_STATIC_BUCKET
STATIC_PREFIX = config.GCP_COVERS_PREFIX

router = APIRouter()


@router.post("/", response_model=Film)
def create_film_route(
    film: FilmCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can add films.",
        )

    return create_film(db=db, film=film)


@router.post("/{film_id}/upload-cover")
async def upload_cover_image(
    film_id: int,
    cover_image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can upload cover images.",
        )

    get_film_by_id(db=db, film_id=film_id)

    object_name = f"{STATIC_PREFIX}/{cover_image.filename}"
    cover_image_url = await upload_to_gcp_bucket(
        cover_image, STATIC_BUCKET, object_name
    )

    return update_film_cover_image(
        db=db, film_id=film_id, cover_image_url=cover_image_url
    )


@router.get("/")
def read_films_route(
    skip: int = 0,
    limit: int = 10,
    year_start: int | None = None,
    year_end: int | None = None,
    genre: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    db: Session = Depends(get_db),
):
    db_films = get_films(
        db,
        skip=skip,
        limit=limit,
        year_start=year_start,
        year_end=year_end,
        genre=genre,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return db_films


@router.get("/{film_id}", response_model=Film)
def read_film_route(film_id: int, db: Session = Depends(get_db)):
    return get_film_by_id(db=db, film_id=film_id)


@router.put("/{film_id}", response_model=Film)
def update_film_route(
    film_id: int,
    film_data: FilmCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can update films.",
        )

    return update_film(db=db, film_id=film_id, film_data=film_data)


@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film_route(
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can delete films.",
        )

    return delete_film(db=db, film_id=film_id)
