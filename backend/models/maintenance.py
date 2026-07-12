from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey

from models.base import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    service_type = Column(
        String(100),
        nullable=False
    )

    service_date = Column(
        Date,
        nullable=False
    )

    next_service_date = Column(
        Date,
        nullable=False
    )

    vendor = Column(
        String(100),
        nullable=False
    )

    cost = Column(
        Float,
        nullable=False
    )

    notes = Column(
        String(500),
        default=""
    )

    status = Column(
        String(30),
        default="Scheduled"
    )