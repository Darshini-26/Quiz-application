from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import   User, Rating
from config.database import get_db
from schemas.schemas import ReviewCreate
from auth.auth import JWTBearer  # Assuming you're using JWT authentication

router = APIRouter(prefix="/ratings", tags=["Rating"])

@router.post("/")
def submit_review(category_id: int, rating: float, review: str = None, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    user_id = JWTBearer.get_user_id_from_token(token)
    
    # Query the User table to get the user information
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    # Create a new review for the quiz with the extracted user_id
    review = Rating(category_id=category_id, user_id=user.user_id, rating=rating, review=review)
    db.add(review)
    db.commit()
    db.refresh(review)

    return {"message": "Review submitted successfully"}
