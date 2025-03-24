from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models import ContentModel
from app.content.schemas import ContentSchema
from app.logger import logger


class ContentRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.logger = logger

    async def create_content(
        self,
        content_body: ContentSchema,
    ) -> Optional[ContentModel]:
        query = insert(ContentModel).values(
            content_name=content_body.content_name,
            content_data=content_body.content_data,
            access_level=content_body.access_level
        ).returning(ContentModel)
        async with self.db_session as session:
            try:
                result = await session.execute(query)
                await session.commit()
                added_content = result.scalar_one_or_none()
                self.logger.info(
                    "Content added successfully"
                )
                return added_content
            except SQLAlchemyError as e:
                await self.db_session.rollback()
                self.logger.error(
                    "Content creation error: %s", str(e),
                    exc_info=True, stack_info=True
                )
                raise

    async def retrieve_content(
        self,
        content_id: int,
    ) -> Optional[ContentModel]:
        query = select(ContentModel).where(ContentModel.id == content_id)

        try:
            result = await self.db_session.execute(query)
            content = result.scalar_one_or_none()

            if content:
                self.logger.debug("Content found: ID %d", content_id)
            else:
                self.logger.warning("Content not found: ID %d", content_id)

            return content

        except SQLAlchemyError as e:
            self.logger.error(
                "Content retrieval error: %s", str(e),
                exc_info=True, stack_info=True
            )
            raise
