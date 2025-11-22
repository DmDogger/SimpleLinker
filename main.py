from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <-- Добавьте эту строку

from app.api.routes.link import router as link_router

app = FastAPI(
    title='SimpleLinker',
    description='URL Shortener',
    version='0.1.0'
)

origins = [
    "https://www.simplelinker.cc",
    "https://simplelinker.cc",
    "https://simplelinker-frontend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(link_router, prefix='/api')


