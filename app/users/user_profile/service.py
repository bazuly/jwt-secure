from dataclasses import dataclass

from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserProfileRepository
from app.users.user_profile.schemas import UserCreateProfileSchema, UserLoginSchema


@dataclass
class UserService:
    user_repository: UserProfileRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user_data_create = UserCreateProfileSchema(
            username=username, password=password)
        user = await self.user_repository.create_user(user_data_create)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
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
