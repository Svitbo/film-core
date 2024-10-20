from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.auth import get_current_user
from ..crud.film_crud import (
    create_film,
    delete_film,
    get_film_by_id,
    get_films,
    update_film,
)
from ..database import get_db
from ..enums import RoleEnum
from ..models import User as UserModel
from ..schemas import Film, FilmCreate

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
    films = get_films(
        db,
        skip=skip,
        limit=limit,
        year_start=year_start,
        year_end=year_end,
        genre=genre,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return films


@router.get("/{film_id}", response_model=Film)
def read_film_route(film_id: int, db: Session = Depends(get_db)):
    db_film = get_film_by_id(db=db, film_id=film_id)
    if db_film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return db_film


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

    db_film = update_film(db=db, film_id=film_id, film_data=film_data)
    if db_film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return db_film


@router.delete("/{film_id}", response_model=dict)
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

    success = delete_film(db=db, film_id=film_id)
    if not success:
        raise HTTPException(status_code=404, detail="Film not found")
    return {"detail": "Film deleted successfully"}
