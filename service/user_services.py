from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from schemas.schemas import UserCreate

def create_user(db: Session, user: UserCreate):
    return UserRepository.create_user(db, user)

def get_all_users(db: Session):
    return UserRepository.get_all_users(db)

def get_user_by_id(db: Session, user_id: str):
    return UserRepository.get_user_by_id(db, user_id)
