from fastapi import APIRouter, HTTPException
from datetime import date

# --- Configuração do Router ---
router = APIRouter(
    prefix="/rental",
    tags=["rental"],
    responses={404: {"description": "Rental not found"}},
)


# Os IDs de usuário, veículo e funcionário referenciam os dados
# que criamos nos outros arquivos de rotas.
mock_db_rentals = {
    1: {
        "id": 1,
        "rent_date": "2024-07-20",
        "return_date": "2024-07-25",
        "rent_value": 475, # 95.00 * 5 dias
        "id_user": 1, # Rick Sanchez
        "id_vehicle": 1, # Fiat Mobi
        "id_employee": 1 # Jerry Smith
    },
    2: {
        "id": 2,
        "rent_date": "2024-07-21",
        "return_date": "2024-07-28",
        "rent_value": 560, # 80.00 * 7 dias
        "id_user": 2, # Morty Smith
        "id_vehicle": 2, # Honda CB 500F
        "id_employee": 2 # Beth Smith
    },
}


@router.get("/")
async def get_all_rentals():
    """
    Retorna uma lista de todos os aluguéis cadastrados.
    """
    return list(mock_db_rentals.values())


@router.post("/")
async def create_rental(rental: dict):
    """
    Cria um novo registro de aluguel.
    O corpo da requisição deve ser um JSON com os dados do aluguel.
    Ex: {"return_date": "2024-08-10", "rent_value": 500, "id_user": 1, ...}
    """
    # Em um app real, você inseriria no banco de dados aqui.
    new_id = max(mock_db_rentals.keys() or [0]) + 1
    
    # Adiciona a data de aluguel padrão se não for fornecida
    if "rent_date" not in rental:
        rental["rent_date"] = date.today().isoformat()

    new_rental = {"id": new_id, **rental}
    mock_db_rentals[new_id] = new_rental
    return {"message": "Rental created successfully", "rental_id": new_id}


@router.get("/{rental_id}")
async def get_rental_by_id(rental_id: int):
    """
    Retorna os detalhes de um aluguel específico pelo seu ID.
    """
    rental = mock_db_rentals.get(rental_id)
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental


@router.put("/{rental_id}")
async def update_rental(rental_id: int, rental_update: dict):
    """
    Atualiza os dados de um aluguel existente.
    """
    if rental_id not in mock_db_rentals:
        raise HTTPException(status_code=404, detail="Rental not found")

    # Em uma aplicação real, você faria um UPDATE no banco de dados.
    mock_db_rentals[rental_id].update(rental_update)
    return {"message": "Rental updated successfully", "data": mock_db_rentals[rental_id]}


@router.delete("/{rental_id}")
async def delete_rental(rental_id: int):
    """
    Remove um registro de aluguel do sistema.
    """
    if rental_id not in mock_db_rentals:
        raise HTTPException(status_code=404, detail="Rental not found")

    # Em uma aplicação real, você faria um DELETE no banco de dados.
    del mock_db_rentals[rental_id]

    return {"message": "Rental deleted successfully", "rental_id": rental_id}