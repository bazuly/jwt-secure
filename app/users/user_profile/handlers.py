from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependency import get_user_service, get_auth_service
from app.users.user_profile.schemas import UserCreateProfileSchema
from app.users.auth.schemas import AuthResponseSchema
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthService

router = APIRouter(prefix="/users", tags=['users'])


@router.post("/register", response_model=AuthResponseSchema)
async def register(
    user_data: UserCreateProfileSchema,
    user_service: UserService = Depends(get_user_service)
):
    """
    Register endpoint that creates a new user and returns JWT access token.
    """
    # TODO: убрать принты
    print(f"Creating user with access level: {user_data.access_level}")
    result = await user_service.create_user(
        username=user_data.username,
        password=user_data.password,
        access_level=user_data.access_level
    )
    print(f"Created user with ID: {result.user_id}")
    return result


@router.post("/login", response_model=AuthResponseSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Login endpoint that returns JWT access token.
    """
    return await auth_service.login_user(
        username=form_data.username,
        password=form_data.password
    )
