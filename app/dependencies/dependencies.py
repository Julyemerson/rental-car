from fastapi import Request
from ..repositories.user_repository import UserRepository

def get_user_repo(request: Request) -> UserRepository:
    """
    Dependency function that creates and returns a UserRepository instance.
    It gets the database pool from the application state.
    """
    return UserRepository(pool=request.app.state.db_pool)