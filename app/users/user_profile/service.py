from dataclasses import dataclass

from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.schemas import UserCreateProfileSchema
from app.users.auth.schemas import AuthResponseSchema
from app.users.auth.jwt import JWTHandler
from app.content.models import AccessLevel


@dataclass
class UserService:
    user_repository: UserProfileRepository
    auth_service: AuthService
    jwt_handler: JWTHandler

    async def create_user(
        self,
        username: str,
        password: str,
        access_level: AccessLevel
    ) -> AuthResponseSchema:
        user_data_create = UserCreateProfileSchema(
            username=username, password=password, access_level=access_level
        )
        user = await self.user_repository.create_user(user_data_create)
        access_token = await self.jwt_handler.create_access_token(subject=user.id)
        # print(user)
        return AuthResponseSchema(
            user_id=user.id,
            access_token=access_token
        )
