import logging
from fastapi import Depends, Request
from redis.asyncio import Redis, from_url
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.users.auth.jwt import JWTHandler
from app.users.auth.service import AuthService
from app.content.service import ContentService
from app.infra.database import get_db_connection
from app.content.repository import ContentRepository
from app.content.models import AccessLevel
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.service import UserService

logger = logging.getLogger(__name__)


async def get_redis():
    redis = await from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        password=settings.REDIS_PASSWORD,
        encoding="utf-8",
        decode_responses=True
    )
    try:
        await redis.ping()
        logger.info("Successfully connected to Redis")
        yield redis
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise
    finally:
        await redis.close()


def get_jwt_handler(redis: Redis = Depends(get_redis)) -> JWTHandler:
    return JWTHandler(redis)


async def get_content_repository(db_session: AsyncSession = Depends(get_db_connection)) -> ContentRepository:
    return ContentRepository(db_session=db_session)


async def get_content_service(
    content_repository: ContentRepository = Depends(get_content_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> ContentService:
    return ContentService(
        content_repository=content_repository,
        jwt_handler=jwt_handler
    )


async def get_user_repository(db_session: AsyncSession = Depends(get_db_connection)) -> UserProfileRepository:
    return UserProfileRepository(db_session=db_session)


async def get_user_access_level(
    request: Request,
    redis: Redis = Depends(get_redis),
    user_repository: UserProfileRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
) -> AccessLevel:
    """
    Логика работы метода:
    1. Получаем токен из хедера запроса
    2. Если токен не найден, пытаемся получить его из параметров запроса
    3. Если токен не найден, возвращаем PUBLIC
    4. Если токен найден, проверяем его валидность
    5. Если токен валиден, возвращаем уровень доступа пользователя
    """

    # лучше конечно вынести в отдельный метод
    # а то это фигня, а не DDD
    access_token = request.headers.get(
        "Authorization", "").replace("Bearer ", "")

    if not access_token:
        access_token = request.query_params.get("access_token", "")

    if not access_token:
        return AccessLevel.PUBLIC

    try:
        payload = await jwt_handler.verify_token(access_token, request)
        user_id = int(payload["sub"])
        user = await user_repository.get_user_by_id(user_id)
        if user:
            print(
                f"Found user with ID {user_id}, access level: {user.access_level}")
            return user.access_level
        else:
            print(f"User with ID {user_id} not found")
            return AccessLevel.PUBLIC
    except Exception as e:
        print(f"Error getting user access level: {str(e)}")
        return AccessLevel.PUBLIC


def get_auth_service(
    user_repository: UserProfileRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        jwt_handler=jwt_handler
    )


async def get_user_service(
    user_repository: UserProfileRepository = Depends(get_user_repository),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        jwt_handler=jwt_handler,
        auth_service=auth_service
    )
