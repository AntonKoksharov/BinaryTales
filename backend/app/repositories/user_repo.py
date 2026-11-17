from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserRegister

class UserRepository:
    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_in: UserRegister, password_hash: str) -> User:
        user = User(
            username=user_in.username,
            password_hash=password_hash,
            full_name=user_in.full_name,
            balance=Decimal("125450.00"),
            monthly_income=Decimal("80000.00")
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def update_balance(self, db: AsyncSession, user_id: int, delta: Decimal) -> None:
        user = await self.get_by_id(db, user_id)
        if user:
            user.balance = user.balance + delta
            await db.flush()

user_repo = UserRepository()
