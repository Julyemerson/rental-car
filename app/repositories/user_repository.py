from typing import List, Optional
from .base_repository import BaseRepository
from ..schemas.user import UserCreate, UserUpdate, UserInDB

class UserRepository(BaseRepository):
    
    async def get_all(self) -> List[UserInDB]:
        query = "SELECT id, name, last_name, cpf, email, birth_at FROM user;"
        records = await self._execute_query(query, fetch='all')
        return [UserInDB(**record) for record in (records or [])]

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        query = "SELECT id, name, last_name, cpf, email, birth_at FROM user WHERE id = %s;"
        record = await self._execute_query(query, (user_id,), fetch='one')
        return UserInDB(**record) if record else None

    async def create(self, user: UserCreate) -> UserInDB:
        query = """
            INSERT INTO user (name, last_name, cpf, email, birth_at)
            VALUES (%s, %s, %s, %s, %s);
        """
        params = (user.name, user.last_name, user.cpf, user.email, user.birth_at)
        new_id = await self._execute_query(query, params)
        if new_id is None:
            raise ValueError("Failed to create user: no ID returned from database.")
        return UserInDB(id=new_id, **user.model_dump())

    async def update(self, user_id: int, user_update: UserUpdate) -> Optional[UserInDB]:
        # Pega os dados que foram realmente enviados para atualização
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(user_id) # Se nada foi enviado, retorna o usuário atual

        # Monta a query dinamicamente para atualizar apenas os campos enviados
        set_clause = ", ".join([f"{key} = %s" for key in update_data.keys()])
        query = f"UPDATE user SET {set_clause} WHERE id = %s;"
        params = tuple(update_data.values()) + (user_id,)
        
        await self._execute_query(query, params)
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> bool:
        query = "DELETE FROM user WHERE id = %s;"
        await self._execute_query(query, (user_id,))
        # Podemos verificar se a deleção foi bem-sucedida checando se o usuário ainda existe
        return await self.get_by_id(user_id) is None