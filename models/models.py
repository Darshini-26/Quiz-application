from datetime import datetime
import uuid
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Text,Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base,engine
from sqlalchemy.dialects.postgresql import JSONB


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)


    answers = relationship('Answer', back_populates='user')
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")
    scores=relationship("Score",back_populates="user",cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)

    questions = relationship("Question", back_populates="category")
    ratings = relationship("Rating", back_populates="category", cascade="all, delete-orphan")
    scores=relationship("Score",back_populates="category",cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    options = Column(JSONB, nullable=False)  # Storing options as JSON
    correct_option = Column(String, nullable=False)  # Correct answer as text

    category = relationship("Category", back_populates="questions")
    answers = relationship("Answer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.question_id", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    option_id = Column(Integer) 
    user_id = Column(UUID, ForeignKey('users.user_id'))  # Foreign key to User
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")
    user = relationship('User', back_populates='answers')

class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # Rating out of 5
    review = Column(String, nullable=True)

    user = relationship("User", back_populates="ratings")
    category = relationship("Category", back_populates="ratings")

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), nullable=False)
    score_percentage = Column(Float, nullable=False)  # Storing score as a percentage

    user = relationship("User", back_populates="scores")
    category = relationship("Category", back_populates="scores")