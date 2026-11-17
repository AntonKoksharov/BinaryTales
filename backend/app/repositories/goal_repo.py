from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.goal import Goal
from app.schemas.goal import GoalCreate

class GoalRepository:
    async def get_all(self, db: AsyncSession, user_id: int) -> list[Goal]:
        result = await db.execute(select(Goal).where(Goal.user_id == user_id))
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, goal_id: int, user_id: int) -> Goal | None:
        result = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_id: int, goal_in: GoalCreate) -> Goal:
        goal = Goal(
            user_id=user_id,
            title=goal_in.title,
            target_amount=goal_in.target_amount,
            current_amount=goal_in.current_amount,
            deadline=goal_in.deadline,
            monthly_payment=goal_in.monthly_payment
        )
        db.add(goal)
        await db.flush()
        await db.refresh(goal)
        return goal

    async def deposit(self, db: AsyncSession, goal: Goal, amount: Decimal) -> Goal:
        goal.current_amount = goal.current_amount + amount
        await db.flush()
        await db.refresh(goal)
        return goal

goal_repo = GoalRepository()
