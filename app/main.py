from fastapi import FastAPI

from .database import engine
from .models import Base
from .routes import film_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(film_router, prefix="/films", tags=["films"])
app.include_router(user_router, tags=["users"])
