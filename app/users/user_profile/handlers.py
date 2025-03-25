from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependency import get_user_service
from app.users.user_profile.schemas import UserLoginSchema, UserCreateProfileSchema
from app.users.user_profile.service import UserService

router = APIRouter(prefix="/users", tags=['users'])


@router.post(
    "/create_user",
    response_model=UserLoginSchema
)
async def create_user(
        body: UserCreateProfileSchema,
        user_repository: Annotated[UserService, Depends(get_user_service)]
):
    return await user_repository.create_user(
        username=body.username,
        password=body.password
    )

@router.get(
    "/login",
    response_model=UserLoginSchema
)
async def login_user(
    body: UserLoginSchema,
    user_repository: Annotated[UserService, Depends(get_user_service)]
):
    return await user_repository.login_user(
        username=body.username,
        password=body.password
    )