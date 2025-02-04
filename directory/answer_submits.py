from sqlalchemy.orm import Session
from models.models import Question,Answer
import uuid
from sqlalchemy import insert


class AnswerSubmits:
    def __init__(self, session: Session):
        self.session = session

    def get_question_by_id_and_category(self, question_id: int, category_id: int):
        return self.session.query(Question).filter(Question.question_id == question_id, Question.category_id == category_id).first()

    
    def save_answer(self, user_id, question_id, option_id, selected_option_text, is_correct):
        # Ensure you're passing the correct values to the Answer model
        new_answer = Answer(
            question_id=question_id,
            option_id=option_id,  # Option ID should be an integer
            user_id=user_id,
            text=selected_option_text,  # Option text should be a string
            is_correct=is_correct
        )
        self.session.add(new_answer)
        self.session.commit()



