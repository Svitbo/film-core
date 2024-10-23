from .. import SessionLocal
from ..config import config
from ..crud import create_user
from ..enums import RoleEnum
from ..models import User as UserModel
from ..schemas import UserCreate

INITIAL_ADMIN_USERNAME = config.INITIAL_ADMIN_USERNAME
INITIAL_ADMIN_PASSWORD = config.INITIAL_ADMIN_PASSWORD


def add_initial_admin():
    with SessionLocal() as session:
        initial_admin = (
            session.query(UserModel)
            .filter(
                UserModel.username == INITIAL_ADMIN_USERNAME,
                UserModel.role == RoleEnum.ADMIN,
            )
            .first()
        )

        if initial_admin is not None:
            print("Initial admin already exists in the users table. No action taken")
            return

        initial_admin_data = UserCreate(
            username=INITIAL_ADMIN_USERNAME,
            password=INITIAL_ADMIN_PASSWORD,
        )

        create_user(session, initial_admin_data, role=RoleEnum.ADMIN)

        print("Initial admin added to the users table")


if __name__ == "__main__":
    add_initial_admin()
