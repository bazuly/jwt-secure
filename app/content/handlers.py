from fastapi import APIRouter, Depends, HTTPException

from app.auth.auth_service import AuthService
from app.content.service import ContentService
from app.models.schemas import (
    CommonContentResponse,
    RoleContentResponse,
)
from app.depends import get_content_service, get_auth_service

router = APIRouter(prefix="/content")


@router.get("/common", response_model=CommonContentResponse)
async def get_common_content(
    content_service: ContentService = Depends(get_content_service)
):
    return content_service.get_common_content()


@router.get("/role-specific", response_model=RoleContentResponse)
async def get_role_specific_content(
    auth_service: AuthService = Depends(get_auth_service),
    content_service: ContentService = Depends(get_content_service)
):
    return content_service.get_role_specific_content(auth_service.current_user)
