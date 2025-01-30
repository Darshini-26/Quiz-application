from sqlalchemy.orm import Session
from repository.answer_repository import AnswerRepository
from schemas.schemas import AnswerCreate


class AnswerService:
    @staticmethod
    def create_answer(db: Session, question_id: int, answer: AnswerCreate):
        return AnswerRepository.create_answer(db, question_id, answer)

    @staticmethod
    def get_all_answers(db: Session):
        return AnswerRepository.get_all_answers(db)

    @staticmethod
    def get_answers_by_question_id(db: Session, question_id: int):
        return AnswerRepository.get_answers_by_question_id(db, question_id)
