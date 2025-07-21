# /app/database/base_repository.py

import aiomysql
from typing import Optional, Any

class BaseRepository:
    """
    Classe base que contém a lógica de execução de queries,
    para ser reutilizada por todos os outros repositórios.
    """
    def __init__(self, pool: aiomysql.Pool):
        self.pool = pool

    async def _execute_query(
        self, 
        query: str, 
        params: Optional[tuple] = None, 
        fetch: Optional[str] = None
    ) -> Optional[Any]:
        """
        Método auxiliar genérico para executar queries no banco de dados.
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, params or ())
                
                if fetch == 'one':
                    return await cursor.fetchone()
                if fetch == 'all':
                    return await cursor.fetchall()
                
                # Para INSERT, retorna o ID da nova linha.
                if query.strip().upper().startswith('INSERT'):
                    return cursor.lastrowid
                
                # Para UPDATE e DELETE, podemos retornar o número de linhas afetadas.
                if query.strip().upper().startswith(('UPDATE', 'DELETE')):
                    return cursor.rowcount
                
                return None