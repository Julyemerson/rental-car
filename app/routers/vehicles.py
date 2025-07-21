from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleInDB
from ..dependencies.dependencies import get_vehicle_repo 
from ..repositories.vehicle_repository import VehicleRepository

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
    responses={404: {"description": "Vehicle not found"}},
)


@router.get("/", response_model=List[VehicleInDB])
async def get_all_vehicles(vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)):
    """
    Retorna uma lista de todos os veículos cadastrados.
    """
    return await vehicle_repo.get_all()


@router.post("/", response_model=VehicleInDB, status_code=status.HTTP_201_CREATED)
async def create_vehicle(vehicle: VehicleCreate, vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)):
   return await vehicle_repo.create(vehicle)


@router.get("/{vehicle_id}", response_model=VehicleInDB, status_code=status.HTTP_200_OK)
async def get_vehicle_by_id(vehicle_id: int, vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)):
    """
    Retorna os detalhes de um veículo específico pelo seu ID.
    """
    vehicle = await vehicle_repo.get_by_id(vehicle_id) 
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleInDB, status_code=status.HTTP_200_OK)
async def update_vehicle(vehicle_id: int, vehicle_update: VehicleUpdate, vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)):
    """
    Atualiza os dados de um veículo existente.
    """
    updated_vehicle = await vehicle_repo.update(vehicle_id, vehicle_update)
    if not update_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(vehicle_id: int, vehicle_repo: VehicleRepository = Depends(get_vehicle_repo)):
    """
    Remove um veículo do sistema.
    """
    success = await vehicle_repo.delete(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None