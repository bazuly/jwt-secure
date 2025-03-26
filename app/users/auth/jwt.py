from datetime import datetime, timedelta
from typing import Any

from fastapi import Request
from redis.asyncio import Redis
from jose import jwt

from app.config import settings

# TODO удалить все комментарии


class JWTHandler:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.algorithm = settings.JWT_ENCODE_ALGORITHM
        self.access_token_expire = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire = timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.token_usage_key_prefix = "token_usage:"
        self.token_ip_key_prefix = "token_ip:"

    async def create_access_token(self, subject: str) -> tuple[str, datetime]:
        expire = datetime.utcnow() + self.access_token_expire
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "access"
        }
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=self.algorithm
        )
        # Добавляем токен в белый список
        await self.redis.set(
            f"whitelist:access:{encoded_jwt}",
            "valid",
            ex=int(self.access_token_expire.total_seconds())
        )
        return encoded_jwt, expire

    async def create_refresh_token(self, subject: str) -> tuple[str, datetime]:
        expire = datetime.utcnow() + self.refresh_token_expire
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "refresh"
        }
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=self.algorithm
        )
        # Добавляем токен в белый список
        await self.redis.set(
            f"whitelist:refresh:{encoded_jwt}",
            "valid",
            ex=int(self.refresh_token_expire.total_seconds())
        )
        return encoded_jwt, expire

    async def _check_concurrent_usage(self, token: str, request: Request) -> bool:
        """Проверяет, не используется ли токен одновременно с разных IP-адресов"""
        client_ip = request.client.host
        token_usage_key = f"{self.token_usage_key_prefix}{token}"
        token_ip_key = f"{self.token_ip_key_prefix}{token}"

        # Получаем текущий IP для токена
        stored_ip = await self.redis.get(token_ip_key)

        if stored_ip and stored_ip != client_ip:
            # Если IP отличается от сохраненного, значит токен используется с другого IP
            return False

        # Обновляем информацию о последнем использовании
        await self.redis.set(
            token_usage_key,
            datetime.utcnow().isoformat(),
            ex=int(self.access_token_expire.total_seconds())
        )
        await self.redis.set(
            token_ip_key,
            client_ip,
            ex=int(self.access_token_expire.total_seconds())
        )

        return True

    async def verify_token(self, token: str, request: Request) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[self.algorithm]
            )

            # Проверяем, не в черном ли списке токен
            if await self.redis.get(f"blacklist:{token}"):
                raise jwt.JWTError("Token is blacklisted")

            # Проверяем, в белом ли списке токен
            token_type = payload.get("type", "access")
            if not await self.redis.get(f"whitelist:{token_type}:{token}"):
                raise jwt.JWTError("Token not in whitelist")

            # Проверяем одновременное использование
            if not await self._check_concurrent_usage(token, request):
                # Если обнаружено одновременное использование, добавляем токен в черный список
                await self.blacklist_token(token)
                raise jwt.JWTError(
                    "Token is being used from different IP address")

            return payload
        except jwt.JWTError:
            raise jwt.JWTError("Could not validate credentials")

    async def blacklist_token(self, token: str) -> None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[self.algorithm]
            )
            exp = payload.get("exp")
            if exp:
                # Вычисляем оставшееся время жизни токена
                expire_time = datetime.fromtimestamp(exp) - datetime.utcnow()
                # Добавляем токен в черный список
                await self.redis.set(
                    f"blacklist:{token}",
                    "invalid",
                    ex=int(expire_time.total_seconds())
                )
                # Удаляем из белого списка
                token_type = payload.get("type", "access")
                await self.redis.delete(f"whitelist:{token_type}:{token}")
                # Удаляем информацию об использовании
                await self.redis.delete(f"{self.token_usage_key_prefix}{token}")
                await self.redis.delete(f"{self.token_ip_key_prefix}{token}")
        except jwt.JWTError:
            pass  # Если токен невалидный, ничего не делаем
