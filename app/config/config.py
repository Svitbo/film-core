import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # DB section
    DB_USER = os.getenv("MARIADB_USER")
    DB_PASSWORD = os.getenv("MARIADB_PASSWORD")
    DB_DATABASE = os.getenv("MARIADB_DATABASE")
    DB_HOSTNAME = os.getenv("MARIADB_HOSTNAME")
    DB_PORT = os.getenv("MARIADB_PORT")
    DB_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_DATABASE}"
    )

    # Plugins section
    INITIAL_ADMIN_USERNAME = os.getenv("INITIAL_ADMIN_USERNAME")
    INITIAL_ADMIN_PASSWORD = os.getenv("INITIAL_ADMIN_PASSWORD")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(";")

    # JWT section
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

    # GCP section
    GCP_STORAGE_API_PREFIX = os.getenv("GCP_STORAGE_API_PREFIX")
    GCP_STATIC_BUCKET = os.getenv("GCP_STATIC_BUCKET")
    GCP_COVERS_PREFIX = os.getenv("GCP_COVERS_PREFIX")


config = Config()
