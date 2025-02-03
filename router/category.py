from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.category import CategoryService
from config.database import get_db, SessionLocal
from schemas.schemas import CategoryCreate, CategoryResponse  # Assuming CategoryResponse exists for GET responses
from typing import List
from service.unit_of_work import UnitOfWork
from auth.auth import JWTBearer


router = APIRouter(prefix="/categories", tags=["Category"])

def get_uow() -> UnitOfWork:
    # Returning UnitOfWork, assuming it provides access to the necessary repositories.
    return UnitOfWork(SessionLocal)

@router.post("/", response_model=CategoryResponse,dependencies= [Depends(JWTBearer())])  # Change to CategoryResponse for better structure
def create_category(category: CategoryCreate, uow: UnitOfWork = Depends(get_uow)):
    try:
        # This should call the appropriate service method to handle category creation
        return CategoryService.create_category_service(uow, category)
    except Exception as e:
        # Raising HTTPException in case of failure
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CategoryResponse],dependencies= [Depends(JWTBearer())])  # Assuming you have a response model for multiple categories
def read_categories(uow: UnitOfWork = Depends(get_uow)):
    # Retrieve all categories via service layer
    return CategoryService.get_all_categories_service(uow)

@router.get("/{category_title}", response_model=CategoryResponse,dependencies= [Depends(JWTBearer())])
def read_category(category_title: str, uow: UnitOfWork = Depends(get_uow)):
    try:
        # Retrieve category by title via service layer
        return CategoryService.get_category_by_title_service(uow, category_title)
    except Exception as e:
        # Handle failure to find category
        raise HTTPException(status_code=404, detail=str(e))
