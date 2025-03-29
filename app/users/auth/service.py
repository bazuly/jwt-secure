from dataclasses import dataclass
import logging

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import Settings
from app.exceptions import UserNotFoundException, UserNotCorrectPasswordException
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.models import UserProfile
from app.users.user_profile.password import verify_password
from app.users.auth.schemas import AuthResponseSchema
from app.users.auth.jwt import JWTHandler

logger = logging.getLogger(__name__)


@dataclass
class AuthService:
    user_repository: UserProfileRepository
    settings: Settings
    jwt_handler: JWTHandler

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if not verify_password(password, user.password):
            raise UserNotCorrectPasswordException

    async def login_user(self, username: str, password: str) -> AuthResponseSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)

        access_token = await self.jwt_handler.create_access_token(subject=user.id)
        return AuthResponseSchema(
            user_id=user.id,
            access_token=access_token
        )

    def get_user_from_token(self, access_token: str) -> UserProfile:
        try:
            payload = jwt.decode(
                access_token=access_token,
                key=self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM]
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        logger.info(f"User {payload['user_id']} logged in")
        return payload["user_id"]


# TODO: Сделать все импорты по pep8
