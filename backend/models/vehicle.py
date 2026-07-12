from sqlalchemy import Column, Integer, String, Float

from models.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    registration_number = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    vehicle_name = Column(
        String(100),
        nullable=False
    )

    vehicle_type = Column(
        String(50),
        nullable=False
    )

    max_load_capacity = Column(
        Float,
        nullable=False
    )

    odometer = Column(
        Float,
        default=0
    )

    acquisition_cost = Column(
        Float,
        default=0
    )

    status = Column(
        String(30),
        default="Available"
    )