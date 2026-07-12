from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
import crud

from schemas.trip import (
    TripCreate,
    TripUpdate,
    TripResponse,
)

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


@router.get("/", response_model=list[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    return crud.get_all_trips(db)


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):

    trip = crud.get_trip_by_id(db, trip_id)

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    return trip


@router.post(
    "/",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED
)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db)
):

    try:
        return crud.create_trip(db, trip)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    trip: TripUpdate,
    db: Session = Depends(get_db)
):

    try:

        updated_trip = crud.update_trip(
            db,
            trip_id,
            trip
        )

        if not updated_trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found"
            )

        return updated_trip

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{trip_id}")
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    deleted_trip = crud.delete_trip(
        db,
        trip_id
    )

    if not deleted_trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found"
        )

    return {
        "message": "Trip deleted successfully"
    }