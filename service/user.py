from sqlalchemy.orm import Session
from directory.user_list import UserList
from schemas.schemas import UserCreate
from .unit_of_work import UnitOfWork

class UserService:
    @staticmethod
    def create_user(uow: UnitOfWork, user: UserCreate):
        with uow:
            return uow.users.create_user(user)

    @staticmethod
    def get_all_users(uow: UnitOfWork):
        return UserRepository.get_all_users(db)

    @staticmethod
    def get_user_by_id(uow: UnitOfWork, user_id: str):
        return UserRepository.get_user_by_id(db, user_id)