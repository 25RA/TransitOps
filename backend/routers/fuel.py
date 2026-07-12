from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import crud

from schemas.fuel import (
    FuelCreate,
    FuelUpdate,
    FuelResponse,
)

router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"]
)


@router.get("/", response_model=list[FuelResponse])
def get_fuel_logs(db: Session = Depends(get_db)):
    return crud.get_all_fuel_logs(db)


@router.get("/{fuel_id}", response_model=FuelResponse)
def get_fuel(fuel_id: int, db: Session = Depends(get_db)):

    fuel = crud.get_fuel_by_id(db, fuel_id)

    if not fuel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fuel record not found."
        )

    return fuel


@router.post(
    "/",
    response_model=FuelResponse,
    status_code=status.HTTP_201_CREATED
)
def create_fuel(
    fuel: FuelCreate,
    db: Session = Depends(get_db)
):

    try:
        return crud.create_fuel(db, fuel)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{fuel_id}", response_model=FuelResponse)
def update_fuel(
    fuel_id: int,
    fuel: FuelUpdate,
    db: Session = Depends(get_db)
):

    try:

        record = crud.update_fuel(
            db,
            fuel_id,
            fuel
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fuel record not found."
            )

        return record

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{fuel_id}")
def delete_fuel(
    fuel_id: int,
    db: Session = Depends(get_db)
):

    record = crud.delete_fuel(
        db,
        fuel_id
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fuel record not found."
        )

    return {
        "message": "Fuel record deleted successfully"
    }