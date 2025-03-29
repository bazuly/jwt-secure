from pydantic import BaseModel, ConfigDict


class AuthResponseSchema(BaseModel):
    user_id: int
    access_token: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )
