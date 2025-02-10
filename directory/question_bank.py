# repositories/question_repository.py

from sqlalchemy.orm import Session
from models.models import Question
from schemas.schemas import QuestionCreate
import random
from sqlalchemy.sql import func

class QuestionTypes:
    def __init__(self, session: Session):
        self.session = session

    def create_question(self, question: QuestionCreate, category_id: int):
        # Convert options list of Pydantic models into JSON serializable list of dictionaries
        options_as_dict = [option.dict() for option in question.options]

        question_data = Question(
            **question.dict(exclude={"options"}),  # Exclude 'options' from dict
            options=options_as_dict,  # Store as JSONB
            category_id=category_id
        )
        
        self.session.add(question_data)
        self.session.commit()
        self.session.refresh(question_data)
        return question_data

        

    @staticmethod
    def get_all_question(session: Session):
        return session.query(Question).all()

    @staticmethod
    def get_question_by_id(session: Session, question_id: int):
        return session.query(Question).filter(Question.question_id == question_id).first()

    @staticmethod
    def get_questions_by_category(session: Session, category_id: int):
        return session.query(Question).filter(Question.category_id == category_id).all()

    @staticmethod
    def fetch_random_questions(session: Session, category_id: int, num_questions: int):
        return (
            session.query(Question)
            .filter(Question.category_id == category_id)
            .order_by(func.random())  # Fetch random questions
            .limit(num_questions)
            .all()
        )
    
    @staticmethod
    def get_question_by_id(session:Session, category_id: int, question_id: int):
        return session.query(Question).filter(
            Question.category_id == category_id,
            Question.question_id == question_id
        ).first()
    
    @staticmethod
    def delete_question( session: Session, question: Question):
        session.delete(question)
