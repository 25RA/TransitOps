from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey

from models.base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    driver_id = Column(
        Integer,
        ForeignKey("drivers.id"),
        nullable=False
    )

    source = Column(
        String(100),
        nullable=False
    )

    destination = Column(
        String(100),
        nullable=False
    )

    start_time = Column(
        DateTime,
        nullable=False
    )

    end_time = Column(
        DateTime,
        nullable=True
    )

    distance_km = Column(
        Float,
        nullable=False
    )

    cargo_weight = Column(
        Float,
        default=0
    )

    status = Column(
        String(30),
        default="Scheduled"
    )