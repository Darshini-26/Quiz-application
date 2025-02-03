from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db,SessionLocal
from service.user import UserService
from schemas.schemas import UserCreate, UserResponse
from auth.auth import JWTBearer
from service.unit_of_work import UnitOfWork

router = APIRouter(prefix="/users", tags=["User"])

def get_uow() -> UnitOfWork:
    # Returning UnitOfWork, assuming it provides access to the necessary repositories.
    return UnitOfWork(SessionLocal)

@router.post("/", response_model=UserResponse,dependencies= [Depends(JWTBearer())])
def create_new_user(user: UserCreate, uow: UnitOfWork = Depends(get_uow)):
    return UserService.create_user( user,uow)

@router.get("/", response_model=list[UserResponse],dependencies= [Depends(JWTBearer())])
def list_users(uow: UnitOfWork = Depends(get_uow)):
    return UserService.get_all_users(uow)

@router.get("/{user_id}", response_model=UserResponse,dependencies= [Depends(JWTBearer())])
def get_user(user_id: str, uow: UnitOfWork = Depends(get_uow)):
    return UserService.get_user_by_id(user_id,uow)