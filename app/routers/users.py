from fastapi import APIRouter, HTTPException

# --- Configuração do Router ---
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)

# --- Dados Mock (simulando um banco de dados com base no seu SQL) ---
mock_db_users = {
    1: {
        "id": 1,
        "name": "Rick",
        "last_name": "Sanchez",
        "cpf": "12345678901",
        "email": "rick.sanchez@email.com",
        "birth_at": "1955-03-04"
    },
    2: {
        "id": 2,
        "name": "Morty",
        "last_name": "Smith",
        "cpf": "09876543211",
        "email": "morty.smith@email.com",
        "birth_at": "2008-01-10"
    },
}


@router.get("/")
async def get_all_users():
    """
    Retorna uma lista de todos os usuários cadastrados.
    """
    return list(mock_db_users.values())


@router.post("/")
async def create_user(user: dict):
    """
    Cria um novo usuário.
    O corpo da requisição deve ser um JSON com os dados do usuário.
    Ex: {"name": "Summer", "last_name": "Smith", "email": "summer@email.com", ...}
    """
    # Em um app real, você inseriria no banco de dados aqui.
    new_id = max(mock_db_users.keys() or [0]) + 1
    new_user = {"id": new_id, **user}
    mock_db_users[new_id] = new_user
    return {"message": "User created successfully", "user_id": new_id}


@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    """
    Retorna os detalhes de um usuário específico pelo seu ID.
    """
    user = mock_db_users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
async def update_user(user_id: int, user_update: dict):
    """
    Atualiza os dados de um usuário existente.
    """
    if user_id not in mock_db_users:
        raise HTTPException(status_code=404, detail="User not found")

    # Em uma aplicação real, você faria um UPDATE no banco de dados.
    mock_db_users[user_id].update(user_update)
    return {"message": "User updated successfully", "data": mock_db_users[user_id]}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """
    Remove um usuário do sistema.
    """
    if user_id not in mock_db_users:
        raise HTTPException(status_code=404, detail="User not found")

    # Em uma aplicação real, você faria um DELETE no banco de dados.
    del mock_db_users[user_id]

    return {"message": "User deleted successfully", "user_id": user_id}