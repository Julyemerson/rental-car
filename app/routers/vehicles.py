from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Vehicle not found"}},
)

# --- Dados Mock (simulando um banco de dados com dicionários) ---
mock_db_vehicles = {
    1: {
        "id": 1,
        "brand": "Fiat",
        "model": "Mobi",
        "vehicle_type": "car",
        "year": 2022,
        "license_plate": "ABC1D23",
        "color": "White",
        "mileage": 15000,
        "available": True,
        "daily_charge": 95.00
    },
    2: {
        "id": 2,
        "brand": "Honda",
        "model": "CB 500F",
        "vehicle_type": "motorcycle",
        "year": 2023,
        "license_plate": "DEF4E56",
        "color": "Red",
        "mileage": 5000,
        "available": True,
        "daily_charge": 80.00
    },
    3: {
        "id": 3,
        "brand": "Chevrolet",
        "model": "Onix",
        "vehicle_type": "car",
        "year": 2020,
        "license_plate": "GHI7F89",
        "color": "Silver",
        "mileage": 89000,
        "available": False,
        "daily_charge": 105.70
    },
}


@router.get("/")
async def get_all_vehicles():
    """
    Retorna uma lista de todos os veículos cadastrados.
    """
    return list(mock_db_vehicles.values())


@router.post("/")
async def create_vehicle(vehicle: dict):
    """
    Cria um novo veículo.
    O corpo da requisição deve ser um JSON com os dados do veículo.
    """
    # Em um app real, você inseriria no banco de dados aqui.
    new_id = max(mock_db_vehicles.keys() or [0]) + 1
    new_vehicle = {"id": new_id, **vehicle}
    mock_db_vehicles[new_id] = new_vehicle
    return {"message": "Vehicle created successfully", "vehicle_id": new_id}


@router.get("/{vehicle_id}")
async def get_vehicle_by_id(vehicle_id: int):
    """
    Retorna os detalhes de um veículo específico pelo seu ID.
    """
    vehicle = mock_db_vehicles.get(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle_update: dict):
    """
    Atualiza os dados de um veículo existente.
    """
    if vehicle_id not in mock_db_vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Em uma aplicação real, você faria um UPDATE no banco de dados.
    mock_db_vehicles[vehicle_id].update(vehicle_update)
    return {"message": "Vehicle updated successfully", "data": mock_db_vehicles[vehicle_id]}


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    """
    Remove um veículo do sistema.
    """
    if vehicle_id not in mock_db_vehicles:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Em uma aplicação real, você faria um DELETE no banco de dados.
    del mock_db_vehicles[vehicle_id]

    return {"message": "Vehicle deleted successfully", "vehicle_id": vehicle_id}
