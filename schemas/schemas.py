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
    is_admin: bool = False

class UserResponse(UserBase):
    # user_id: uuid.UUID

    class Config:
        from_attributes = True


# Category Schemas
class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    text: str
    options: List[str]  # List of 4 answer choices
    correct_option: str  # The correct answer text


class QuestionCreate(QuestionBase):
    # category_id: int
    pass

class BulkQuestionCreate(BaseModel):
    questions: List[QuestionCreate]

class QuestionResponse(QuestionBase):
    question_id: int
    category_id: int

    class Config:
        from_attributes = True


# Answer Schemas
class AnswerBase(BaseModel):
    text: str

class AnswerCreate(AnswerBase):
    question_id: int

class AnswerSubmitRequest(BaseModel):
    answers: List[AnswerCreate]

class AnswerResponse(AnswerBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True


# Rating Schema
class ReviewCreate(BaseModel):
    rating: int
    feedback: str | None = None  # Optional feedback

    class Config:
        from_attributes = True

    class Config:
        from_attributes = True
