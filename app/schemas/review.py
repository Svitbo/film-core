from typing import Optional

from pydantic import BaseModel, conint, constr


class ReviewBase(BaseModel):
    rating: conint(ge=0, le=100)
    title: constr(max_length=255)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    user_id: int
    film_id: int

    class Config:
        from_attributes = True
