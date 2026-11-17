from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.transaction import Transaction
from app.repositories.transaction_repo import transaction_repo
from app.repositories.user_repo import user_repo
from app.schemas.transaction import TransactionCreate, TransactionSummary

class TransactionService:
    async def create_transaction(
        self,
        db: AsyncSession,
        user: User,
        tx_in: TransactionCreate
    ) -> Transaction:
        # Создаем запись о транзакции
        tx = await transaction_repo.create(db, user.id, tx_in)

        # Автоматически обновляем баланс пользователя
        delta = tx_in.amount if tx_in.type == "income" else -tx_in.amount
        await user_repo.update_balance(db, user.id, delta)

        return tx

    async def get_summary(self, db: AsyncSession, user: User) -> TransactionSummary:
        totals = await transaction_repo.get_totals(db, user.id)
        # Если баланс пользователя еще не изменен транзакциями, берем из профиля
        effective_balance = user.balance

        return TransactionSummary(
            total_balance=effective_balance,
            total_income=totals["total_income"] or user.monthly_income,
            total_expense=totals["total_expense"],
            saved_amount=totals["net_savings"] if totals["net_savings"] > 0 else Decimal("0.00")
        )

transaction_service = TransactionService()
