from sqlalchemy import Column, Integer, String, Float, Date

from models.base import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    license_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    license_category = Column(
        String(20),
        nullable=False
    )

    license_expiry_date = Column(
        Date,
        nullable=False
    )

    contact_number = Column(
        String(15),
        nullable=False
    )

    safety_score = Column(
        Float,
        default=100
    )

    status = Column(
        String(20),
        default="Available"
    )