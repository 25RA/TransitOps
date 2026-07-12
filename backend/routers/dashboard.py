from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import crud

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return crud.get_dashboard_summary(db)


@router.get("/fleet")
def fleet_statistics(db: Session = Depends(get_db)):
    return crud.get_fleet_statistics(db)


@router.get("/drivers")
def driver_statistics(db: Session = Depends(get_db)):
    return crud.get_driver_statistics(db)


@router.get("/fuel")
def fuel_statistics(db: Session = Depends(get_db)):
    return crud.get_fuel_statistics(db)


@router.get("/maintenance")
def maintenance_statistics(db: Session = Depends(get_db)):
    return crud.get_maintenance_statistics(db)


@router.get("/expenses")
def expense_statistics(db: Session = Depends(get_db)):
    return crud.get_expense_statistics(db)


@router.get("/alerts")
def alerts(db: Session = Depends(get_db)):
    return crud.get_dashboard_alerts(db)