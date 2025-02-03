from fastapi import HTTPException
from .unit_of_work import UnitOfWork  
from models.models import Rating
from directory.rating_submits import RatingSubmits

class ReviewService:
    def __init__(self, uow: UnitOfWork):  # Accepts uow as a parameter
        self.uow = uow
        self.review_repository = RatingSubmits(uow)  # Repository for handling reviews

    def submit_review(self, category_id: int, rating: float, review: str, user_id: int):
        """Submits a review and commits it to the database."""

        # Validate the rating
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

        # Create the review object
        review = Rating(
            category_id=category_id, 
            user_id=user_id, 
            rating=rating, 
            review=review
        )

        # Use the repository to add the review
        self.review_repository.add(review)

        # Commit the transaction
        self.uow.commit()

        # Refresh the review object (if needed)
        self.uow.session.refresh(review)  

        return {"message": "Review submitted successfully", "review_id": review.id}
