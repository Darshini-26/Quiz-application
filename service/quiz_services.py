from sqlalchemy.orm import Session
from repository.quiz_repository import QuizRepository
from schemas.schemas import QuizCreate
from repository.question_repository import QuestionRepository
from schemas.schemas import QuizQuestionResponse

def create_quiz(db: Session, quiz: QuizCreate):
    return QuizRepository.create_quiz(db, quiz)

def get_all_quizzes(db: Session):
    return QuizRepository.get_all_quizzes(db)

def get_quiz_by_title(db: Session, title=str):
    return QuizRepository.get_quiz(db, title)


def get_random_questions(db: Session, quiz_id: int, num_questions: int):
    questions = QuestionRepository.get_random_questions(db, quiz_id, num_questions)

    # Transform data to exclude `quiz_id` and include `options`
    response = []
    for question in questions:
        options = [{"id": option.id, "text": option.text} for option in question.options]  # No is_correct field
        response.append({
            "id": question.id,
            "text": question.text,
            "options": options
        })

    return response