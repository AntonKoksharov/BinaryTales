import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class GoalCreate(BaseModel):
    title: str = Field(..., max_length=100)
    target_amount: Decimal = Field(..., gt=0)
    current_amount: Decimal = Field(Decimal("0.00"), ge=0)
    deadline: Optional[datetime.date] = None
    monthly_payment: Decimal = Field(Decimal("0.00"), ge=0)

class GoalDeposit(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма пополнения копилки")

class GoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    target_amount: Decimal
    current_amount: Decimal
    deadline: Optional[datetime.date]
    monthly_payment: Decimal
    progress_percent: float = 0.0

    model_config = ConfigDict(from_attributes=True)
