from fastapi import HTTPException
from models.models import Category
from schemas.schemas import CategoryCreate
from .unit_of_work import UnitOfWork

class CategoryService:
    @staticmethod  # Use staticmethod decorator
    def create_category_service(uow: UnitOfWork, category: CategoryCreate):
        with uow:
            # Ensure you are passing the Pydantic model to the repository method for creation
            return uow.categories.create_category(category)

    @staticmethod  # Use staticmethod decorator
    def get_all_categories_service(uow: UnitOfWork):
        with uow:
            return uow.categories.get_all_category(uow._session)

    @staticmethod  # Use staticmethod decorator
    def get_category_by_title_service(uow: UnitOfWork, title: str):
        with uow:
            category = uow.categories.get_category_by_title(uow._session,title)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")  # Handle 404 error
            return category
