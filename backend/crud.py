from sqlalchemy.orm import Session

from models.vehicle import Vehicle
from schemas.vehicle import VehicleCreate, VehicleUpdate

import os
import csv

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# ==========================
# VEHICLE CRUD OPERATIONS
# ==========================

def get_all_vehicles(db: Session):
    return db.query(Vehicle).order_by(Vehicle.id.desc()).all()


def get_vehicle_by_id(db: Session, vehicle_id: int):
    return (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id)
        .first()
    )


def get_vehicle_by_registration(db: Session, registration_number: str):
    return (
        db.query(Vehicle)
        .filter(Vehicle.registration_number == registration_number)
        .first()
    )


def create_vehicle(db: Session, vehicle: VehicleCreate):

    existing = get_vehicle_by_registration(
        db,
        vehicle.registration_number
    )

    if existing:
        raise ValueError("Vehicle registration number already exists.")

    db_vehicle = Vehicle(
        registration_number=vehicle.registration_number,
        vehicle_name=vehicle.vehicle_name,
        vehicle_type=vehicle.vehicle_type,
        max_load_capacity=vehicle.max_load_capacity,
        odometer=vehicle.odometer,
        acquisition_cost=vehicle.acquisition_cost,
        status=vehicle.status
    )

    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


def update_vehicle(
    db: Session,
    vehicle_id: int,
    vehicle: VehicleUpdate
):

    db_vehicle = get_vehicle_by_id(db, vehicle_id)

    if not db_vehicle:
        return None

    update_data = vehicle.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_vehicle, key, value)

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


def delete_vehicle(
    db: Session,
    vehicle_id: int
):

    db_vehicle = get_vehicle_by_id(db, vehicle_id)

    if not db_vehicle:
        return None

    db.delete(db_vehicle)
    db.commit()

    return db_vehicle

# ==========================
# DRIVER CRUD OPERATIONS
# ==========================

from models.driver import Driver
from schemas.driver import DriverCreate, DriverUpdate


def get_all_drivers(db: Session):
    return db.query(Driver).order_by(Driver.id.desc()).all()


def get_driver_by_id(db: Session, driver_id: int):
    return (
        db.query(Driver)
        .filter(Driver.id == driver_id)
        .first()
    )


def get_driver_by_license(db: Session, license_number: str):
    return (
        db.query(Driver)
        .filter(Driver.license_number == license_number)
        .first()
    )


def create_driver(db: Session, driver: DriverCreate):

    existing = get_driver_by_license(
        db,
        driver.license_number
    )

    if existing:
        raise ValueError("Driver license already exists.")

    db_driver = Driver(
        name=driver.name,
        license_number=driver.license_number,
        license_category=driver.license_category,
        license_expiry_date=driver.license_expiry_date,
        contact_number=driver.contact_number,
        safety_score=driver.safety_score,
        status=driver.status
    )

    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)

    return db_driver


def update_driver(
    db: Session,
    driver_id: int,
    driver: DriverUpdate
):

    db_driver = get_driver_by_id(db, driver_id)

    if not db_driver:
        return None

    update_data = driver.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_driver, key, value)

    db.commit()
    db.refresh(db_driver)

    return db_driver


def delete_driver(
    db: Session,
    driver_id: int
):

    db_driver = get_driver_by_id(db, driver_id)

    if not db_driver:
        return None

    db.delete(db_driver)
    db.commit()

    return db_driver

# ==========================
# TRIP CRUD OPERATIONS
# ==========================

from models.trip import Trip
from models.vehicle import Vehicle
from models.driver import Driver

from schemas.trip import TripCreate, TripUpdate


def get_all_trips(db: Session):
    return db.query(Trip).order_by(Trip.id.desc()).all()


def get_trip_by_id(db: Session, trip_id: int):
    return (
        db.query(Trip)
        .filter(Trip.id == trip_id)
        .first()
    )


def create_trip(db: Session, trip: TripCreate):

    # Validate Vehicle
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    if not vehicle:
        raise ValueError("Vehicle not found.")

    # Validate Driver
    driver = (
        db.query(Driver)
        .filter(Driver.id == trip.driver_id)
        .first()
    )

    if not driver:
        raise ValueError("Driver not found.")

    # Check Vehicle Availability
    active_vehicle_trip = (
        db.query(Trip)
        .filter(
            Trip.vehicle_id == trip.vehicle_id,
            Trip.status.in_(["Scheduled", "In Progress"])
        )
        .first()
    )

    if active_vehicle_trip:
        raise ValueError("Vehicle already assigned to another active trip.")

    # Check Driver Availability
    active_driver_trip = (
        db.query(Trip)
        .filter(
            Trip.driver_id == trip.driver_id,
            Trip.status.in_(["Scheduled", "In Progress"])
        )
        .first()
    )

    if active_driver_trip:
        raise ValueError("Driver already assigned to another active trip.")

    db_trip = Trip(
        vehicle_id=trip.vehicle_id,
        driver_id=trip.driver_id,
        source=trip.source,
        destination=trip.destination,
        start_time=trip.start_time,
        end_time=trip.end_time,
        distance_km=trip.distance_km,
        cargo_weight=trip.cargo_weight,
        status=trip.status
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip


def update_trip(
    db: Session,
    trip_id: int,
    trip: TripUpdate
):

    db_trip = get_trip_by_id(db, trip_id)

    if not db_trip:
        return None

    update_data = trip.model_dump(exclude_unset=True)

    # Validate Vehicle if updated
    if "vehicle_id" in update_data:

        vehicle = (
            db.query(Vehicle)
            .filter(Vehicle.id == update_data["vehicle_id"])
            .first()
        )

        if not vehicle:
            raise ValueError("Vehicle not found.")

    # Validate Driver if updated
    if "driver_id" in update_data:

        driver = (
            db.query(Driver)
            .filter(Driver.id == update_data["driver_id"])
            .first()
        )

        if not driver:
            raise ValueError("Driver not found.")

    for key, value in update_data.items():
        setattr(db_trip, key, value)

    db.commit()
    db.refresh(db_trip)

    return db_trip


def delete_trip(
    db: Session,
    trip_id: int
):

    db_trip = get_trip_by_id(db, trip_id)

    if not db_trip:
        return None

    db.delete(db_trip)
    db.commit()

    return db_trip

# ==========================
# MAINTENANCE CRUD OPERATIONS
# ==========================

from models.maintenance import Maintenance
from models.vehicle import Vehicle

from schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
)


def get_all_maintenance(db: Session):
    return (
        db.query(Maintenance)
        .order_by(Maintenance.service_date.desc())
        .all()
    )


def get_maintenance_by_id(
    db: Session,
    maintenance_id: int
):
    return (
        db.query(Maintenance)
        .filter(Maintenance.id == maintenance_id)
        .first()
    )


def get_vehicle_maintenance(
    db: Session,
    vehicle_id: int
):
    return (
        db.query(Maintenance)
        .filter(Maintenance.vehicle_id == vehicle_id)
        .order_by(Maintenance.service_date.desc())
        .all()
    )


def create_maintenance(
    db: Session,
    maintenance: MaintenanceCreate
):

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == maintenance.vehicle_id)
        .first()
    )

    if not vehicle:
        raise ValueError("Vehicle not found.")

    if maintenance.next_service_date <= maintenance.service_date:
        raise ValueError(
            "Next service date must be after service date."
        )

    db_record = Maintenance(
        vehicle_id=maintenance.vehicle_id,
        service_type=maintenance.service_type,
        service_date=maintenance.service_date,
        next_service_date=maintenance.next_service_date,
        vendor=maintenance.vendor,
        cost=maintenance.cost,
        notes=maintenance.notes,
        status=maintenance.status
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    return db_record


def update_maintenance(
    db: Session,
    maintenance_id: int,
    maintenance: MaintenanceUpdate
):

    db_record = get_maintenance_by_id(
        db,
        maintenance_id
    )

    if not db_record:
        return None

    update_data = maintenance.model_dump(
        exclude_unset=True
    )

    if "vehicle_id" in update_data:

        vehicle = (
            db.query(Vehicle)
            .filter(
                Vehicle.id == update_data["vehicle_id"]
            )
            .first()
        )

        if not vehicle:
            raise ValueError("Vehicle not found.")

    service_date = update_data.get(
        "service_date",
        db_record.service_date
    )

    next_service_date = update_data.get(
        "next_service_date",
        db_record.next_service_date
    )

    if next_service_date <= service_date:
        raise ValueError(
            "Next service date must be after service date."
        )

    for key, value in update_data.items():
        setattr(db_record, key, value)

    db.commit()
    db.refresh(db_record)

    return db_record


def delete_maintenance(
    db: Session,
    maintenance_id: int
):

    db_record = get_maintenance_by_id(
        db,
        maintenance_id
    )

    if not db_record:
        return None

    db.delete(db_record)
    db.commit()

    return db_record

# ==========================
# FUEL CRUD OPERATIONS
# ==========================

from models.fuel import Fuel
from schemas.fuel import FuelCreate, FuelUpdate


def get_all_fuel_logs(db: Session):
    return (
        db.query(Fuel)
        .order_by(Fuel.date.desc())
        .all()
    )


def get_fuel_by_id(db: Session, fuel_id: int):
    return (
        db.query(Fuel)
        .filter(Fuel.id == fuel_id)
        .first()
    )


def create_fuel(db: Session, fuel: FuelCreate):

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == fuel.vehicle_id)
        .first()
    )

    if not vehicle:
        raise ValueError("Vehicle not found.")

    db_fuel = Fuel(
        vehicle_id=fuel.vehicle_id,
        date=fuel.date,
        fuel_quantity=fuel.fuel_quantity,
        fuel_cost=fuel.fuel_cost,
        odometer=fuel.odometer,
        fuel_station=fuel.fuel_station,
        remarks=fuel.remarks
    )

    db.add(db_fuel)
    db.commit()
    db.refresh(db_fuel)

    return db_fuel


def update_fuel(
    db: Session,
    fuel_id: int,
    fuel: FuelUpdate
):

    db_fuel = get_fuel_by_id(
        db,
        fuel_id
    )

    if not db_fuel:
        return None

    update_data = fuel.model_dump(
        exclude_unset=True
    )

    if "vehicle_id" in update_data:

        vehicle = (
            db.query(Vehicle)
            .filter(
                Vehicle.id == update_data["vehicle_id"]
            )
            .first()
        )

        if not vehicle:
            raise ValueError("Vehicle not found.")

    for key, value in update_data.items():
        setattr(db_fuel, key, value)

    db.commit()
    db.refresh(db_fuel)

    return db_fuel


def delete_fuel(
    db: Session,
    fuel_id: int
):

    db_fuel = get_fuel_by_id(
        db,
        fuel_id
    )

    if not db_fuel:
        return None

    db.delete(db_fuel)
    db.commit()

    return db_fuel

# ==========================
# EXPENSE CRUD OPERATIONS
# ==========================

from models.expense import Expense
from schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
)


def get_all_expenses(db: Session):
    return (
        db.query(Expense)
        .order_by(Expense.expense_date.desc())
        .all()
    )


def get_expense_by_id(
    db: Session,
    expense_id: int
):
    return (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )


def create_expense(
    db: Session,
    expense: ExpenseCreate
):

    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.id == expense.vehicle_id
        )
        .first()
    )

    if not vehicle:
        raise ValueError("Vehicle not found.")

    db_expense = Expense(
        vehicle_id=expense.vehicle_id,
        expense_type=expense.expense_type,
        amount=expense.amount,
        expense_date=expense.expense_date,
        vendor=expense.vendor,
        notes=expense.notes
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


def update_expense(
    db: Session,
    expense_id: int,
    expense: ExpenseUpdate
):

    db_expense = get_expense_by_id(
        db,
        expense_id
    )

    if not db_expense:
        return None

    update_data = expense.model_dump(
        exclude_unset=True
    )

    if "vehicle_id" in update_data:

        vehicle = (
            db.query(Vehicle)
            .filter(
                Vehicle.id == update_data["vehicle_id"]
            )
            .first()
        )

        if not vehicle:
            raise ValueError("Vehicle not found.")

    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)

    return db_expense


def delete_expense(
    db: Session,
    expense_id: int
):

    db_expense = get_expense_by_id(
        db,
        expense_id
    )

    if not db_expense:
        return None

    db.delete(db_expense)
    db.commit()

    return db_expense

# ==========================================
# DASHBOARD ANALYTICS
# ==========================================

from sqlalchemy import func
from datetime import date, timedelta

from models.vehicle import Vehicle
from models.driver import Driver
from models.trip import Trip
from models.fuel import Fuel
from models.maintenance import Maintenance
from models.expense import Expense


# ==========================
# DASHBOARD SUMMARY
# ==========================

def get_dashboard_summary(db: Session):

    total_vehicles = db.query(Vehicle).count()

    available_vehicles = (
        db.query(Vehicle)
        .filter(Vehicle.status == "Available")
        .count()
    )

    active_trips = (
        db.query(Trip)
        .filter(Trip.status == "In Progress")
        .count()
    )

    total_drivers = db.query(Driver).count()

    available_drivers = (
        db.query(Driver)
        .filter(Driver.status == "Available")
        .count()
    )

    fuel_cost = (
        db.query(func.coalesce(func.sum(Fuel.fuel_cost), 0))
        .scalar()
    )

    maintenance_cost = (
        db.query(func.coalesce(func.sum(Maintenance.cost), 0))
        .scalar()
    )

    expense_cost = (
        db.query(func.coalesce(func.sum(Expense.amount), 0))
        .scalar()
    )

    return {
        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "active_trips": active_trips,
        "total_drivers": total_drivers,
        "available_drivers": available_drivers,
        "fuel_cost": round(fuel_cost, 2),
        "maintenance_cost": round(maintenance_cost, 2),
        "expense_cost": round(expense_cost, 2),
        "total_operational_cost": round(
            fuel_cost +
            maintenance_cost +
            expense_cost,
            2
        )
    }


# ==========================
# FLEET STATISTICS
# ==========================

def get_fleet_statistics(db: Session):

    available = (
        db.query(Vehicle)
        .filter(Vehicle.status == "Available")
        .count()
    )

    in_use = (
        db.query(Vehicle)
        .filter(Vehicle.status == "In Use")
        .count()
    )

    maintenance = (
        db.query(Vehicle)
        .filter(Vehicle.status == "Maintenance")
        .count()
    )

    inactive = (
        db.query(Vehicle)
        .filter(Vehicle.status == "Inactive")
        .count()
    )

    return {
        "available": available,
        "in_use": in_use,
        "maintenance": maintenance,
        "inactive": inactive
    }


# ==========================
# DRIVER STATISTICS
# ==========================

def get_driver_statistics(db: Session):

    available = (
        db.query(Driver)
        .filter(Driver.status == "Available")
        .count()
    )

    assigned = (
        db.query(Driver)
        .filter(Driver.status == "Assigned")
        .count()
    )

    inactive = (
        db.query(Driver)
        .filter(Driver.status == "Inactive")
        .count()
    )

    average_score = (
        db.query(
            func.coalesce(
                func.avg(
                    Driver.safety_score
                ),
                0
            )
        ).scalar()
    )

    return {
        "total_drivers": db.query(Driver).count(),
        "available": available,
        "assigned": assigned,
        "inactive": inactive,
        "average_safety_score": round(
            average_score,
            2
        )
    }
    

from datetime import date, timedelta
from sqlalchemy import func


# ==========================
# FUEL ANALYTICS
# ==========================

def get_fuel_statistics(db: Session):

    total_logs = db.query(Fuel).count()

    total_quantity = (
        db.query(
            func.coalesce(
                func.sum(Fuel.fuel_quantity),
                0
            )
        ).scalar()
    )

    total_cost = (
        db.query(
            func.coalesce(
                func.sum(Fuel.fuel_cost),
                0
            )
        ).scalar()
    )

    avg_price = (
        total_cost / total_quantity
        if total_quantity > 0 else 0
    )

    return {
        "total_logs": total_logs,
        "total_quantity": round(total_quantity, 2),
        "total_cost": round(total_cost, 2),
        "average_price_per_unit": round(avg_price, 2)
    }


# ==========================
# MAINTENANCE ANALYTICS
# ==========================

def get_maintenance_statistics(db: Session):

    total_records = db.query(Maintenance).count()

    total_cost = (
        db.query(
            func.coalesce(
                func.sum(Maintenance.cost),
                0
            )
        ).scalar()
    )

    completed = (
        db.query(Maintenance)
        .filter(
            Maintenance.status == "Completed"
        )
        .count()
    )

    scheduled = (
        db.query(Maintenance)
        .filter(
            Maintenance.status == "Scheduled"
        )
        .count()
    )

    return {
        "total_records": total_records,
        "completed": completed,
        "scheduled": scheduled,
        "total_cost": round(total_cost, 2)
    }


# ==========================
# EXPENSE ANALYTICS
# ==========================

def get_expense_statistics(db: Session):

    total_expenses = db.query(Expense).count()

    total_amount = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0
            )
        ).scalar()
    )

    average = (
        total_amount / total_expenses
        if total_expenses else 0
    )

    return {
        "total_expenses": total_expenses,
        "total_amount": round(total_amount, 2),
        "average_expense": round(average, 2)
    }


# ==========================
# ALERTS
# ==========================

def get_dashboard_alerts(db: Session):

    today = date.today()

    upcoming_services = (
        db.query(Maintenance)
        .filter(
            Maintenance.next_service_date <=
            today + timedelta(days=30)
        )
        .count()
    )

    expired_licenses = (
        db.query(Driver)
        .filter(
            Driver.license_expiry_date <= today
        )
        .count()
    )

    active_trips = (
        db.query(Trip)
        .filter(
            Trip.status == "In Progress"
        )
        .count()
    )

    return {
        "upcoming_services": upcoming_services,
        "expired_driver_licenses": expired_licenses,
        "active_trips": active_trips
    }
    
# ==========================================
# REPORTS API
# ==========================================

from datetime import datetime, timedelta
from sqlalchemy import func


# -----------------------------
# Daily Report
# -----------------------------
def get_daily_report(db: Session):

    today = datetime.now().date()

    trips = db.query(Trip).filter(
        func.date(Trip.start_time) == today
    ).count()

    fuel_cost = db.query(
        func.coalesce(func.sum(Fuel.fuel_cost), 0)
    ).filter(
        Fuel.date == today
    ).scalar()

    expenses = db.query(
        func.coalesce(func.sum(Expense.amount), 0)
    ).filter(
        Expense.expense_date == today
    ).scalar()

    maintenance = db.query(
        func.coalesce(func.sum(Maintenance.cost), 0)
    ).filter(
        Maintenance.service_date == today
    ).scalar()

    return {
        "date": str(today),
        "trips": trips,
        "fuel_cost": round(fuel_cost,2),
        "maintenance_cost": round(maintenance,2),
        "expenses": round(expenses,2),
        "total_cost": round(
            fuel_cost +
            maintenance +
            expenses,
            2
        )
    }


# -----------------------------
# Weekly Report
# -----------------------------
def get_weekly_report(db: Session):

    today = datetime.now().date()
    week = today - timedelta(days=7)

    trips = db.query(Trip).filter(
        Trip.start_time >= week
    ).count()

    fuel = db.query(
        func.coalesce(func.sum(Fuel.fuel_cost),0)
    ).filter(
        Fuel.date >= week
    ).scalar()

    maintenance = db.query(
        func.coalesce(func.sum(Maintenance.cost),0)
    ).filter(
        Maintenance.service_date >= week
    ).scalar()

    expenses = db.query(
        func.coalesce(func.sum(Expense.amount),0)
    ).filter(
        Expense.expense_date >= week
    ).scalar()

    return {
        "period":"Last 7 Days",
        "trips":trips,
        "fuel_cost":round(fuel,2),
        "maintenance_cost":round(maintenance,2),
        "expenses":round(expenses,2),
        "total_cost":round(
            fuel +
            maintenance +
            expenses,
            2
        )
    }


# -----------------------------
# Monthly Report
# -----------------------------
def get_monthly_report(db: Session):

    month = datetime.now().month
    year = datetime.now().year

    trips = db.query(Trip).filter(
        func.extract("month",Trip.start_time)==month,
        func.extract("year",Trip.start_time)==year
    ).count()

    fuel = db.query(
        func.coalesce(func.sum(Fuel.fuel_cost),0)
    ).filter(
        func.extract("month",Fuel.date)==month,
        func.extract("year",Fuel.date)==year
    ).scalar()

    maintenance = db.query(
        func.coalesce(func.sum(Maintenance.cost),0)
    ).filter(
        func.extract("month",Maintenance.service_date)==month,
        func.extract("year",Maintenance.service_date)==year
    ).scalar()

    expenses = db.query(
        func.coalesce(func.sum(Expense.amount),0)
    ).filter(
        func.extract("month",Expense.expense_date)==month,
        func.extract("year",Expense.expense_date)==year
    ).scalar()

    return {
        "month":month,
        "year":year,
        "trips":trips,
        "fuel_cost":round(fuel,2),
        "maintenance_cost":round(maintenance,2),
        "expenses":round(expenses,2),
        "total_cost":round(
            fuel +
            maintenance +
            expenses,
            2
        )
    }


# -----------------------------
# Fleet Report
# -----------------------------
def get_fleet_report(db: Session):

    vehicles = db.query(Vehicle).all()

    report=[]

    for vehicle in vehicles:

        report.append({

            "vehicle_id":vehicle.id,
            "registration":vehicle.registration_number,
            "name":vehicle.vehicle_name,
            "type":vehicle.vehicle_type,
            "status":vehicle.status,
            "odometer":vehicle.odometer

        })

    return report


# -----------------------------
# Driver Report
# -----------------------------
def get_driver_report(db: Session):

    drivers=db.query(Driver).all()

    report=[]

    for driver in drivers:

        report.append({

            "driver_id":driver.id,
            "name":driver.name,
            "license":driver.license_number,
            "category":driver.license_category,
            "status":driver.status,
            "safety_score":driver.safety_score

        })

    return report


# -----------------------------
# Vehicle Report
# -----------------------------
def get_vehicle_report(db: Session):

    vehicles=db.query(Vehicle).all()

    report=[]

    for vehicle in vehicles:

        trip_count=db.query(Trip).filter(
            Trip.vehicle_id==vehicle.id
        ).count()

        fuel_cost=db.query(
            func.coalesce(
                func.sum(Fuel.fuel_cost),
                0
            )
        ).filter(
            Fuel.vehicle_id==vehicle.id
        ).scalar()

        maintenance_cost=db.query(
            func.coalesce(
                func.sum(Maintenance.cost),
                0
            )
        ).filter(
            Maintenance.vehicle_id==vehicle.id
        ).scalar()

        report.append({

            "vehicle_id":vehicle.id,
            "registration":vehicle.registration_number,
            "vehicle":vehicle.vehicle_name,
            "trip_count":trip_count,
            "fuel_cost":round(fuel_cost,2),
            "maintenance_cost":round(maintenance_cost,2),
            "status":vehicle.status

        })

    return report

# ==========================================
# CSV EXPORT
# ==========================================

def export_csv(db: Session):

    os.makedirs("exports", exist_ok=True)

    filepath = os.path.join(
        "exports",
        "transit_report.csv"
    )

    vehicles = db.query(Vehicle).all()

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Vehicle ID",
            "Registration",
            "Vehicle Name",
            "Type",
            "Status",
            "Odometer"
        ])

        for vehicle in vehicles:

            writer.writerow([

                vehicle.id,
                vehicle.registration_number,
                vehicle.vehicle_name,
                vehicle.vehicle_type,
                vehicle.status,
                vehicle.odometer

            ])

    return filepath

# ==========================================
# PDF EXPORT
# ==========================================

def export_pdf(db: Session):

    os.makedirs("exports", exist_ok=True)

    filepath = os.path.join(
        "exports",
        "transit_report.pdf"
    )

    pdf = SimpleDocTemplate(filepath)

    data = [[

        "ID",
        "Vehicle",
        "Registration",
        "Status"

    ]]

    vehicles = db.query(Vehicle).all()

    for vehicle in vehicles:

        data.append([

            vehicle.id,
            vehicle.vehicle_name,
            vehicle.registration_number,
            vehicle.status

        ])

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("BOTTOMPADDING", (0,0), (-1,0), 8)

    ]))

    pdf.build([table])

    return filepath