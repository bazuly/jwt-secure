from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schemas import UserCreateProfileSchema


@dataclass
class UserProfileRepository:
    db_session: AsyncSession

    async def create_user(self, user_body: UserCreateProfileSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user_body.dict(exclude_none=True)).returning(UserProfile.id)

        user_id: int = (await self.db_session.execute(query)).scalar()
        return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        user = (await self.db_session.execute(query)).scalar_one_or_none()
        return user

    async def update_user(self, user_id: int, user_body: UserCreateProfileSchema) -> UserProfile:
        query = update(UserProfile).where(UserProfile.id == user_id).values(
            **user_body.dict(exclude_none=True)).returning(UserProfile.id)

        user_id: int = (await self.db_session.execute(query)).scalar()
        return await self.get_user(user_id)
