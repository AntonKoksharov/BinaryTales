from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repo import user_repo
from app.repositories.category_repo import category_repo
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse

class AuthService:
    async def register(self, db: AsyncSession, user_in: UserRegister) -> TokenResponse:
        existing = await user_repo.get_by_username(db, user_in.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким логином уже зарегистрирован"
            )

        pwd_hash = hash_password(user_in.password)
        user = await user_repo.create(db, user_in, pwd_hash)
        
        # Создаем базовые категории расходов для нового пользователя
        await category_repo.create_default_categories(db, user.id)

        token = create_access_token(user.id, user.username)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

    async def authenticate(self, db: AsyncSession, login_in: UserLogin) -> TokenResponse:
        user = await user_repo.get_by_username(db, login_in.username)
        if not user or not verify_password(login_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль"
            )

        token = create_access_token(user.id, user.username)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )

auth_service = AuthService()
