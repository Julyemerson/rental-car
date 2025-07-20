# database.py
import aiomysql
import os

# Em um projeto real, use variáveis de ambiente para segurança!
DB_HOST = os.getenv("MARIADB_HOST", "localhost")
DB_USER = os.getenv("MARIADB_USER", "root")
DB_PASSWORD = os.getenv("MARIADB_PASSWORD", "qwe123poi")
DB_NAME = os.getenv("MARIADB_DATABASE", "br-rental-car")

# O 'pool' de conexões é uma coleção de conexões abertas que podem ser
# reutilizadas, o que é muito mais eficiente do que abrir e fechar
# uma conexão para cada operação.
async def get_db_pool():
    """Cria e retorna um pool de conexões com o banco de dados."""
    return await aiomysql.create_pool(
        host=DB_HOST,
        port=3306,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True  # Salva as alterações automaticamente
    )