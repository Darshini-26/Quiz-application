from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
import uuid


# Login Schema
class Login(BaseModel):
    name: str
    password: str


#  User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str 
    is_admin:bool=False # Only required when creating a user

class UserResponse(UserBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True


# Quiz Schemas
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None

class QuizCreate(QuizBase):
    pass

class QuizResponse(QuizBase):
    id: int

    class Config:
        from_attributes = True


# Option (Answer Choices) Schema
class OptionResponse(BaseModel):
    id: int
    text: str  # No `is_correct` field (only text)


# Question Schemas
class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    quiz_id: int

    class Config:
        from_attributes = True


# Question with Options Response (for API)
class QuizQuestionResponse(BaseModel):
    id: int
    text: str
    options: List[OptionResponse]  # Returns list of options instead of `quiz_id`

    class Config:
        from_attributes = True


#  Answer Schema
class AnswerBase(BaseModel):
    text: str
    is_correct: bool

class AnswerCreate(BaseModel):
    question_id: int
    quiz_id:int
    options: List[AnswerBase]  #  Users select from a list of options

class Answers(BaseModel):
    id: int  # ID of the question being answered
    option_id: int

class AnswerSubmitRequest(BaseModel):
    question_id: int
    option_id: int
    
class QuizSubmissionRequest(BaseModel):
    answers: List[AnswerSubmitRequest]


class AnswerResponse(AnswerBase):
    id: int
    question_id: int  #  Removed `quiz_id` (not needed)

    class Config:
        from_attributes = True



class ReviewCreate(BaseModel):
    rating: int
    feedback: str | None = None  # Optional feedback

    class Config:
        from_attributes = True