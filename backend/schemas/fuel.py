from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FuelBase(BaseModel):

    vehicle_id: int = Field(..., gt=0)

    date: date

    fuel_quantity: float = Field(..., gt=0)

    fuel_cost: float = Field(..., gt=0)

    odometer: float = Field(..., ge=0)

    fuel_station: str

    remarks: str = ""


class FuelCreate(FuelBase):
    pass


class FuelUpdate(BaseModel):

    vehicle_id: Optional[int] = None

    date: Optional[date] = None

    fuel_quantity: Optional[float] = Field(default=None, gt=0)

    fuel_cost: Optional[float] = Field(default=None, gt=0)

    odometer: Optional[float] = Field(default=None, ge=0)

    fuel_station: Optional[str] = None

    remarks: Optional[str] = None


class FuelResponse(FuelBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )