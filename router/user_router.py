from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from service.user_services import create_user, get_user_by_id, get_all_users
from schemas.schemas import UserCreate, UserResponse
from auth.auth import JWTBearer

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse,dependencies= [Depends(JWTBearer())])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@user_router.get("/", response_model=list[UserResponse],dependencies= [Depends(JWTBearer())])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

@user_router.get("/{user_id}", response_model=UserResponse,dependencies= [Depends(JWTBearer())])
def get_user(user_id: str, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)
