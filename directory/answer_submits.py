from sqlalchemy.orm import Session
from models.models import Question,Answer,Score
import uuid
from sqlalchemy import insert
from sqlalchemy.sql import func


class AnswerSubmits:
    def __init__(self, session: Session):
        self.session = session

    def get_question_by_id_and_category(self, question_id: int, category_id: int):
        return self.session.query(Question).filter(Question.question_id == question_id, Question.category_id == category_id).first()

    def save_answer(self, user_id, question_id, option_id, selected_option_text, is_correct, category_id, total_questions,correct_count):
        # Save the user's answer
        new_answer = Answer(
            question_id=question_id,
            option_id=option_id,
            user_id=user_id,
            text=selected_option_text,
            is_correct=is_correct
        )
        self.session.add(new_answer)
        self.session.commit()

        # Calculate the updated score for the user in the given category
        correct_answers_count = (
            self.session.query(func.count(Answer.id))
            .filter(Answer.user_id == user_id, Answer.is_correct == True)
            .join(Question, Answer.question_id == Question.question_id)
            .filter(Question.category_id == category_id)
            .scalar()
        )

        # Debug: print the count of correct answers and total questions
        print(f"Correct Answers: {correct_count}")
        print(f"Total Questions: {total_questions}")

        # Calculate score percentage
        score_percentage = (correct_count / float(total_questions)) * 100  # Ensure float division

        # Debug: print the score percentage before saving it
        print(f"Calculated Score Percentage: {score_percentage}")

        # Check if a score entry exists for the user in this category
        score_entry = (
            self.session.query(Score)
            .filter(Score.user_id == user_id, Score.category_id == category_id)
            .first()
        )

        if score_entry:
            # If score exists, update it
            print(f"Score entry already exists for user {user_id} and category {category_id}. Updating the score.")
            score_entry.score_percentage = score_percentage  # Update the existing score with the new percentage
            self.session.commit()
        else:
            # Create a new score entry if it doesn't exist
            new_score = Score(
                user_id=user_id,
                category_id=category_id,
                score_percentage=score_percentage  # Store as percentage
            )
            self.session.add(new_score)
            self.session.commit()
            print(f"New score entry created for user {user_id} with percentage: {score_percentage}")

        return score_percentage
        

    

