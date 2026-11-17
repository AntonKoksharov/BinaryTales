from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.repositories.category_repo import category_repo
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Категории"])

@router.get(
    "",
    summary="Список категорий пользователя",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoryResponse],
    description="Возвращает системные и персональные категории пользователя с их лимитами и цветами."
)
async def get_categories(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[CategoryResponse]:
    categories = await category_repo.get_all_by_user(db, current_user.id)
    return [CategoryResponse.model_validate(c) for c in categories]

@router.post(
    "",
    summary="Создание новой категории",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponse
)
async def create_category(
    cat_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> CategoryResponse:
    category = await category_repo.create(db, current_user.id, cat_in)
    return CategoryResponse.model_validate(category)
