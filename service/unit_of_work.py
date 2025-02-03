from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from typing import Callable
from directory.category_types import CategoryTypes
from directory.question_bank import QuestionTypes
from directory.user_list import UserList
from directory.answer_submits import AnswerSubmits
from directory.rating_submits import RatingSubmits

class UnitOfWorkBase(ABC):
    categories: CategoryTypes
    questions: QuestionTypes
    users:UserList
    answers:AnswerSubmits
    ratings:RatingSubmits

    def __enter__(self):
        return self  # Ensures that 'self' (UnitOfWork) is returned and available to the context manager

    def __exit__(self, exc_type, exc_value, traceback):
        # In case of an exception or successful exit, rollback to maintain consistent state
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        """Commit the current transaction."""
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollback the current transaction."""
        raise NotImplementedError()


class UnitOfWork(UnitOfWorkBase):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._session_factory = session_factory
        self._session = None
        self.categories = None
        self.questions = None
        self.answers=None
        self.ratings=None

    def __enter__(self):
        self._session =self._session_factory()  # Start a new session
        self.categories = CategoryTypes(self._session)  # Initialize the categories repository
        self.questions = QuestionTypes(self._session)  # Initialize the questions repository
        self.users=UserList(self._session)
        self.answers=AnswerSubmits(self._session)
        self.ratings=RatingSubmits(self._session)
        return super().__enter__()  # Return self to make the repositories accessible

    def commit(self):
        """Commit the current transaction."""
        self._session.commit()  # Commit the session

    def rollback(self):
        """Rollback the current transaction."""
        self._session.rollback()  # Rollback the session

    def __del__(self):
        """Ensure the session is closed after usage. (Although not recommended for resource management)"""
        self._session.close()  # Make sure we clean up the session
