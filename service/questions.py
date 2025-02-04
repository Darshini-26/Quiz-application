from fastapi import HTTPException
from models.models import Question
from schemas.schemas import QuestionCreate
from .unit_of_work import UnitOfWork

class QuestionService:
    @staticmethod  # Use staticmethod decorator
    def create_question_service(uow: UnitOfWork, question: QuestionCreate, category_id: int):
        with uow:
            # Create the question by passing the Pydantic model to the repository method for creation
            return uow.questions.create_question(question, category_id)

   
    @staticmethod
    def get_all_questions_service(uow: UnitOfWork):
        with uow:
            return uow.questions.get_all_question(uow._session)

    @staticmethod  # Use staticmethod decorator
    def get_question_by_id_service(uow: UnitOfWork, quiz_id: int):
        with uow:
            question = uow.questions.get_question_by_id(uow._session, quiz_id)
            if not question:
                raise HTTPException(status_code=404, detail="Question not found")  # Handle 404 error
            return question

    @staticmethod  # Use staticmethod decorator
    def get_questions_by_category_service(uow: UnitOfWork, category_id: int):
        with uow:
            return uow.questions.get_questions_by_category(uow._session, category_id)


    @staticmethod
    def fetch_random_questions_for_quiz(uow: UnitOfWork, category_id: int, num_questions: int):
        with uow:
            # Fetch random questions
            questions = uow.questions.fetch_random_questions(uow._session, category_id, num_questions)

            # Format the response
            result = [
                {
                    "question_id": question.question_id,
                    "question_text": question.text,
                    "category_id": question.category_id,
                    "options": question.options  # Fetch options directly from the column
                }
                for question in questions
            ]

            return result
