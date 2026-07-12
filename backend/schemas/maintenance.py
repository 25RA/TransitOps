from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class MaintenanceBase(BaseModel):

    vehicle_id: int = Field(
        ...,
        gt=0,
        examples=[1]
    )

    service_type: str = Field(
        ...,
        examples=["Oil Change"]
    )

    service_date: date = Field(
        ...,
        examples=["2026-07-12"]
    )

    next_service_date: date = Field(
        ...,
        examples=["2026-10-12"]
    )

    vendor: str = Field(
        ...,
        examples=["Tata Service Center"]
    )

    cost: float = Field(
        ...,
        gt=0,
        examples=[4500]
    )

    notes: str = Field(
        default="",
        examples=["Changed engine oil and filters."]
    )

    status: str = Field(
        default="Scheduled",
        examples=["Scheduled"]
    )


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceUpdate(BaseModel):

    vehicle_id: Optional[int] = None

    service_type: Optional[str] = None

    service_date: Optional[date] = None

    next_service_date: Optional[date] = None

    vendor: Optional[str] = None

    cost: Optional[float] = Field(
        default=None,
        gt=0
    )

    notes: Optional[str] = None

    status: Optional[str] = None


class MaintenanceResponse(MaintenanceBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )