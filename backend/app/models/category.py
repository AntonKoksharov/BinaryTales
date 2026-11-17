from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    type: Mapped[str] = mapped_column(String(20), default="expense") # expense | income
    icon: Mapped[str] = mapped_column(String(30), default="tag")
    color: Mapped[str] = mapped_column(String(20), default="#194E9F")
    monthly_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
