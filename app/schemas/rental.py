from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date

class RentalBase(BaseModel):
    """Base model with common fields for a rental."""
    return_date: date = Field(..., examples=["2025-08-10"])
    rent_value: int = Field(..., gt=0, description="Rental value in cents to avoid float issues, or as integer.")
    
    # Foreign Keys
    id_user: int = Field(..., gt=0, examples=[1])
    id_vehicle: int = Field(..., gt=0, examples=[2])
    id_employee: int = Field(..., gt=0, examples=[1])


class RentalCreate(RentalBase):
    """
    Model for creating a new rental.
    The rent_date is optional here and will default to today's date if not provided,
    mimicking the SQL 'DEFAULT CURRENT_DATE'.
    """
    rent_date: date = Field(default_factory=date.today, examples=["2025-08-01"])

    # This is a model-level validator. It runs after all individual fields are validated.
    @model_validator(mode='after')
    def check_dates(self) -> 'RentalCreate':
        """Ensures that the return_date is after the rent_date."""
        if self.rent_date and self.return_date:
            if self.return_date <= self.rent_date:
                raise ValueError("Return date must be after the rent date.")
        return self


class RentalUpdate(BaseModel):
    """Model for updating a rental. All fields are optional."""
    rent_date: Optional[date] = None
    return_date: Optional[date] = None
    rent_value: Optional[int] = Field(None, gt=0)
    id_user: Optional[int] = Field(None, gt=0)
    id_vehicle: Optional[int] = Field(None, gt=0)
    id_employee: Optional[int] = Field(None, gt=0)


class RentalInDB(RentalBase):
    """Model representing a rental as it exists in the database."""
    id: int