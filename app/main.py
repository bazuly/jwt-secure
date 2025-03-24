from fastapi import FastAPI

from app.auth.handlers import router as auth_router
from app.content.handlers import router as content_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(content_router)
