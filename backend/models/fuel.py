from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey

from models.base import Base


class Fuel(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    date = Column(
        Date,
        nullable=False
    )

    fuel_quantity = Column(
        Float,
        nullable=False
    )

    fuel_cost = Column(
        Float,
        nullable=False
    )

    odometer = Column(
        Float,
        nullable=False
    )

    fuel_station = Column(
        String(100),
        nullable=False
    )

    remarks = Column(
        String(300),
        default=""
    )