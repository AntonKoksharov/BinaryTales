from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Логин пользователя")
    password: str = Field(..., min_length=4, max_length=100, description="Пароль пользователя")
    full_name: str = Field("", max_length=100, description="Имя пользователя")

class UserLogin(BaseModel):
    username: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    balance: Decimal
    monthly_income: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
