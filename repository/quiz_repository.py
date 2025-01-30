from sqlalchemy.orm import Session
from models.models import Quiz
from schemas.schemas import QuizCreate

class QuizRepository:
    @staticmethod
    def create_quiz(db: Session, quiz: QuizCreate):
        new_quiz = Quiz(title=quiz.title, description=quiz.description)
        db.add(new_quiz)
        db.commit()
        db.refresh(new_quiz)
        return new_quiz

    @staticmethod
    def get_all_quizzes(db: Session):
        return db.query(Quiz).all()

    @staticmethod
    def get_quiz(db: Session, title:str):
        return db.query(Quiz).filter(Quiz.title == title).first()
    
    @staticmethod
    def get_quiz_by_id(db: Session, id:int):
        return db.query(Quiz).filter(Quiz.id == id).first()
