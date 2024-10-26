from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Film as FilmModel
from ..models import Review as ReviewModel
from ..models import User as UserModel
from ..schemas import ReviewCreate


def create_review(
    db: Session, review: ReviewCreate, user_id: int, film_id: int
) -> ReviewModel:
    db_review = (
        db.query(ReviewModel)
        .filter(ReviewModel.user_id == user_id, ReviewModel.film_id == film_id)
        .first()
    )

    if db_review:
        raise HTTPException(
            status_code=400, detail="User has already reviewed this film"
        )

    db_review = ReviewModel(
        rating=review.rating,
        title=review.title,
        comment=review.comment,
        user_id=user_id,
        film_id=film_id,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def get_reviews_by_film(db: Session, film_id: int):
    db_film = db.query(FilmModel).filter(FilmModel.id == film_id).first()

    if not db_film:
        raise HTTPException(status_code=404, detail="Film not found")

    return db.query(ReviewModel).filter(ReviewModel.film_id == db_film.id).all()


def get_reviews_by_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(ReviewModel).filter(ReviewModel.user_id == db_user.id).all()


def delete_review(db: Session, review_id: int) -> None:
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return True
