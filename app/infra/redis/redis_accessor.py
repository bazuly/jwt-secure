from redis import asyncio as redis
from app.config import get_settings

settings = get_settings()


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        port=settings.CACHE_PORT,
        host=settings.CACHE_HOST,
        decode_responses=True
    )
