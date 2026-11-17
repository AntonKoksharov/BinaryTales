from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.goal_repo import goal_repo
from app.repositories.user_repo import user_repo
from app.schemas.goal import GoalCreate, GoalDeposit, GoalResponse

router = APIRouter(prefix="/goals", tags=["Цели и копилки"])

@router.get(
    "",
    summary="Список финансовых целей",
    status_code=status.HTTP_200_OK,
    response_model=list[GoalResponse]
)
async def get_goals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[GoalResponse]:
    goals = await goal_repo.get_all(db, current_user.id)
    responses = []
    for g in goals:
        progress = float((g.current_amount / g.target_amount) * 100) if g.target_amount > 0 else 0.0
        resp = GoalResponse(
            id=g.id,
            user_id=g.user_id,
            title=g.title,
            target_amount=g.target_amount,
            current_amount=g.current_amount,
            deadline=g.deadline,
            monthly_payment=g.monthly_payment,
            progress_percent=round(min(progress, 100.0), 1)
        )
        responses.append(resp)
    return responses

@router.post(
    "",
    summary="Создание новой финансовой цели",
    status_code=status.HTTP_201_CREATED,
    response_model=GoalResponse
)
async def create_goal(
    goal_in: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GoalResponse:
    goal = await goal_repo.create(db, current_user.id, goal_in)
    progress = float((goal.current_amount / goal.target_amount) * 100) if goal.target_amount > 0 else 0.0
    return GoalResponse(
        id=goal.id,
        user_id=goal.user_id,
        title=goal.title,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        deadline=goal.deadline,
        monthly_payment=goal.monthly_payment,
        progress_percent=round(min(progress, 100.0), 1)
    )

@router.post(
    "/{goal_id}/deposit",
    summary="Пополнение финансовой цели",
    status_code=status.HTTP_200_OK,
    response_model=GoalResponse,
    description="Увеличивает накопленную сумму цели и списывает средства с баланса пользователя."
)
async def deposit_to_goal(
    goal_id: int,
    deposit_in: GoalDeposit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GoalResponse:
    goal = await goal_repo.get_by_id(db, goal_id, current_user.id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Цель не найдена")

    # Списываем сумму с баланса и зачисляем в копилку
    await user_repo.update_balance(db, current_user.id, -deposit_in.amount)
    updated_goal = await goal_repo.deposit(db, goal, deposit_in.amount)

    progress = float((updated_goal.current_amount / updated_goal.target_amount) * 100) if updated_goal.target_amount > 0 else 0.0
    return GoalResponse(
        id=updated_goal.id,
        user_id=updated_goal.user_id,
        title=updated_goal.title,
        target_amount=updated_goal.target_amount,
        current_amount=updated_goal.current_amount,
        deadline=updated_goal.deadline,
        monthly_payment=updated_goal.monthly_payment,
        progress_percent=round(min(progress, 100.0), 1)
    )
