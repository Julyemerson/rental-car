import os 
import mysql.connector
from mysql.connector import Error

class Database:
    """
    Uma classe que gerencia a conexão com o MariaDB usando um gerenciador de contexto.
    É a forma recomendada e mais segura de usar.
    """
    def __init__(self):
        self.host = os.getenv("MARIADB_HOST", 'localhost')
        self.user = os.getenv("MARIADB_USER")
        self.password = os.getenv("MARIADB_PASSWORD")
        self.database = os.getenv("MARIADB_DATABASE")
        self._conn = None
        self._cursor = None

    def __enter__(self):
        """
        Método de entrada do gerenciador de contexto.
        É aqui que abrimos a conexão.
        """
        try:
            self._conn = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            self._cursor = self._conn.cursor(dictionary=True)
            print(f"Conexão com '{self.database}' aberta.")
            return self
        except Error as e:
            print(f"Error ao conectar ao MariaDB: {e}")
            raise e
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Método de saída do gerenciador de contexto.
        É aqui que fechamos tudo, não importa o que aconteça.
        """
        if self._conn and self._conn.is_connected():
            self._cursor.close()
            self._conn.close()
            print("Conexão com o MariaDB fechada.")

    def execute(self, sql, params=None):
        """
        Executa uma query que não retorna dados (INSERT, UPDATE, DELETE).
        Sempre use parâmetros para evitar SQL Injection!
        """
        self._cursor.execute(sql, params or ())
        self._conn.commit()
        return self._cursor.lastrowid()
    
    def fetchall(self, sql, params=None):
        """Busca todos os resultados de uma query (SELECT)."""
        self._cursor.execute(sql, params or ())
        return self._cursor.fetchall()

    def fetchone(self, sql, params=None):
        """Busca o primeiro resultado de uma query (SELECT)."""
        self._cursor.execute(sql, params or ())
        return self._cursor.fetchone()

    def commit(self):
        """Commits the current transaction to the database."""
        self._conn.commit()

    def rollback(self):
        """Rolls back the current transaction."""
        self._conn.rollback()
    