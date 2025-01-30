from sqlalchemy.orm import Session,joinedload, contains_eager,selectinload
from models.models import Question,Option
from schemas.schemas import QuestionCreate
import random
from sqlalchemy.sql import func


class QuestionRepository:
    @staticmethod
    def create_question(db: Session, quiz_id: int, text: str):
        print(f"📌 Received quiz_id: {quiz_id}")  # Debugging log
        max_id = db.query(Question.id).filter(Question.quiz_id == quiz_id).order_by(Question.id.desc()).first()
        next_id = max_id[0] + 1 if max_id else 1

        new_question = Question(text=text, quiz_id=quiz_id)  # ✅ Let the database handle id



        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        print(f"✅ After refresh: {new_question.quiz_id}")  # Debugging log

        return new_question





    @staticmethod
    def get_all_questions(db: Session):
        return db.query(Question).all()

    @staticmethod
    def get_questions_by_id(db: Session, quiz_id: int):
        return db.query(Question).filter(Question.quiz_id == quiz_id).all()
    
    
    @staticmethod
    def get_question_by_quiz_and_id(db: Session, quiz_id: int, question_id: int):
            return db.query(Question).filter(Question.id == question_id, Question.quiz_id == quiz_id).first()

    
    @staticmethod
    def get_random_questions(db: Session, quiz_id: int, num_questions: int):
        questions = (
    db.query(Question)
    .options(
        selectinload(Question.options)
    )  
    .filter(Question.quiz_id == quiz_id)  # Ensure questions belong to the right quiz
    .order_by(func.random())
    .limit(num_questions)
    .all()
)
        
    
        for question in questions:
            question.options = [opt for opt in question.options if opt.quiz_id == quiz_id]

        return questions