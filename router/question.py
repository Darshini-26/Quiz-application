from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from service.questions import QuestionService  # Ensure this import path is correct
from config.database import get_db, SessionLocal
from schemas.schemas import QuestionCreate, QuestionResponse,BulkQuestionCreate # Adjust your schemas accordingly
from typing import List
from service.unit_of_work import UnitOfWork
from auth.auth import JWTBearer

router = APIRouter(prefix="/questions", tags=["Question"])

def get_uow() -> UnitOfWork:
    # Returning UnitOfWork, assuming it provides access to the necessary repositories
    return UnitOfWork(SessionLocal)

@router.post("/{category_id}/", response_model=QuestionResponse,dependencies=[Depends(JWTBearer(admin_required=True))])
def create_question(question: QuestionCreate, category_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        # Create question using the QuestionService
        return QuestionService.create_question_service(uow, question, category_id)
    except Exception as e:
        # Raise an HTTP exception if creation fails
        raise HTTPException(status_code=400, detail=str(e))
    
# @router.post("/{category_id}/bulk", response_model=List[QuestionResponse])
# def create_bulk_questions(category_id: int, bulk_questions: BulkQuestionCreate, uow: UnitOfWork = Depends(get_uow)):
#     try:
#         # Loop through all the questions and create them one by one
#         created_questions = []
#         for question in bulk_questions.questions:
#             created_question = QuestionService.create_question_service(uow, question, category_id)
#             created_questions.append(created_question)
#         return created_questions
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[QuestionResponse],dependencies= [Depends(JWTBearer(admin_required=True))])  # Adjust response model if necessary
def read_questions(uow: UnitOfWork = Depends(get_uow)):
    try:
        # Get all questions using QuestionService
        return QuestionService.get_all_questions_service(uow)
    except Exception as e:
        # Handle failure to retrieve questions
        raise HTTPException(status_code=500, detail="Failed to fetch questions")

# @router.get("/{quiz_id}", response_model=QuestionResponse,dependencies= [Depends(JWTBearer())])
# def read_question(quiz_id: int, uow: UnitOfWork = Depends(get_uow)):
#     try:
#         # Retrieve question by its ID
#         return QuestionService.get_question_by_id_service(uow, quiz_id)
#     except Exception as e:
#         # Handle failure to find the question
#         raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/quiz/{category_id}/random-questions",dependencies= [Depends(JWTBearer())])
def get_quiz_questions(category_id: int, num_questions: int = 5,uow: UnitOfWork = Depends(get_uow)):
    # Fetch random questions with options from the service layer
    questions =  QuestionService.fetch_random_questions_for_quiz(uow, category_id, num_questions)
    return questions

@router.put("/{category_id}/", response_model=QuestionResponse, dependencies=[Depends(JWTBearer(admin_required=True))])
def update_question(
    category_id: int,
    question_id: int,
    question_data: QuestionCreate,
    uow: UnitOfWork = Depends(get_uow)
):
    try:
        return QuestionService.update_question_service(uow, category_id, question_id, question_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{category_id}/", dependencies=[Depends(JWTBearer(admin_required=True))])
def delete_question(category_id: int, question_id: int, uow: UnitOfWork = Depends(get_uow)):
    try:
        return QuestionService.delete_question_service(uow, category_id, question_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
