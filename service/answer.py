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
        user_id = JWTBearer.get_user_id_from_token(token)

        with uow:
            for answer in answers:
                question = uow.answers.get_question_by_id_and_category(answer.question_id, category_id)
                if not question:
                    results.append({
                        "question_id": answer.question_id,
                        "error": "Question not found in the specified category"
                    })
                else:
                    correct_option_id = None
                    selected_option_text = None  # Store the selected option's text

                    for option in question.options:
                        if option['option_id'] == answer.option_id:
                            selected_option_text = option['text']
                        if option['text'] == question.correct_option:
                            correct_option_id = option['option_id']

                    # Check if the provided option_id is valid
                    if answer.option_id is None or not any(option['option_id'] == answer.option_id for option in question.options):
                        results.append({
                            "question_id": answer.question_id,
                            "error": "Invalid option_id"
                        })
                        continue  # Skip this answer if option_id is invalid

                    # Compare option_id and set correctness
                    is_correct = correct_option_id == answer.option_id
                    if is_correct:
                        correct_count += 1

                    # Now save the correct values: option_id (integer), text (string)
                    uow.answers.save_answer(user_id, answer.question_id, answer.option_id, selected_option_text, is_correct)

                    results.append({
                        "question_id": answer.question_id,
                        "is_correct": is_correct
                    })

        return {
            "results": results,
            "correct_count": correct_count,
            "total_questions": total_questions
        }

