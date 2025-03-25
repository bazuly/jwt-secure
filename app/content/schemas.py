from pydantic import BaseModel, ConfigDict

from app.content.models import AccessLevel


class ContentBase(BaseModel):
    title: str
    content: str
    access_level: AccessLevel = AccessLevel.PUBLIC

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )


class ContentCreate(ContentBase):
    pass


class ContentSchema(ContentBase):
    id: int
    created_by: int


    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )
