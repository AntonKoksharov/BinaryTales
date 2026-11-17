import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.category import CategoryResponse

class TransactionCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма операции (строго больше 0)")
    type: str = Field(..., pattern="^(expense|income)$", description="Тип: expense или income")
    category_id: Optional[int] = Field(None, description="ID категории")
    description: str = Field("", max_length=255, description="Описание или название заведения")
    date: Optional[datetime.date] = Field(default_factory=datetime.date.today, description="Дата операции")

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(expense|income)$")
    category_id: Optional[int] = None
    description: Optional[str] = None
    date: Optional[datetime.date] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    category_id: Optional[int]
    amount: Decimal
    type: str
    description: str
    date: datetime.date
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)

class TransactionSummary(BaseModel):
    total_balance: Decimal
    total_income: Decimal
    total_expense: Decimal
    saved_amount: Decimal
