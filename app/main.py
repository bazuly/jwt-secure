from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.user_profile.handlers import router as user_router
from app.content.handlers import router as content_router
from app.exceptions import (
    validation_exception_handler,
    database_error_handler,
    sqlalchemy_error_handler,
    jwt_error_handler,
    generic_exception_handler,
    DatabaseError,
    RequestValidationError,
    SQLAlchemyError,
    JWTError
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # В проде конечно же надо будет ограничить
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(JWTError, jwt_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


app.include_router(user_router)
app.include_router(content_router)


@app.get("/")
async def root():
    return {"message": "Welcome to JWT Secure API"}
