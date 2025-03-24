from sqlalchemy import Column, Integer, String, Text, Enum
from app.infra.database import Base
from app.content.schemas import AccessLevel


class ContentModel(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content_name = Column(String, index=True, nullable=False)
    content_data = Column(Text, nullable=False)
    access_level = Column(
        Enum(AccessLevel),
        default=AccessLevel.REGULAR,
        nullable=False
    )
