from pydantic import BaseModel, ConfigDict

from app.content.models import AccessLevel


class ContentSchema(BaseModel):
    content_name: str
    content_data: str
    access_level: AccessLevel = AccessLevel.PUBLIC

    model_config = ConfigDict(
        # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.validate_assignment
        arbitrary_types_allowed=True,  # разрешает использовать произвольные типы данных !!!!
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )


class ContentCreate(ContentSchema):
    pass
