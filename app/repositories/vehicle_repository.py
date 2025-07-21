from typing import List, Optional
from .base_repository import BaseRepository
from ..schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleInDB

class VehicleRepository(BaseRepository):
    async def get_all(self) -> List[VehicleInDB]:
        query = "SELECT * FROM vehicle;"
        records = await self._execute_query(query, fetch='all')
        return [VehicleInDB(**record) for record in records] if records else []

    async def get_by_id(self, vehicle_id: int) -> Optional[VehicleInDB]:
        """
        Busca um único veículo pelo seu ID.
        """
        query = "SELECT * FROM vehicle WHERE id = %s;"
        record = await self._execute_query(query, params=(vehicle_id,), fetch='one')
        return VehicleInDB(**record) if record else None

    async def create(self, vehicle: VehicleCreate) -> VehicleInDB:
        """
        Insere um novo veículo no banco de dados.
        """
        query = """
            INSERT INTO vehicle (brand, model, vehicle_type, year, license_plate, color, mileage, available, daily_charge)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            vehicle.brand, vehicle.model, vehicle.vehicle_type, vehicle.year, 
            vehicle.license_plate, vehicle.color, vehicle.mileage, 
            vehicle.available, vehicle.daily_charge
        )
        new_id = await self._execute_query(query, params=params)
        if new_id is None:
            raise ValueError("Failed to create vehicle: no ID returned from database.")
        vehicle_in_db = await self.get_by_id(new_id)
        if vehicle_in_db is None:
            raise ValueError("Failed to retrieve newly created vehicle from database.")
        return vehicle_in_db

    async def update(self, vehicle_id: int, vehicle_update: VehicleUpdate) -> Optional[VehicleInDB]:
        """
        Atualiza os dados de um veículo existente.
        """
        update_data = vehicle_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_by_id(vehicle_id)

        # Monta a query dinamicamente para atualizar apenas os campos enviados
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE vehicle SET {set_clause} WHERE id = %s;"
        
        params = tuple(update_data.values()) + (vehicle_id,)

        await self._execute_query(query, params=params)        
        return await self.get_by_id(vehicle_id)

    async def delete(self, vehicle_id: int) -> bool:
        """
        Deleta um veículo do banco de dados.
        """
        query = "DELETE FROM vehicle WHERE id = %s;"
        rows_affected = await self._execute_query(query, params=(vehicle_id,))
        return rows_affected is not None and rows_affected > 0