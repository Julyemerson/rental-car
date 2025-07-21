from fastapi import Request
from ..repositories.user_repository import UserRepository
from ..repositories.vehicle_repository import VehicleRepository

def get_user_repo(request: Request) -> UserRepository:
    return UserRepository(pool=request.app.state.db_pool)

def get_vehicle_repo(request: Request) -> VehicleRepository:
    return VehicleRepository(pool=request.app.state.db_pool)