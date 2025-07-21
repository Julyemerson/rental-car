from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class VehicleBase(BaseModel):
    """Base model with common vehicle fields."""
    brand: str = Field(..., min_length=2, max_length=255, examples=["Volkswagen"])
    model: str = Field(..., min_length=1, max_length=255, examples=["Golf"])
    vehicle_type: Literal['car', 'motorcycle']
    year: int = Field(..., ge=1900, le=2100, examples=[2021]) # ge = greater than or equal
    license_plate: str = Field(..., min_length=7, max_length=10, examples=["BRA2E19"])
    color: Optional[str] = Field(None, max_length=100, examples=["Black"])
    mileage: int = Field(..., ge=0, examples=[50000])
    available: bool = Field(True, examples=[True])
    daily_charge: float = Field(..., gt=0, examples=[120.50])

class VehicleCreate(VehicleBase):
    "Modelo para criar novo veículo."
    pass

class VehicleUpdate(BaseModel):
    """
    Model for updating a vehicle. All fields are optional to allow
    for partial updates (PATCH-like behavior).
    """
    brand: Optional[str] = Field(None, min_length=2, max_length=255)
    model: Optional[str] = Field(None, min_length=1, max_length=255)
    vehicle_type: Optional[Literal['car', 'motorcycle']] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    license_plate: Optional[str] = Field(None, min_length=7, max_length=10)
    color: Optional[str] = Field(None, max_length=100)
    mileage: Optional[int] = Field(None, ge=0)
    available: Optional[bool] = None
    daily_charge: Optional[float] = Field(None, gt=0)

class VehicleInDB(VehicleBase):
    """Model representing the vehicle as it exists in the database."""
    id: int
    registration_date: datetime