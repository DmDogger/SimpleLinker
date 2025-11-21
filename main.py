from fastapi import FastAPI

from app.api.routes.link import router as link_router

app = FastAPI(
    title='SimpleLinker',
    description='URL Shortener',
    version='0.1.0'
)

app.include_router(link_router)


