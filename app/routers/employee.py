from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.employee import CreateEmployee, UpdateEmployee, EmployeeInDB
from ..repositories.employee_repository import EmployeeRepository
from ..dependencies.dependencies import get_employee_repo

router = APIRouter(
    prefix="/employee", 
    tags=["employee"],
    responses={404: {"description": "Employee not found"}},
)


@router.get("/", response_model=List[EmployeeInDB])
async def get_all_employees(
    employee_repo: EmployeeRepository = Depends(get_employee_repo)
):
    return await employee_repo.get_all()


@router.post("/", response_model=EmployeeInDB, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: CreateEmployee, 
    employee_repo: EmployeeRepository = Depends(get_employee_repo)
):
    return await employee_repo.create(employee)


@router.get("/{employee_id}", response_model=EmployeeInDB)
async def get_employee_by_id(
    employee_id: int, 
    employee_repo: EmployeeRepository = Depends(get_employee_repo)
):
    """
    Retrieves a single employee by their ID.
    """
    db_employee = await employee_repo.get_by_id(employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.put("/{employee_id}", response_model=EmployeeInDB)
async def update_employee(
    employee_id: int, 
    employee_update: UpdateEmployee, 
    employee_repo: EmployeeRepository = Depends(get_employee_repo)
):
    updated_employee = await employee_repo.update(employee_id, employee_update)
    if updated_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int, 
    employee_repo: EmployeeRepository = Depends(get_employee_repo)
):
    success = await employee_repo.delete(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None
