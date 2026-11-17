from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    name: str = Field(..., max_length=50)
    type: str = Field("expense", pattern="^(expense|income)$")
    icon: str = Field("tag", max_length=30)
    color: str = Field("#194E9F", max_length=20)
    monthly_limit: Decimal = Field(Decimal("0.00"), ge=0)

class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None
    monthly_limit: Decimal | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    icon: str
    color: str
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)
