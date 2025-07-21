from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from ..schemas.rental import RentalCreate, RentalUpdate, RentalInDB
from ..repositories.rental_repository import RentalRepository
from ..dependencies.dependencies import get_rental_repo

router = APIRouter(
    prefix="/rental", #
    tags=["rental"],
    responses={404: {"description": "Rental not found"}},
)


@router.get("/", response_model=List[RentalInDB])
async def get_all_rentals(
    rental_repo: RentalRepository = Depends(get_rental_repo)
):
    return await rental_repo.get_all()


@router.post("/", response_model=RentalInDB, status_code=status.HTTP_201_CREATED)
async def create_rental(
    rental: RentalCreate, 
    rental_repo: RentalRepository = Depends(get_rental_repo)
):
    return await rental_repo.create(rental)


@router.get("/{rental_id}", response_model=RentalInDB)
async def get_rental_by_id(
    rental_id: int, 
    rental_repo: RentalRepository = Depends(get_rental_repo)
):
    db_rental = await rental_repo.get_by_id(rental_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return db_rental


@router.put("/{rental_id}", response_model=RentalInDB)
async def update_rental(
    rental_id: int, 
    rental_update: RentalUpdate, 
    rental_repo: RentalRepository = Depends(get_rental_repo)
):
    updated_rental = await rental_repo.update(rental_id, rental_update)
    if updated_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated_rental


@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rental(
    rental_id: int, 
    rental_repo: RentalRepository = Depends(get_rental_repo)
):
    success = await rental_repo.delete(rental_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rental not found")
    return None