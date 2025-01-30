from models.models import Answer,Question
from sqlalchemy.orm import Session
from schemas.schemas import AnswerCreate


class AnswerRepository:

    
    @staticmethod
    def create_answer(db: Session, answer: AnswerCreate):
        db_answer = Answer(
            text=answer.text,
            is_correct=answer.is_correct,
            question_id=answer.question_id,
            quiz_id=answer.quiz_id  # Include quiz_id
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        return db_answer

    @staticmethod
    def get_all_answers(db: Session):
        return db.query(Answer).all()

    @staticmethod
    def get_answer_by_id(db: Session, answer_id: int):
        # Fetch answer from the database
        answer = db.query(Answer).filter(Answer.id == answer_id).first()

        if not answer:
            return None  # If answer not found, return None
        
        # Fetch the related question to get quiz_id
        question = db.query(Question).filter(Question.id == answer.question_id).first()

        return {
            "id": answer.id,
            "text": answer.text,
            "is_correct": answer.is_correct,
            "question_id": answer.question_id,
            "quiz_id": question.quiz_id if question else None  # Fetch quiz_id from Question
        }