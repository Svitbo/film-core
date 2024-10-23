from typing import List

from pydantic import BaseModel

from ..enums import RoleEnum
from .film import Film


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: RoleEnum
    favorite_films: List[Film] = []

    class Config:
        from_attributes = True
