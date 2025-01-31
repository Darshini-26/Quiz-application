from sqlalchemy.orm import Session
from repository.quiz_repository import QuizRepository
from repository.question_repository import QuestionRepository
from models.models import Question
from schemas.schemas import QuestionCreate,QuizQuestionResponse, OptionResponse 

class QuestionService:
    @staticmethod
    def create_question(db: Session, quiz_id: int, text: str):
        return QuestionRepository.create_question(db, quiz_id, text)


    def get_all_questions(db: Session):
        return QuestionRepository.get_all_questions(db)

    def get_questions_by_quizid(db: Session, quiz_id: int):
        return QuestionRepository.get_questions_by_id(db, quiz_id)

    @staticmethod
    def get_question_by_quiz_and_id(db: Session, quiz_id: int, question_id: int):
        return QuestionRepository.get_question_by_quiz_and_id(db, quiz_id, question_id)

    @staticmethod
    def fetch_random_questions_for_quiz(db, quiz_id:int, num_questions:int):
        # Call the repository to get the questions with options
        questions_with_options = QuestionRepository.get_random_questions(db, quiz_id, num_questions)
        
        # Convert the questions and options into the response format
        quiz_question_responses = []
        for question in questions_with_options:
            options = [OptionResponse(id=option.id, text=option.text) for option in question.options]
            quiz_question_responses.append(QuizQuestionResponse(id=question.id, text=question.text, options=options))

        return quiz_question_responses