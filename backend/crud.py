from sqlalchemy.orm import Session

from models.vehicle import Vehicle
from schemas.vehicle import VehicleCreate, VehicleUpdate


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