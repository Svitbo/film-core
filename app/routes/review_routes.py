from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth.auth import get_current_user, get_db
from ..crud import (
    create_review,
    delete_review,
    get_reviews_by_film,
    get_reviews_by_user,
)
from ..models import Film as FilmModel
from ..models import User as UserModel
from ..schemas import Review, ReviewCreate

router = APIRouter()


@router.post("/", response_model=Review)
async def create_review_route(
    review: ReviewCreate,
    film_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db.query(FilmModel).filter(FilmModel.id == film_id).first()

    return create_review(db=db, review=review, user_id=current_user.id, film_id=film_id)


@router.get("/films/{film_id}/reviews", response_model=list[Review])
def get_film_reviews(film_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_film(db=db, film_id=film_id)


@router.get("/users/{user_id}/reviews", response_model=list[Review])
def get_film_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_user(db=db, user_id=user_id)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review_route(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return delete_review(db=db, review_id=review_id)
