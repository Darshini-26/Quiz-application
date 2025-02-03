from fastapi import APIRouter, Depends, HTTPException
from service.unit_of_work import UnitOfWork
from service.answer import AnswerService
from auth.auth import JWTBearer  # Ensure authentication
from config.database import get_db, SessionLocal
from schemas.schemas import AnswerCreate,AnswerSubmitRequest
from auth.auth import JWTBearer

router = APIRouter(prefix="/answers", tags=["Answers"])

def get_uow() -> UnitOfWork:
    return UnitOfWork(SessionLocal)


@router.post("/{category_id}/submit", dependencies=[Depends(JWTBearer())])
def submit_answers(category_id: int, answer_request: AnswerSubmitRequest, uow: UnitOfWork = Depends(get_uow), user_id: int = Depends(JWTBearer())):
    # Now we don't need to pass token, the user_id is extracted from the token automatically
    response = AnswerService.validate_answers(uow, category_id, answer_request.answers, user_id)
    return response