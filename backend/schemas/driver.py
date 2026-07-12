from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DriverBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        examples=["Rahul Sharma"]
    )

    license_number: str = Field(
        ...,
        min_length=3,
        max_length=50,
        examples=["DL123456789"]
    )

    license_category: str = Field(
        ...,
        min_length=1,
        max_length=20,
        examples=["LMV"]
    )

    license_expiry_date: date = Field(
        ...,
        examples=["2028-12-31"]
    )

    contact_number: str = Field(
        ...,
        min_length=10,
        max_length=15,
        examples=["9876543210"]
    )

    safety_score: float = Field(
        default=100,
        ge=0,
        le=100,
        examples=[95]
    )

    status: str = Field(
        default="Available",
        examples=["Available"]
    )


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        examples=["Rahul Sharma"]
    )

    license_category: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
        examples=["LMV"]
    )

    license_expiry_date: Optional[date] = Field(
        default=None,
        examples=["2028-12-31"]
    )

    contact_number: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=15,
        examples=["9876543210"]
    )

    safety_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        examples=[98]
    )

    status: Optional[str] = Field(
        default=None,
        examples=["Available"]
    )


class DriverResponse(DriverBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )