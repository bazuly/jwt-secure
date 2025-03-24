from fastapi import Depends
from app.repository.user_repository import TokenRepository
from app.auth.auth_service import AuthService
from app.content.service import ContentService
from redis import Redis


def get_redis():
    return Redis(host="redis", port=6379, db=0)


def get_token_repo(redis: Redis = Depends(get_redis)) -> TokenRepository:
    return TokenRepository(redis)


def get_auth_service(token_repo: TokenRepository = Depends(get_token_repo)) -> AuthService:
    return AuthService(token_repo)


def get_content_service(token_repo: TokenRepository = Depends(get_token_repo)) -> ContentService:
    return ContentService(token_repo)
