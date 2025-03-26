from dataclasses import dataclass
from logging import Logger

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import Settings
from app.exceptions import UserNotFoundException, UserNotCorrectPasswordException
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.models import UserProfile


@dataclass
class AuthService:
    user_repository: UserProfileRepository
    logger: Logger
    settings: Settings

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    # TODO нужно это вообще ?
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
        self.logger.info(f"User {payload['user_id']} logged in")
        return payload["user_id"]


# TODO: Сделать все импорты по pep8
