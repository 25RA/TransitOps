from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TripBase(BaseModel):
    vehicle_id: int = Field(
        ...,
        gt=0,
        examples=[1]
    )

    driver_id: int = Field(
        ...,
        gt=0,
        examples=[1]
    )

    source: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Raipur"]
    )

    destination: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Bilaspur"]
    )

    start_time: datetime = Field(
        ...,
        examples=["2026-07-12T09:00:00"]
    )

    end_time: Optional[datetime] = Field(
        default=None,
        examples=["2026-07-12T14:30:00"]
    )

    distance_km: float = Field(
        ...,
        gt=0,
        examples=[125.5]
    )

    cargo_weight: float = Field(
        default=0,
        ge=0,
        examples=[350]
    )

    status: str = Field(
        default="Scheduled",
        examples=["Scheduled"]
    )


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    vehicle_id: Optional[int] = Field(
        default=None,
        gt=0,
        examples=[1]
    )

    driver_id: Optional[int] = Field(
        default=None,
        gt=0,
        examples=[1]
    )

    source: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        examples=["Raipur"]
    )

    destination: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        examples=["Bilaspur"]
    )

    start_time: Optional[datetime] = Field(
        default=None,
        examples=["2026-07-12T09:00:00"]
    )

    end_time: Optional[datetime] = Field(
        default=None,
        examples=["2026-07-12T14:30:00"]
    )

    distance_km: Optional[float] = Field(
        default=None,
        gt=0,
        examples=[125.5]
    )

    cargo_weight: Optional[float] = Field(
        default=None,
        ge=0,
        examples=[350]
    )

    status: Optional[str] = Field(
        default=None,
        examples=["Completed"]
    )


class TripResponse(TripBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )