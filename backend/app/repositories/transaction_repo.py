from datetime import date
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

class TransactionRepository:
    async def get_all(
        self,
        db: AsyncSession,
        user_id: int,
        category_id: int | None = None,
        tx_type: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[Transaction]:
        stmt = (
            select(Transaction)
            .options(selectinload(Transaction.category))
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.date.desc(), Transaction.id.desc())
        )
        if category_id:
            stmt = stmt.where(Transaction.category_id == category_id)
        if tx_type:
            stmt = stmt.where(Transaction.type == tx_type)
        
        stmt = stmt.limit(limit).offset(offset)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, user_id: int, tx_in: TransactionCreate) -> Transaction:
        tx = Transaction(
            user_id=user_id,
            category_id=tx_in.category_id,
            amount=tx_in.amount,
            type=tx_in.type,
            description=tx_in.description,
            date=tx_in.date or date.today()
        )
        db.add(tx)
        await db.flush()
        await db.refresh(tx, attribute_names=["category"])
        return tx

    async def get_totals(self, db: AsyncSession, user_id: int) -> dict[str, Decimal]:
        """Расчет общей суммы доходов и расходов пользователя"""
        income_stmt = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.type == "income"
        )
        expense_stmt = select(func.coalesce(func.sum(Transaction.amount), 0)).where(
            Transaction.user_id == user_id,
            Transaction.type == "expense"
        )
        
        income_res = await db.execute(income_stmt)
        expense_res = await db.execute(expense_stmt)
        
        total_income = Decimal(str(income_res.scalar() or 0))
        total_expense = Decimal(str(expense_res.scalar() or 0))
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_savings": total_income - total_expense
        }

    async def get_expenses_by_category(self, db: AsyncSession, user_id: int) -> list[dict]:
        """Агрегация расходов по категориям для круговой диаграммы"""
        from app.models.category import Category
        stmt = (
            select(
                Category.name,
                Category.color,
                func.coalesce(func.sum(Transaction.amount), 0).label("total")
            )
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id, Transaction.type == "expense")
            .group_by(Category.name, Category.color)
        )
        result = await db.execute(stmt)
        return [{"category": row[0], "color": row[1], "amount": Decimal(str(row[2]))} for row in result.all()]

transaction_repo = TransactionRepository()
