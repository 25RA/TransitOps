from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):

    vehicle_id: int = Field(..., gt=0)

    expense_type: str

    amount: float = Field(..., gt=0)

    expense_date: date

    vendor: str

    notes: str = ""


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):

    vehicle_id: Optional[int] = None

    expense_type: Optional[str] = None

    amount: Optional[float] = Field(default=None, gt=0)

    expense_date: Optional[date] = None

    vendor: Optional[str] = None

    notes: Optional[str] = None


class ExpenseResponse(ExpenseBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )