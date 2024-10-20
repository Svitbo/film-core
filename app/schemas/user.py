from pydantic import BaseModel

from ..enums import RoleEnum


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: RoleEnum

    class Config:
        from_attributes = True
