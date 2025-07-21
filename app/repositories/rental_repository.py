import aiomysql
from typing import List, Optional
from .base_repository import BaseRepository
from ..schemas.rental import RentalCreate, RentalUpdate, RentalInDB, VehicleRentalCount, RentalReport

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
    
    async def get_summary_report(self) -> RentalReport:
        """
        Gera um relatório de resumo com faturamento total e veículos mais alugados.
        """
        # Query 1: Calcular o faturamento total
        revenue_query = "SELECT SUM(rent_value) as total FROM rental;"
        revenue_result = await self._execute_query(revenue_query, fetch='one')
        total_revenue = revenue_result['total'] if revenue_result and revenue_result['total'] else 0

        # Query 2: Contar aluguéis por veículo e juntar com a tabela de veículos
        # para obter os nomes, ordenando pelos mais alugados.
        count_query = """
            SELECT 
                r.id_vehicle, 
                v.brand, 
                v.model, 
                COUNT(r.id_vehicle) as rental_count
            FROM rental r
            JOIN vehicle v ON r.id_vehicle = v.id
            GROUP BY r.id_vehicle, v.brand, v.model
            ORDER BY rental_count DESC
            LIMIT 5;
        """
        count_records = await self._execute_query(count_query, fetch='all')
        
        # Constrói a lista de veículos mais alugados
        most_rented = [VehicleRentalCount(**record) for record in (count_records or [])]
        
        # Retorna o objeto de relatório completo
        return RentalReport(
            total_revenue=total_revenue,
            most_rented_vehicle=most_rented
        )