from sqlalchemy.orm import Session
from models.models import User
from schemas.schemas import UserCreate
import uuid

class UserRepository:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        new_user = User(
            user_id=uuid.uuid4(),
            name=user.name,
            email=user.email,
            hashed_password=user.password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_all_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str):
        return db.query(User).filter(User.user_id == user_id).first()
