from sqlalchemy.orm import Session
from models.models import UserQuiz
from schemas.schemas import UserQuizCreate

class UserQuizRepository:
    @staticmethod
    def create_user_quiz(db: Session, user_quiz: UserQuizCreate):
        new_user_quiz = UserQuiz(user_id=user_quiz.user_id, quiz_id=user_quiz.quiz_id, score=user_quiz.score)
        db.add(new_user_quiz)
        db.commit()
        db.refresh(new_user_quiz)
        return new_user_quiz

    @staticmethod
    def get_all_user_quizzes(db: Session):
        return db.query(UserQuiz).all()

    @staticmethod
    def get_user_quiz_by_id(db: Session, user_quiz_id: int):
        return db.query(UserQuiz).filter(UserQuiz.id == user_quiz_id).first()
