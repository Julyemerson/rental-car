# /app/repositories/employee_repository.py

import aiomysql
from typing import List, Optional
from .base_repository import BaseRepository
from ..schemas.employee import CreateEmployee, UpdateEmployee, EmployeeInDB

class EmployeeRepository(BaseRepository):
    
    async def get_all(self) -> List[EmployeeInDB]:
        """Busca todos os funcionários cadastrados."""
        query = "SELECT * FROM employee;"
        records = await self._execute_query(query, fetch='all')
        # Adopts the more concise pattern for handling an empty result.
        return [EmployeeInDB(**record) for record in (records or [])]

    async def get_by_id(self, employee_id: int) -> Optional[EmployeeInDB]:
        """Busca um único funcionário pelo seu ID."""
        query = "SELECT * FROM employee WHERE id = %s;"
        record = await self._execute_query(query, params=(employee_id,), fetch='one')
        return EmployeeInDB(**record) if record else None

    async def create(self, employee: CreateEmployee) -> EmployeeInDB:
        """
        Insere um novo funcionário no banco de dados.
        """
        query = """
            INSERT INTO employee (name, last_name, cpf, email, role)
            VALUES (%s, %s, %s, %s, %s);
        """
        params = (
            employee.name, employee.last_name, employee.cpf, 
            employee.email, employee.role
        )
        new_id = await self._execute_query(query, params=params)
        
        if new_id is None:
            raise ValueError("Failed to create employee: No ID returned from database.")
            
        # Constructs the response object without a second DB query.
        return EmployeeInDB(id=new_id, **employee.model_dump())

    async def update(self, employee_id: int, employee_update: UpdateEmployee) -> Optional[EmployeeInDB]:
        """Atualiza os dados de um funcionário existente."""
        update_data = employee_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_by_id(employee_id)

        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE employee SET {set_clause} WHERE id = %s;"
        
        params = tuple(update_data.values()) + (employee_id,)
        await self._execute_query(query, params=params)
        return await self.get_by_id(employee_id)

    async def delete(self, employee_id: int) -> bool:
        """
        Deleta um funcionário do banco de dados.
        Confirms deletion by checking if the record still exists.
        """
        query = "DELETE FROM employee WHERE id = %s;"
        await self._execute_query(query, params=(employee_id,))
        # This is a more robust way to confirm deletion.
        return await self.get_by_id(employee_id) is None
