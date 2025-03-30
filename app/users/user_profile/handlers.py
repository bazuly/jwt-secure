import logging
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependency import get_user_service, get_auth_service
from app.users.user_profile.schemas import UserCreateProfileSchema
from app.users.auth.schemas import AuthResponseSchema
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthService

router = APIRouter(prefix="/users", tags=['users'])

logger = logging.getLogger(__name__)


@router.post("/register", response_model=AuthResponseSchema)
async def register(
    user_data: UserCreateProfileSchema,
    user_service: UserService = Depends(get_user_service)
) -> AuthResponseSchema:
    try:
        result = await user_service.create_user(
            username=user_data.username,
            password=user_data.password,
            access_level=user_data.access_level
        )
        return result
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise


@router.post("/login", response_model=AuthResponseSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> AuthResponseSchema:

    return await auth_service.login_user(
        username=form_data.username,
        password=form_data.password
    )
