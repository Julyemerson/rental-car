import aiomysql
from typing import List, Optional
from .base_repository import BaseRepository
from ..schemas.rental import RentalCreate, RentalUpdate, RentalInDB

class RentalRepository(BaseRepository):
    async def get_all(self) -> List[RentalInDB]:
        """Retrieves all rental records from the database."""
        query = "SELECT * FROM rental;"
        records = await self._execute_query(query, fetch='all')
        return [RentalInDB(**record) for record in (records or [])]

    async def get_by_id(self, rental_id: int) -> Optional[RentalInDB]:
        """Retrieves a single rental by its ID."""
        query = "SELECT * FROM rental WHERE id = %s;"
        record = await self._execute_query(query, params=(rental_id,), fetch='one')
        return RentalInDB(**record) if record else None

    async def create(self, rental: RentalCreate) -> RentalInDB:
        query = """
            INSERT INTO rental (rent_date, return_date, rent_value, id_user, id_vehicle, id_employee)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        params = (
            rental.rent_date, rental.return_date, rental.rent_value,
            rental.id_user, rental.id_vehicle, rental.id_employee
        )
        new_id = await self._execute_query(query, params=params)
        
        if new_id is None:
            raise ValueError("Failed to create rental: No ID returned from database.")
            
        # Constructs the response object without a second DB query.
        return RentalInDB(id=new_id, **rental.model_dump())

    async def update(self, rental_id: int, rental_update: RentalUpdate) -> Optional[RentalInDB]:
        update_data = rental_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_by_id(rental_id)

        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE rental SET {set_clause} WHERE id = %s;"
        
        params = tuple(update_data.values()) + (rental_id,)
        
        await self._execute_query(query, params=params)
        
        return await self.get_by_id(rental_id)

    async def delete(self, rental_id: int) -> bool:
        query = "DELETE FROM rental WHERE id = %s;"
        await self._execute_query(query, params=(rental_id,))
        
        return await self.get_by_id(rental_id) is None