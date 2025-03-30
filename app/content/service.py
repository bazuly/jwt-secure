from dataclasses import dataclass
import logging

from fastapi import HTTPException

from app.content.repository import ContentRepository
from app.content.schemas import ContentSchema
from app.content.models import AccessLevel
from app.users.auth.jwt import JWTHandler


logger = logging.getLogger(__name__)


@dataclass
class ContentService:
    content_repository: ContentRepository
    jwt_handler: JWTHandler

    def _check_access_level(self, content: ContentSchema, user_access_level: AccessLevel) -> bool:
        access_levels = {
            AccessLevel.PUBLIC: 0,
            AccessLevel.PRIVATE: 1,
            AccessLevel.SECRET: 2
        }
        logger.info(
            "Checking access level - Content level: %s, User level: %s",
            content.access_level,
            user_access_level
        )
        logger.info(
            "Access level values - Content: %d, User: %d",
            access_levels[content.access_level],
            access_levels[user_access_level]
        )
        result = access_levels[user_access_level] >= access_levels[content.access_level]
        logger.info("Access check result: %s", result)
        return result

    async def create_content(self, content: ContentSchema) -> ContentSchema:
        created_content = await self.content_repository.create_content(content)
        return created_content

    async def get_content_by_name(self, content_name: str, access_token: str, user_access_level: AccessLevel) -> ContentSchema:
        content = await self.content_repository.retrieve_content(content_name)
        if await self.jwt_handler.is_token_blacklisted(access_token):
            logger.error(
                "Token is blacklisted, access_token: %s",
                access_token,
            )
            raise HTTPException(status_code=401, detail="Token is blacklisted")
        if not content:
            logger.error(
                "Content not found, content_id: %s",
                content_name,
            )
            raise HTTPException(status_code=404, detail="Content not found")

        if not self._check_access_level(content, user_access_level):
            logger.error(
                "Access denied to content %s for user with access level %s",
                content_name,
                user_access_level,
            )
            raise HTTPException(status_code=403, detail="Access denied")

        return content
