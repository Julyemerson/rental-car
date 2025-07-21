from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    "Modelo base para os usuários. Contém os campos comuns."
    name: str
    last_name: str
    cpf: str
    email: EmailStr
    birth_at: date

class UserCreate(UserBase):
    "Modelo para criar um novo usuário. Todos os campos são obrigatórios."
    pass

class UserUpdate(BaseModel):
    "Modelo para atualizar os dados de um usuário. Todos os campos são opcionais. Use apenas os campos que deseja atualizar."
    name: Optional[str] = None
    last_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_at: Optional[date] = None

class UserInDB(UserBase):
    "Modelo para representar um usuário no banco de dados."
    id: int