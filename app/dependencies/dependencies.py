from fastapi import Request
from ..repositories.user_repository import UserRepository
from ..repositories.vehicle_repository import VehicleRepository
from ..repositories.employee_repository import EmployeeRepository
from ..repositories.rental_repository import RentalRepository

def get_user_repo(request: Request) -> UserRepository:
    return UserRepository(pool=request.app.state.db_pool)

def get_vehicle_repo(request: Request) -> VehicleRepository:
    return VehicleRepository(pool=request.app.state.db_pool)

def get_employee_repo(request: Request) -> EmployeeRepository:
    return EmployeeRepository(pool=request.app.state.db_pool)

def get_rental_repo(request: Request) -> RentalRepository:
    return RentalRepository(pool=request.app.state.db_pool)