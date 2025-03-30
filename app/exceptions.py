from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError


class DatabaseError(Exception):
    """Base exception for all database errors."""
    pass


class DatabaseConnectionError(DatabaseError):
    """Exception raised when a database connection cannot be established."""

    def __init__(self, details: str = None):
        self.details = details
        message = "Failed to connect to database."
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class RepositoryError(DatabaseError):
    """Default repository exception."""

    def __init__(self, message: str = "Repository error"):
        super().__init__(message)


class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


async def database_error_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Database error: {str(exc)}"}
    )


async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid authentication credentials"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
