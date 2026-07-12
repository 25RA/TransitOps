from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import crud

from schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse,
)

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.get("/", response_model=list[MaintenanceResponse])
def get_maintenance(db: Session = Depends(get_db)):
    return crud.get_all_maintenance(db)


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance_by_id(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    record = crud.get_maintenance_by_id(
        db,
        maintenance_id
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found."
        )

    return record


@router.get(
    "/vehicle/{vehicle_id}",
    response_model=list[MaintenanceResponse]
)
def get_vehicle_history(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_vehicle_maintenance(
        db,
        vehicle_id
    )


@router.post(
    "/",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_maintenance(
    maintenance: MaintenanceCreate,
    db: Session = Depends(get_db)
):

    try:
        return crud.create_maintenance(
            db,
            maintenance
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put(
    "/{maintenance_id}",
    response_model=MaintenanceResponse
)
def update_maintenance(
    maintenance_id: int,
    maintenance: MaintenanceUpdate,
    db: Session = Depends(get_db)
):

    try:

        record = crud.update_maintenance(
            db,
            maintenance_id,
            maintenance
        )

        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Maintenance record not found."
            )

        return record

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):

    record = crud.delete_maintenance(
        db,
        maintenance_id
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Maintenance record not found."
        )

    return {
        "message": "Maintenance record deleted successfully"
    }