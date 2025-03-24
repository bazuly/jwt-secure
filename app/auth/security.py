from app.config import Settings
from infra.redis.redis_accessor import get_redis_connection

redis_client = get_redis_connection()


def add_token_to_blacklist(token: str, expires: int):
    redis_client.setex(f"blacklist:{token}", expires, "true")


def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(f"blacklist:{token}") == 1
