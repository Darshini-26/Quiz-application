from sqlalchemy.orm import Session
from repository.userquiz_repository import UserQuizRepository
from schemas.schemas import UserQuizCreate

def create_user_quiz(db: Session, user_quiz: UserQuizCreate):
    return UserQuizRepository.create_user_quiz(db, user_quiz)

def get_all_user_quizzes(db: Session):
    return UserQuizRepository.get_all_user_quizzes(db)

def get_user_quiz_by_id(db: Session, user_quiz_id: int):
    return UserQuizRepository.get_user_quiz_by_id(db, user_quiz_id)
