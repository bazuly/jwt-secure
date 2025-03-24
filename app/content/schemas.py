from enum import Enum

from pydantic import BaseModel


class AccessLevel(str, Enum):
    REGULAR = "regular"
    SECRET = "secret"
    ADMIN = "admin"


class ContentSchema(BaseModel):
    id: int
    content_name: str
    content_data: str
    access_level: AccessLevel = AccessLevel.REGULAR

    class Config:
        from_attributes = True
