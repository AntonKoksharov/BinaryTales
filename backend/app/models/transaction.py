from datetime import date
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False) # expense | income
    description: Mapped[str] = mapped_column(String(255), default="")
    date: Mapped[date] = mapped_column(Date, default=date.today)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")
