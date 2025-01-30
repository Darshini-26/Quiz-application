from datetime import datetime
import uuid
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,event, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import PrimaryKeyConstraint,ForeignKeyConstraint, UniqueConstraint

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship with UserQuiz
    quizzes = relationship("UserQuiz", back_populates="user")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    is_correct = Column(Boolean, default=False)

    # Fix Foreign Key Reference
    question_id = Column(Integer, ForeignKey("questions.id", ondelete='CASCADE'), nullable=False)  
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete='CASCADE'), nullable=False)
   
    
    # Relationships
    question = relationship("Question", back_populates="answers")
    quiz = relationship("Quiz", back_populates="answers")
  

class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)

    # Relationships
    questions = relationship("Question", back_populates="quiz")
    user_quizzes = relationship("UserQuiz", back_populates="quiz")
    answers = relationship("Answer", back_populates="quiz") 
    reviews = relationship("Review", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)  # ✅ Unique Primary Key
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete='CASCADE'), nullable=False)
    text = Column(String, nullable=True)

    # Ensure (quiz_id, id) is unique if needed
    __table_args__ = (UniqueConstraint('quiz_id', 'id', name='uq_quiz_question'),)

    # Relationships
    answers = relationship("Answer", back_populates="question", cascade="all, delete")
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete")


class Option(Base):
    __tablename__ = 'options'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)  # ✅ Indicates if the option is correct
    
    # Foreign Key References
    question_id = Column(Integer, ForeignKey("questions.id", ondelete='CASCADE'), nullable=False)  
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete='CASCADE'), nullable=False)

    # Relationships
    question = relationship("Question", back_populates="options")




class UserQuiz(Base):
    __tablename__ = 'user_quizzes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    score = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="quizzes")
    quiz = relationship("Quiz", back_populates="user_quizzes")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False) 
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)  # Rating out of 5
    feedback = Column(String, nullable=True)  # Optional feedback
    

    quiz = relationship("Quiz", back_populates="reviews")
    user = relationship("User", back_populates="reviews")