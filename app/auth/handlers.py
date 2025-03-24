from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.auth_service import AuthService
from app.models.schemas import Token, LoginRequest
from app.depends import get_auth_service, get_token_repo

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token)
async def login(
    body: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    return auth_service.login(username=body.username, password=body.password)


@router.post("/logout")
async def logout(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: str = Depends(get_token_repo),
) -> dict:
    auth_service.logout(token)
    return {
        "message": "Successfully logged out"
    }
