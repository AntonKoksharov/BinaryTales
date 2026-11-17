from datetime import date
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    target_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    current_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    monthly_payment: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0.00"))

    user = relationship("User", back_populates="goals")
