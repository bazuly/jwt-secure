from datetime import datetime, timedelta
import logging
from typing import Any

from fastapi import Request
from redis.asyncio import Redis
from jose import jwt

from app.config import settings

logger = logging.getLogger(__name__)


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

    async def create_access_token(self, subject: int) -> str:
        try:
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

            whitelist_key = f"whitelist:access:{encoded_jwt}"
            await self.redis.set(
                whitelist_key,
                "valid",
                ex=int(self.access_token_expire.total_seconds())
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating access token: {str(e)}")
            raise

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
        await self.redis.set(
            f"whitelist:refresh:{encoded_jwt}",
            "valid",
            ex=int(self.refresh_token_expire.total_seconds())
        )
        return encoded_jwt, expire

    # проверка, не используется ли токен одновременно с разных IP-адресов
    async def _check_concurrent_usage(self, token: str, request: Request) -> bool:
        # По сути подход с x-forwarded-for - самый распространённый способ получения ip-адреса клиента,
        # если мы используем прокси-серверы. Обычно это nginx, но в нашем случае это uvicorn.
        # Неплохая статья про X-Forwarded-For
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For
        forwarded_for = request.headers.get("X-Forwarded-For", "")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = request.client.host

        logger.info(f"Checking concurrent usage for IP: {client_ip}")

        token_usage_key = f"{self.token_usage_key_prefix}{token}"
        token_ip_key = f"{self.token_ip_key_prefix}{token}"

        stored_ip = await self.redis.get(token_ip_key)
        logger.info(f"Stored IP: {stored_ip}")

        if stored_ip and stored_ip != client_ip:
            logger.info(
                f"IP mismatch: stored={stored_ip}, current={client_ip}")
            return False

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

            if await self.redis.get(f"blacklist:{token}"):
                raise jwt.JWTError("Token is blacklisted")

            token_type = payload.get("type", "access")
            if not await self.redis.get(f"whitelist:{token_type}:{token}"):
                raise jwt.JWTError("Token not in whitelist")

            if not await self._check_concurrent_usage(token, request):
                await self.blacklist_token(token)
                raise jwt.JWTError(
                    "Token is being used from different IP address")

            return payload
        except jwt.JWTError as e:
            raise jwt.JWTError("Could not validate credentials")
        except Exception as e:
            raise

    async def blacklist_token(self, token: str) -> None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[self.algorithm]
            )
            exp = payload.get("exp")
            if exp:
                expire_time = datetime.fromtimestamp(exp) - datetime.utcnow()
                await self.redis.set(
                    f"blacklist:{token}",
                    "invalid",
                    ex=int(expire_time.total_seconds())
                )
                token_type = payload.get("type", "access")
                await self.redis.delete(f"whitelist:{token_type}:{token}")
                await self.redis.delete(f"{self.token_usage_key_prefix}{token}")
                await self.redis.delete(f"{self.token_ip_key_prefix}{token}")
        except jwt.JWTError:
            pass

    async def is_token_blacklisted(self, access_token: str) -> bool:
        return await self.redis.get(f"blacklist:{access_token}") is not None
