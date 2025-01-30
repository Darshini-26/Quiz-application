from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import AnswerCreate, AnswerResponse, Answers,AnswerSubmitRequest,QuizSubmissionRequest
from service.answer_services import AnswerService
from service.question_services import QuestionService
from config.database import get_db
from models.models import Answer,Question,Option,Question,Review
from auth.auth import JWTBearer
from typing import Optional,List


answer_router = APIRouter(prefix="/answers", tags=["Answers"])

@answer_router.post("/quiz/{quiz_id}/submit-answers")
def submit_answers(
    quiz_id: int, 
    submission: QuizSubmissionRequest, 
    db: Session = Depends(get_db)
):
    """
    Submit answers for all randomized questions in a quiz and calculate score.
    """
    response = []
    total_questions = len(submission.answers)
    correct_answers = 0  # Counter for correct answers

    for answer in submission.answers:
        # Validate if the selected option exists for the given question and quiz
        option = db.query(Option).filter(
            Option.id == answer.option_id,
            Option.question_id == answer.question_id,
            Option.quiz_id == quiz_id  # Ensure it belongs to the correct quiz
        ).first()

        if not option:
            raise HTTPException(status_code=400, detail=f"Invalid option for question ID {answer.question_id}")

        # Check if the selected option is correct
        is_correct = option.is_correct  
        if is_correct:
            correct_answers += 1  # Increment score if correct

        # Store the user's answer
        new_answer = Answer(
            quiz_id=quiz_id,
            question_id=answer.question_id,
            is_correct=is_correct  # Store correctness, but no need to store option_id
        )
        db.add(new_answer)

        response.append({
            "question_id": answer.question_id,
            "selected_option_id": answer.option_id,
            "is_correct": is_correct
        })

    db.commit()  # Commit all answers in one go

    # Calculate and format the final score
    score = f"{correct_answers}/{total_questions}"

    return {
        "message": "Answers submitted successfully.",
        "score": score,  # Display the marks
        "results": response
    }


@answer_router.post("/", status_code=201)
def create_answers(answer_data: AnswerCreate, db: Session = Depends(get_db)):
    """
    Accept multiple answer options and store both correct and incorrect answers.
    """
    question = db.query(Question).filter(Question.id == answer_data.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Ensure at least one correct answer exists
    if not any(option.is_correct for option in answer_data.options):
        raise HTTPException(status_code=400, detail="At least one correct answer is required")

    # Save all answer options (both correct and incorrect)
    for option in answer_data.options:
        new_answer = Answer(
            text=option.text,
            is_correct=option.is_correct,  # Store both correct & incorrect
            question_id=answer_data.question_id,
            quiz_id=answer_data.quiz_id
        )
        db.add(new_answer)

    db.commit()
    return {"message": "All answer options added successfully"}




@answer_router.get("/{question_id}/", response_model=list[AnswerResponse],dependencies= [Depends(JWTBearer())])
def get_answers_by_question_id(question_id: int, db: Session = Depends(get_db)):
    """
    Get all answers for a specific question.
    """
    try:
        answers = AnswerService.get_answers_by_question_id(db, question_id)
        return answers
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@answer_router.get("/", response_model=list[AnswerResponse],dependencies= [Depends(JWTBearer())])
def get_all_answers(db: Session = Depends(get_db)):
    """
    Get all answers in the database.
    """
    try:
        answers = AnswerService.get_all_answers(db)
        return answers
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@answer_router.get("/{question_id}/", response_model=List[AnswerResponse])
def get_correct_answers(question_id: int, db: Session = Depends(get_db)):
    """
    Fetch only the correct answers for a given question.
    """
    correct_answers = db.query(Answer).filter(
        Answer.question_id == question_id, Answer.is_correct == True
    ).all()

    if not correct_answers:
        raise HTTPException(status_code=404, detail="No correct answers found for this question")

    return correct_answers
