from dataclasses import dataclass

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schemas import UserCreateProfileSchema


@dataclass
class UserProfileRepository:
    db_session: AsyncSession

    async def create_user(self, user_body: UserCreateProfileSchema) -> UserProfile:
        try:
            user_data = user_body.dict(exclude_none=True)
            if "password" in user_data:
                user_data["password"] = user_body.get_hashed_password()

            query = insert(UserProfile).values(
                user_data).returning(UserProfile.id)
            user_id: int = (await self.db_session.execute(query)).scalar()
            await self.db_session.commit()

            user = await self.get_user_by_id(user_id)
            return user
        except Exception as e:
            await self.db_session.rollback()
            raise

    async def get_user_by_id(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        user = (await self.db_session.execute(query)).scalar_one_or_none()
        return user

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        user = (await self.db_session.execute(query)).scalar_one_or_none()
        return user

    async def update_user(self, user_id: int, user_body: UserCreateProfileSchema) -> UserProfile:
        user_data = user_body.dict(exclude_none=True)
        if "password" in user_data:
            user_data["password"] = user_body.get_hashed_password()

        query = update(UserProfile).where(UserProfile.id == user_id).values(
            user_data).returning(UserProfile.id)
        user_id: int = (await self.db_session.execute(query)).scalar()
        await self.db_session.commit()
        return await self.get_user_by_id(user_id)
