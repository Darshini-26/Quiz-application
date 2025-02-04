# review_repository.py
from sqlalchemy.orm import Session
from models.models import Rating

class RatingSubmits:
    def __init__(self, session: Session):
        self.session = session

    def add(self, review: Rating):
        self.session.add(review)
    
    def refresh(self, review: Rating):
        self.session.refresh(review)
