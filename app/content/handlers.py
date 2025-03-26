from fastapi import APIRouter, Depends

from app.content.models import AccessLevel
from app.content.service import ContentService
from app.content.schemas import ContentSchema
from app.dependency import get_content_service, get_user_access_level


router = APIRouter(prefix="/content")


@router.post("/create", response_model=ContentSchema)
async def create_content(
    content: ContentSchema,
    content_service: ContentService = Depends(get_content_service)
):
    return content_service.create_content(content)


@router.get("/get_content/{content_id}", response_model=ContentSchema)
async def get_content(
    content_id: int,
    user_access_level: AccessLevel = Depends(get_user_access_level),
    content_service: ContentService = Depends(get_content_service)
):
    return content_service.get_content_by_id(content_id, user_access_level)
