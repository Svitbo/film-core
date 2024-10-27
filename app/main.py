from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .database import engine
from .models import Base
from .routes import film_router, review_router, user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = config.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(film_router, prefix="/films", tags=["films"])
app.include_router(user_router, tags=["users"])
app.include_router(review_router, prefix="/reviews", tags=["reviews"])
