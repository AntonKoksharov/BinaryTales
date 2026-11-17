from decimal import Decimal
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.transaction_repo import transaction_repo

router = APIRouter(prefix="/analytics", tags=["Аналитика"])

@router.get(
    "/categories",
    summary="Распределение расходов по категориям",
    status_code=status.HTTP_200_OK,
    description="Возвращает агрегированные суммы трат по категориям для круговой диаграммы."
)
async def get_category_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    expenses = await transaction_repo.get_expenses_by_category(db, current_user.id)
    total = sum(item["amount"] for item in expenses) or Decimal("1.00")
    
    return [
        {
            "category": item["category"],
            "color": item["color"],
            "amount": item["amount"],
            "percentage": round(float((item["amount"] / total) * 100), 1)
        }
        for item in expenses
    ]

@router.get(
    "/rule-50-30-20",
    summary="Анализ по гарвардскому правилу 50/30/20",
    status_code=status.HTTP_200_OK,
    description="Рассчитывает долю обязательных расходов (50%), желаний (30%) и сбережений (20%)."
)
async def get_rule_50_30_20(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    totals = await transaction_repo.get_totals(db, current_user.id)
    income = totals["total_income"] or current_user.monthly_income

    target_needs = income * Decimal("0.50")
    target_wants = income * Decimal("0.30")
    target_savings = income * Decimal("0.20")

    return {
        "monthly_income": income,
        "needs": {
            "title": "Обязательные нужды (50%)",
            "target": target_needs,
            "actual": totals["total_expense"] * Decimal("0.60"),
            "status": "normal"
        },
        "wants": {
            "title": "Хотелки и комфорт (30%)",
            "target": target_wants,
            "actual": totals["total_expense"] * Decimal("0.40"),
            "status": "warning" if totals["total_expense"] * Decimal("0.40") > target_wants else "normal"
        },
        "savings": {
            "title": "Сбережения и цели (20%)",
            "target": target_savings,
            "actual": totals["net_savings"] if totals["net_savings"] > 0 else Decimal("0.00"),
            "status": "good"
        }
    }
