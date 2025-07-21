from pydantic import BaseModel, EmailStr
from typing import Optional

class EmployeeBase(BaseModel): 
    name: str
    last_name: str
    cpf: Optional[str] = None
    email: EmailStr
    role: str

class CreateEmployee(EmployeeBase):
    pass

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    cpf: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None

class EmployeeInDB(EmployeeBase):
    id: int
