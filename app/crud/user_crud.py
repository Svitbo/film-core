import bcrypt
from sqlalchemy.orm import Session

from ..enums import RoleEnum
from ..models import User as UserModel
from ..schemas import User as UserSchema
from ..schemas import UserCreate


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_user(db: Session, user: UserCreate, role: RoleEnum) -> UserSchema:
    hashed_password = hash_password(user.password)
    db_user = UserModel(
        username=user.username, hashed_password=hashed_password, role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str) -> UserSchema | None:
    return db.query(UserModel).filter(UserModel.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> UserSchema | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
