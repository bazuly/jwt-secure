from fastapi import Depends
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.users.auth.jwt import JWTHandler
from app.content.service import ContentService
from app.infra.database import get_db_connection
from app.content.repository import ContentRepository
from app.content.models import AccessLevel
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.service import UserService


async def get_redis():
    redis = await from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()


async def get_content_repository(db_session: AsyncSession = Depends(get_db_connection)) -> ContentRepository:
    return ContentRepository(db_session=db_session)


async def get_content_service(content_repository: ContentRepository = Depends(get_content_repository)) -> ContentService:
    return ContentService(content_repository=content_repository)

# TODO херь какая-то


async def get_user_access_level(redis: Redis = Depends(get_redis)) -> AccessLevel:
    return AccessLevel.PUBLIC


async def get_user_repository(db_session: AsyncSession = Depends(get_db_connection)) -> UserProfileRepository:
    return UserProfileRepository(db_session=db_session)


async def get_user_service(user_repository: UserProfileRepository = Depends(get_user_repository)) -> UserService:
    return UserService(user_repository=user_repository)


def get_jwt_handler(redis: Redis = Depends(get_redis)) -> JWTHandler:
    return JWTHandler(redis)
