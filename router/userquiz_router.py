from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from service.userquiz_services import create_user_quiz, get_all_user_quizzes, get_user_quiz_by_id
from schemas.schemas import UserQuizCreate, UserQuizResponse
from auth.auth import JWTBearer

user_quiz_router = APIRouter()

@user_quiz_router.post("/", response_model=UserQuizResponse,dependencies= [Depends(JWTBearer())])
def create_new_user_quiz(user_quiz: UserQuizCreate, db: Session = Depends(get_db)):
    return create_user_quiz(db, user_quiz)

@user_quiz_router.get("/", response_model=list[UserQuizResponse],dependencies= [Depends(JWTBearer())])
def list_user_quizzes(db: Session = Depends(get_db)):
    return get_all_user_quizzes(db)

@user_quiz_router.get("/{user_quiz_id}", response_model=UserQuizResponse,dependencies= [Depends(JWTBearer())])
def get_user_quiz(user_quiz_id: int, db: Session = Depends(get_db)):
    return get_user_quiz_by_id(db, user_quiz_id)
