from pydantic import BaseModel, ConfigDict

from app.content.models import AccessLevel
from app.users.user_profile.password import get_password_hash


class UserCreateProfileSchema(BaseModel):
    username: str | None = None
    password: str | None = None
    access_level: AccessLevel = AccessLevel.PUBLIC

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True,
        use_enum_values=True
    )

    # хэширование пароля
    def get_hashed_password(self) -> str | None:
        if self.password:
            return get_password_hash(self.password)
        return None
