from pydantic import BaseModel


class UserCreateProfileSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str
