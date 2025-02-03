from fastapi import HTTPException
from service.unit_of_work import UnitOfWork
from models.models import Question
from .unit_of_work import UnitOfWork
from schemas.schemas import AnswerSubmitRequest

import uuid
from auth.auth import JWTBearer

class AnswerService:
    @staticmethod
    def validate_answers(uow: UnitOfWork, category_id: int, answers: list, token: str):
        results = []
        correct_count = 0  # Variable to count correct answers
        total_questions = len(answers)

        # Decode user_id from JWT token
        user_id = JWTBearer.get_user_id_from_token(token)  # Ensure this method extracts the user_id correctly

        with uow:
            for answer in answers:
                question = uow.answers.get_question_by_id_and_category(answer.question_id, category_id)
                if not question:
                    results.append({
                        "question_id": answer.question_id,
                        "error": "Question not found in the specified category"
                    })
                else:
                    is_correct = question.correct_option.lower() == answer.text.lower()
                    if is_correct:
                        correct_count += 1
                    # Now, pass the user_id (which should be a UUID) when saving the answer
                    uow.answers.save_answer(user_id, answer.question_id, answer.text, is_correct)

                    results.append({
                        "question_id": answer.question_id,
                        "is_correct": is_correct
                    })

        return {
            "results": results,
            "correct_count": correct_count,
            "total_questions": total_questions
        }
