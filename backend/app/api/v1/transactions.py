from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.transaction_repo import transaction_repo
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionSummary
from app.services.transaction_service import transaction_service

router = APIRouter(prefix="/transactions", tags=["Операции"])

@router.get(
    "/summary",
    summary="Сводные финансовые показатели пользователя",
    status_code=status.HTTP_200_OK,
    response_model=TransactionSummary,
    description="Возвращает общий баланс, доходы за месяц, расходы и сумму сбережений для верхних карточек дашборда."
)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TransactionSummary:
    return await transaction_service.get_summary(db, current_user)

@router.get(
    "",
    summary="Список операций пользователя",
    status_code=status.HTTP_200_OK,
    response_model=list[TransactionResponse],
    description="Возвращает журнал расходов и доходов с возможностью фильтрации по категории и типу."
)
async def get_transactions(
    category_id: int | None = Query(None, description="Фильтр по ID категории"),
    type: str | None = Query(None, pattern="^(expense|income)$", description="Фильтр по типу (expense/income)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[TransactionResponse]:
    transactions = await transaction_repo.get_all(
        db,
        user_id=current_user.id,
        category_id=category_id,
        tx_type=type,
        limit=limit,
        offset=offset
    )
    return [TransactionResponse.model_validate(tx) for tx in transactions]

@router.post(
    "",
    summary="Создание новой операции",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionResponse,
    description="Добавляет операцию в журнал и автоматически обновляет баланс текущего пользователя."
)
async def create_transaction(
    tx_in: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TransactionResponse:
    tx = await transaction_service.create_transaction(db, current_user, tx_in)
    return TransactionResponse.model_validate(tx)
