from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
    description="Создает пользователя с хэшированием пароля через bcrypt и выдает JWT-токен на 7 дней."
)
async def register(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    return await auth_service.register(db, user_in)

@router.post(
    "/login",
    summary="Вход в систему",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    description="Проверяет логин и пароль, возвращает токен доступа и данные пользователя."
)
async def login(
    login_in: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    return await auth_service.authenticate(db, login_in)

@router.get(
    "/me",
    summary="Профиль текущего пользователя",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    description="Возвращает данные авторизованного пользователя на основе переданного Bearer токена."
)
async def get_me(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    return UserResponse.model_validate(current_user)
