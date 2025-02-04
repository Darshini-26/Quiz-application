from sqlalchemy.orm import Session
from models.models import Category
from schemas.schemas import CategoryCreate

class CategoryTypes:
    def __init__(self, session: Session):
        self.session = session

    def create_category(self, category: CategoryCreate):
        # Convert CategoryCreate Pydantic model to SQLAlchemy Category model
        category_data = Category(**category.dict())  # Create SQLAlchemy model instance
        self.session.add(category_data)
        self.session.commit()
        self.session.refresh(category_data)  # Refresh to get the updated object
        return category_data

    @staticmethod
    def get_all_category(session: Session):  # Remove 'self' and accept session argument
        return session.query(Category).all()

    @staticmethod
    def get_category_by_title(session: Session, title: str):  # Remove 'self' and accept session argument
        return session.query(Category).filter(Category.title == title).first()
