from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey

from models.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(
        Integer,
        ForeignKey("vehicles.id"),
        nullable=False
    )

    expense_type = Column(
        String(100),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    expense_date = Column(
        Date,
        nullable=False
    )

    vendor = Column(
        String(100),
        nullable=False
    )

    notes = Column(
        String(500),
        default=""
    )