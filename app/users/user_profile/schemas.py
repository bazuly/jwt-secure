from pydantic import BaseModel, ConfigDict

from app.content.models import AccessLevel


class UserCreateProfileSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    access_level: AccessLevel = AccessLevel.PUBLIC

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )
