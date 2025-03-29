from dataclasses import dataclass
import logging

from fastapi import HTTPException

from app.content.repository import ContentRepository
from app.content.schemas import ContentSchema
from app.content.models import AccessLevel


logger = logging.getLogger(__name__)


@dataclass
class ContentService:
    content_repository: ContentRepository

    def _check_access_level(self, content: ContentSchema, user_access_level: AccessLevel) -> bool:
        access_levels = {
            AccessLevel.PUBLIC: 0,
            AccessLevel.PRIVATE: 1,
            AccessLevel.SECRET: 2
        }
        return access_levels[user_access_level] >= access_levels[content.access_level]

    async def create_content(self, content: ContentSchema) -> ContentSchema:
        created_content = await self.content_repository.create_content(content)
        return created_content

    async def get_content_by_id(self, content_id: int, user_access_level: AccessLevel) -> ContentSchema:
        content = await self.content_repository.retrieve_content(content_id)
        if not content:
            logger.error(
                "Content not found, content_id: %s",
                content_id,
            )
            raise HTTPException(status_code=404, detail="Content not found")

        if not self._check_access_level(content, user_access_level):
            logger.error(
                "Access denied to content %s for user with access level %s",
                content_id,
                user_access_level,
            )
            raise HTTPException(status_code=403, detail="Access denied")

        return content
