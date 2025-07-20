from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/employee",
    tags=["employee"],
    responses={404: {"description": "Employee not found"}},
)

mock_db_employees = {
    1: {
        "id": 1,
        "name": "Jerry",
        "last_name": "Smith",
        "cpf": "11122233344",
        "email": "jerry.smith@email.com",
        "role": "Sales Associate"
    },
    2: {
        "id": 2,
        "name": "Beth",
        "last_name": "Smith",
        "cpf": "55566677788",
        "email": "beth.smith@email.com",
        "role": "Manager"
    },
}


@router.get("/")
async def get_all_employees():
    """
    Retorna uma lista de todos os funcionários cadastrados.
    """
    return list(mock_db_employees.values())


@router.post("/")
async def create_employee(employee: dict):
    """
    Cria um novo funcionário.
    O corpo da requisição deve ser um JSON com os dados do funcionário.
    Ex: {"name": "Bird", "last_name": "Person", "email": "bird.person@email.com", ...}
    """
    new_id = max(mock_db_employees.keys() or [0]) + 1
    new_employee = {"id": new_id, **employee}
    mock_db_employees[new_id] = new_employee
    return {"message": "Employee created successfully", "employee_id": new_id}


@router.get("/{employee_id}")
async def get_employee_by_id(employee_id: int):
    """
    Retorna os detalhes de um funcionário específico pelo seu ID.
    """
    employee = mock_db_employees.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}")
async def update_employee(employee_id: int, employee_update: dict):
    """
    Atualiza os dados de um funcionário existente.
    """
    if employee_id not in mock_db_employees:
        raise HTTPException(status_code=404, detail="Employee not found")


    mock_db_employees[employee_id].update(employee_update)
    return {"message": "Employee updated successfully", "data": mock_db_employees[employee_id]}


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """
    Remove um funcionário do sistema.
    """
    if employee_id not in mock_db_employees:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Em uma aplicação real, você faria um DELETE no banco de dados.
    del mock_db_employees[employee_id]

    return {"message": "Employee deleted successfully", "employee_id": employee_id}
