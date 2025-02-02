from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
import os
from config.database import get_db
from models.models import UserAnswer
from service.s3_services import upload_to_s3

router = APIRouter()

@router.get("/download/user-responses/{user_id}")
def download_user_responses(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch user responses, convert to CSV, upload to S3, and return the S3 file URL.
    """
    try:
        # Fetch user responses from the database
        user_answers = db.query(UserAnswer).filter(UserAnswer.user_id == user_id).all()

        if not user_answers:
            raise HTTPException(status_code=404, detail="No responses found for the user.")

        # Convert data to a list of dictionaries
        data = [
            {
                "question_id": ans.question_id,
                "answer_text": ans.selected_option_id ,
                "is_correct": ans.is_correct,
        
            }
            for ans in user_answers
        ]

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Save to a CSV file locally
        file_name = f"user_responses_{user_id}.csv"
        df.to_csv(file_name, index=False)

        # Upload to S3
        bucket_name = "quiz-application1"
        file_url = upload_to_s3(file_name, bucket_name)

        # Remove local file after upload
        os.remove(file_name)

        return {"message": "File uploaded successfully", "file_url": file_url}

    except Exception as e:
        if os.path.exists(file_name):
            os.remove(file_name)
        raise HTTPException(status_code=500, detail=f"Failed to upload responses: {str(e)}")
