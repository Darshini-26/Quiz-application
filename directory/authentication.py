from sqlalchemy.orm import Session
from models.models import User

class UserRepository:
    @staticmethod
    def get_user_by_name(db: Session, name: str):
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
