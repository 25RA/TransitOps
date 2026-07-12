from fastapi import FastAPI
import models
from routers.vehicles import router as vehicle_router
from routers.drivers import router as driver_router
from database import Base, engine
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Smart Transport Operations Platform"
)

Base.metadata.create_all(bind=engine)
app.include_router(vehicle_router)
app.include_router(driver_router)
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