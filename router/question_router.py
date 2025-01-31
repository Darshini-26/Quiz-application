from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from service.question_services import QuestionService
from schemas.schemas import QuestionCreate, QuestionResponse
from auth.auth import JWTBearer
from typing import List

question_router = APIRouter()

@question_router.post("/{quiz_id}/", response_model=QuestionResponse,dependencies= [Depends(JWTBearer(admin_required=True))])
def create_question(quiz_id: int, question_body: QuestionCreate, db: Session = Depends(get_db)):
    """
    Create a question for the given quiz_id.
    """
    try:
        question = QuestionService.create_question(db, quiz_id, question_body.text)
        return question
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# @question_router.get("/", response_model=list[QuestionResponse],dependencies= [Depends(JWTBearer())])
# def list_questions(db: Session = Depends(get_db)):
#     return QuestionService.get_all_questions(db)

@question_router.get("/{quiz_id}", response_model=list[QuestionResponse],dependencies= [Depends(JWTBearer(admin_required=True))])
def get_question(quiz_id: int, db: Session = Depends(get_db)):
    return QuestionService.get_questions_by_quizid(db, quiz_id)

@question_router.get("/quiz/{quiz_id}/random-questions",dependencies= [Depends(JWTBearer())])
def get_quiz_questions(quiz_id: int, num_questions: int = 5, db: Session = Depends(get_db)):
    # Fetch random questions with options from the service layer
    questions =  QuestionService.fetch_random_questions_for_quiz(db, quiz_id, num_questions)
    return questions