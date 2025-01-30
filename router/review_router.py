from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import  Quiz,Review,User
from config.database import get_db
from schemas.schemas import ReviewCreate
from auth.auth import JWTBearer  # Assuming you're using JWT authentication

review_router = APIRouter()

@review_router.post("/")
def submit_review(quiz_id: int, rating: float, feedback: str = None, db: Session = Depends(get_db), token: str = Depends(JWTBearer())):
    # Extract the user_id from the JWT token directly using get_user_id_from_token
    user_id = JWTBearer.get_user_id_from_token(token)
    
    # Query the User table to get the user information
    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    # Create a new review for the quiz with the extracted user_id
    review = Review(quiz_id=quiz_id, user_id=user.user_id, rating=rating, feedback=feedback)
    db.add(review)
    db.commit()
    db.refresh(review)

    return {"message": "Review submitted successfully"}