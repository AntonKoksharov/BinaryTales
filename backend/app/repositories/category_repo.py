from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate

DEFAULT_CATEGORIES = [
    {"name": "Продукты", "type": "expense", "icon": "shopping-cart", "color": "#11C438", "monthly_limit": Decimal("15000.00")},
    {"name": "Транспорт", "type": "expense", "icon": "car", "color": "#F59E0B", "monthly_limit": Decimal("5000.00")},
    {"name": "Кафе и рестораны", "type": "expense", "icon": "coffee", "color": "#EC4899", "monthly_limit": Decimal("5000.00")},
    {"name": "ЖКХ и аренда", "type": "expense", "icon": "home", "color": "#194E9F", "monthly_limit": Decimal("25000.00")},
    {"name": "Развлечения", "type": "expense", "icon": "film", "color": "#8B5CF6", "monthly_limit": Decimal("6000.00")},
    {"name": "Подписки", "type": "expense", "icon": "repeat", "color": "#06B6D4", "monthly_limit": Decimal("2000.00")},
    {"name": "Здоровье", "type": "expense", "icon": "heart", "color": "#EF4444", "monthly_limit": Decimal("4000.00")},
    {"name": "Одежда и обувь", "type": "expense", "icon": "tag", "color": "#10B981", "monthly_limit": Decimal("7000.00")},
    {"name": "Зарплата", "type": "income", "icon": "dollar-sign", "color": "#11C438", "monthly_limit": Decimal("0.00")},
]

class CategoryRepository:
    async def get_all_by_user(self, db: AsyncSession, user_id: int) -> list[Category]:
        result = await db.execute(
            select(Category).where((Category.user_id == user_id) | (Category.user_id.is_(None)))
        )
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, category_id: int) -> Category | None:
        result = await db.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_id: int, cat_in: CategoryCreate) -> Category:
        category = Category(
            user_id=user_id,
            name=cat_in.name,
            type=cat_in.type,
            icon=cat_in.icon,
            color=cat_in.color,
            monthly_limit=cat_in.monthly_limit
        )
        db.add(category)
        await db.flush()
        await db.refresh(category)
        return category

    async def create_default_categories(self, db: AsyncSession, user_id: int) -> None:
        for cat in DEFAULT_CATEGORIES:
            new_cat = Category(
                user_id=user_id,
                name=cat["name"],
                type=cat["type"],
                icon=cat["icon"],
                color=cat["color"],
                monthly_limit=cat["monthly_limit"]
            )
            db.add(new_cat)
        await db.flush()

category_repo = CategoryRepository()
