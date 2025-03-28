from dataclasses import dataclass

from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.schemas import UserCreateProfileSchema, UserLoginSchema
from app.users.auth.jwt import JWTHandler


@dataclass
class UserService:
    user_repository: UserProfileRepository
    auth_service: AuthService
    jwt_handler: JWTHandler

    async def create_user(
        self,
        username: str,
        password: str,
        access_level: str
    ) -> UserLoginSchema:
        user_data_create = UserCreateProfileSchema(
            username=username, password=password, access_level=access_level
        )
        user = await self.user_repository.create_user(user_data_create)
        access_token = await self.jwt_handler.create_access_token(subject=user.id)
        # print(user)
        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )

    async def login_user(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self.auth_service._validate_auth_user(
            user=user,
            password=password,
        )
