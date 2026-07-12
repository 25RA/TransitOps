from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import crud

from schemas.driver import (
    DriverCreate,
    DriverUpdate,
    DriverResponse,
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.get("/", response_model=list[DriverResponse])
def get_drivers(db: Session = Depends(get_db)):
    return crud.get_all_drivers(db)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    driver = crud.get_driver_by_id(db, driver_id)

    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )

    return driver


@router.post(
    "/",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED
)
def create_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_driver(db, driver)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    driver: DriverUpdate,
    db: Session = Depends(get_db)
):

    updated_driver = crud.update_driver(
        db,
        driver_id,
        driver
    )

    if not updated_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )

    return updated_driver


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):

    deleted_driver = crud.delete_driver(
        db,
        driver_id
    )

    if not deleted_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver not found"
        )

    return {
        "message": "Driver deleted successfully"
    }