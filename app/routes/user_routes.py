from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_user_by_username,
)
from ..crud import (
    add_film_to_favorites,
    create_user,
    get_favorite_films,
    remove_film_from_favorites,
)
from ..database import get_db
from ..enums import RoleEnum
from ..models import User as UserModel
from ..schemas import Film as FilmSchema
from ..schemas import User, UserCreate

router = APIRouter()


@router.post("/register", response_model=User)
def register_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user, role=RoleEnum.USER)


@router.post("/token")
async def token_route(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = await authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": db_user.username, "role": db_user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# "Favorite film" operations


@router.post("/favorites/{film_id}", response_model=User)
def add_favorite_film(
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return add_film_to_favorites(db, current_user.id, film_id)


@router.post("/users/{user_id}/favorites/{film_id}", response_model=User)
def add_favorite_film(
    user_id: int,
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return add_film_to_favorites(db, user_id, film_id)


@router.get("/favorites", response_model=list[FilmSchema])
def get_user_favorite_films(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_favorite_films(db, current_user.id)


@router.get("/users/{user_id}/favorites", response_model=list[FilmSchema])
def get_user_favorite_films(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_favorite_films(db, user_id)


@router.delete("/favorites/{film_id}", response_model=User)
def remove_favorite_film(
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return remove_film_from_favorites(db, current_user.id, film_id)


@router.delete("/users/{user_id}/favorites/{film_id}", response_model=User)
def remove_favorite_film(
    user_id: int,
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")

    return remove_film_from_favorites(db, user_id, film_id)
