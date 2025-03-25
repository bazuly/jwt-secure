from enum import Enum
from datetime import datetime

from sqlalchemy import Integer, String, Text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.database import Base


class AccessLevel(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    RESTRICTED = "restricted"
    SECRET = "secret"


class ContentModel(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    content_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content_data: Mapped[str] = mapped_column(Text, nullable=False)
    access_level: Mapped[AccessLevel] = mapped_column(
        SQLAlchemyEnum(AccessLevel, name="access_level_enum"), 
        default=AccessLevel.PUBLIC, 
        nullable=False
    )

