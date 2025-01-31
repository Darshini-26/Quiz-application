from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from service.quiz_services import create_quiz, get_all_quizzes, get_quiz_by_title,get_random_questions
from schemas.schemas import QuizCreate, QuizResponse,QuizQuestionResponse
from auth.auth import JWTBearer

quiz_router = APIRouter()

@quiz_router.post("/", response_model=QuizResponse,dependencies=[Depends(JWTBearer(admin_required=True))])
def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    return create_quiz(db, quiz)

@quiz_router.get("/", response_model=list[QuizResponse],dependencies= [Depends(JWTBearer())])
def list_quizzes(db: Session = Depends(get_db)):
    return get_all_quizzes(db)

@quiz_router.get("/{title}", response_model=QuizResponse,dependencies= [Depends(JWTBearer())])
def get_quiz(title:str, db: Session = Depends(get_db)):
    return get_quiz_by_title(db, title)

