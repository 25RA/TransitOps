from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class VehicleBase(BaseModel):
    registration_number: str = Field(..., min_length=3, max_length=30)
    vehicle_name: str = Field(..., min_length=2, max_length=100)
    vehicle_type: str
    max_load_capacity: float = Field(..., gt=0)
    odometer: float = Field(default=0, ge=0)
    acquisition_cost: float = Field(default=0, ge=0)
    status: str = "Available"


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    vehicle_name: Optional[str] = None
    vehicle_type: Optional[str] = None
    max_load_capacity: Optional[float] = Field(default=None, gt=0)
    odometer: Optional[float] = Field(default=None, ge=0)
    acquisition_cost: Optional[float] = Field(default=None, ge=0)
    status: Optional[str] = None


class VehicleResponse(VehicleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)