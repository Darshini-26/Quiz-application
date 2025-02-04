from sqlalchemy.orm import Session
from models.models import User
from schemas.schemas import UserCreate
import uuid

class UserList:
    def __init__(self, session: Session):
        self.session = session

    
    def create_user(self, user: UserCreate):
        new_user = User(
            user_id=uuid.uuid4(),
            name=user.name,
            email=user.email,
            hashed_password=user.password,
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    
    def get_all_users(session: Session):
        return session.query(User).all()

    
    def get_user_by_id(session: Session, user_id: str):
        return session.query(User).filter(User.user_id == user_id).first()