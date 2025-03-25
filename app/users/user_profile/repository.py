from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schemas import UserCreateProfileSchema


@dataclass
class UserProfileRepository:
    db_session: AsyncSession

    async def create_user(self, user_body: UserCreateProfileSchema) -> UserProfile:
        query = insert(UserProfile).values(**user_body.model_dump(exclude_unset=True))
        async with self.db_session.begin() as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            return await self.get_user(user_id)
        
    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
            return user
    

        
        