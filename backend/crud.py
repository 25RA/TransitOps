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