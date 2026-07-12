from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
import crud

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/daily")
def daily_report(db: Session = Depends(get_db)):
    return crud.get_daily_report(db)


@router.get("/weekly")
def weekly_report(db: Session = Depends(get_db)):
    return crud.get_weekly_report(db)


@router.get("/monthly")
def monthly_report(db: Session = Depends(get_db)):
    return crud.get_monthly_report(db)


@router.get("/fleet")
def fleet_report(db: Session = Depends(get_db)):
    return crud.get_fleet_report(db)


@router.get("/drivers")
def driver_report(db: Session = Depends(get_db)):
    return crud.get_driver_report(db)


@router.get("/vehicles")
def vehicle_report(db: Session = Depends(get_db)):
    return crud.get_vehicle_report(db)


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):

    filepath = crud.export_csv(db)

    return FileResponse(
        filepath,
        media_type="text/csv",
        filename="transit_report.csv"
    )


@router.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):

    filepath = crud.export_pdf(db)

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename="transit_report.pdf"
    )