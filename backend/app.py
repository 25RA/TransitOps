from fastapi import FastAPI
import models
from routers.vehicles import router as vehicle_router
from routers.drivers import router as driver_router
from routers.trips import router as trip_router
from routers.maintenance import router as maintenance_router
from database import Base, engine
from config import settings
from routers.fuel import router as fuel_router
from routers.expense import router as expense_router
from routers.dashboard import router as dashboard_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Smart Transport Operations Platform"
)

Base.metadata.create_all(bind=engine)
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(trip_router)
app.include_router(maintenance_router)
app.include_router(fuel_router)
app.include_router(expense_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "TransitOps API Running Successfully",
        "version": settings.VERSION,
        "status": "healthy"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }