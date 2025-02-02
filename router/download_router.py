import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from auth.auth import JWTBearer
from models.models import UserAnswer, Question

router = APIRouter()

@router.get("/download-responses/", dependencies=[Depends(JWTBearer())])
def download_user_responses(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    """
    Allow users to download their responses in CSV format.
    """
    user_id = JWTBearer.get_user_id_from_token(token)
    
    # Fetch user responses
    responses = db.query(UserAnswer).filter(UserAnswer.user_id == user_id).all()
    
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found")

    # Create a CSV file in memory
    output = StringIO()
    csv_writer = csv.writer(output)
    
    # Write headers
    csv_writer.writerow(["Question", "User Answer", "Is Correct", "Submitted At"])
    
    # Write user responses
    for response in responses:
        question_text = db.query(Question).filter(Question.id == response.question_id).first().text
        csv_writer.writerow([question_text, response.user_answer, response.is_correct, response.submitted_at])
    
    # Prepare response as downloadable CSV
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=user_responses.csv"
    
    return response
