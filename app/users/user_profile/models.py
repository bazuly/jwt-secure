from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum

from app.infra.database import Base
from app.content.models import AccessLevel


class UserProfile(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    access_level: Mapped[AccessLevel] = mapped_column(
        SQLAlchemyEnum(AccessLevel, name="access_level_enum"),
        default=AccessLevel.PUBLIC,
        nullable=False
    )
