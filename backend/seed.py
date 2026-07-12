from datetime import date, timedelta
from random import choice, randint, uniform

from database import SessionLocal

from models.vehicle import Vehicle
from models.driver import Driver
from models.trip import Trip
from models.maintenance import Maintenance
from models.fuel import Fuel
from models.expense import Expense


db = SessionLocal()


# ----------------------------
# Clear Existing Data
# ----------------------------

db.query(Expense).delete()
db.query(Fuel).delete()
db.query(Maintenance).delete()
db.query(Trip).delete()
db.query(Driver).delete()
db.query(Vehicle).delete()

db.commit()


# ----------------------------
# Vehicles
# ----------------------------

vehicle_status = [
    "Available",
    "In Use",
    "Maintenance"
]

vehicle_types = [
    "Truck",
    "Van",
    "Mini Truck",
    "Bus"
]

vehicles = []

for i in range(1, 21):

    vehicle = Vehicle(
        registration_number=f"CG04AB{i:04}",
        vehicle_name=f"Fleet Vehicle {i}",
        vehicle_type=choice(vehicle_types),
        max_load_capacity=randint(2, 20),
        odometer=randint(10000, 150000),
        acquisition_cost=randint(600000, 2500000),
        status=choice(vehicle_status)
    )

    db.add(vehicle)
    vehicles.append(vehicle)

db.commit()


# ----------------------------
# Drivers
# ----------------------------

driver_status = [
    "Available",
    "Assigned"
]

license_categories = [
    "LMV",
    "HMV",
    "Transport"
]

drivers = []

for i in range(1, 26):

    driver = Driver(
        name=f"Driver {i}",
        license_number=f"DL2026{i:05}",
        license_category=choice(license_categories),
        license_expiry_date=date.today() + timedelta(days=randint(100, 1000)),
        contact_number=f"98765{randint(10000,99999)}",
        safety_score=round(uniform(70, 99), 2),
        status=choice(driver_status)
    )

    db.add(driver)
    drivers.append(driver)

db.commit()

print("Vehicles Added :", db.query(Vehicle).count())
print("Drivers Added  :", db.query(Driver).count())

from datetime import datetime

# ----------------------------
# Trips
# ----------------------------

cities = [
    "Raipur",
    "Bilaspur",
    "Durg",
    "Nagpur",
    "Bhopal",
    "Ranchi",
    "Hyderabad",
    "Visakhapatnam"
]

trip_status = [
    "Completed",
    "Completed",
    "Completed",
    "In Progress",
    "Scheduled"
]

vehicle_ids = [v.id for v in db.query(Vehicle).all()]
driver_ids = [d.id for d in db.query(Driver).all()]

for _ in range(60):

    start = datetime.now() - timedelta(days=randint(1, 90))

    end = start + timedelta(hours=randint(4, 20))

    trip = Trip(
        vehicle_id=choice(vehicle_ids),
        driver_id=choice(driver_ids),
        source=choice(cities),
        destination=choice(cities),
        start_time=start,
        end_time=end,
        distance_km=round(uniform(80, 1200), 2),
        cargo_weight=round(uniform(0.5, 18), 2),
        status=choice(trip_status)
    )

    db.add(trip)

db.commit()

print("Trips Added :", db.query(Trip).count())


# ----------------------------
# Maintenance
# ----------------------------

service_types = [
    "Oil Change",
    "Brake Service",
    "Tyre Rotation",
    "Battery Check",
    "Engine Service"
]

maintenance_status = [
    "Completed",
    "Scheduled"
]

vendors = [
    "Tata Service",
    "Ashok Leyland",
    "Mahindra Workshop",
    "Local Garage"
]

for _ in range(40):

    service_date = date.today() - timedelta(days=randint(1, 180))

    next_service = service_date + timedelta(days=90)

    record = Maintenance(
        vehicle_id=choice(vehicle_ids),
        service_type=choice(service_types),
        service_date=service_date,
        next_service_date=next_service,
        vendor=choice(vendors),
        cost=round(uniform(2000, 30000), 2),
        notes="Routine maintenance",
        status=choice(maintenance_status)
    )

    db.add(record)

db.commit()

print("Maintenance Added :", db.query(Maintenance).count())


# ----------------------------
# Fuel Logs
# ----------------------------

stations = [
    "Indian Oil",
    "HP",
    "BPCL",
    "Reliance"
]

for _ in range(80):

    fuel = Fuel(
        vehicle_id=choice(vehicle_ids),
        date=date.today() - timedelta(days=randint(1, 180)),
        fuel_quantity=round(uniform(20, 120), 2),
        fuel_cost=round(uniform(2000, 12000), 2),
        odometer=round(uniform(10000, 200000), 2),
        fuel_station=choice(stations),
        remarks="Auto generated"
    )

    db.add(fuel)

db.commit()

print("Fuel Logs Added :", db.query(Fuel).count())


# ----------------------------
# Expenses
# ----------------------------

expense_types = [
    "Insurance",
    "Tyre",
    "Permit",
    "Parking",
    "Repair",
    "Cleaning"
]

for _ in range(50):

    expense = Expense(
        vehicle_id=choice(vehicle_ids),
        expense_type=choice(expense_types),
        amount=round(uniform(500, 30000), 2),
        expense_date=date.today() - timedelta(days=randint(1, 180)),
        vendor="Vendor " + str(randint(1, 15)),
        notes="Auto generated"
    )

    db.add(expense)

db.commit()

print("Expenses Added :", db.query(Expense).count())


print("\n===================================")
print("TransitOps Database Ready")
print("===================================")
print("Vehicles     :", db.query(Vehicle).count())
print("Drivers      :", db.query(Driver).count())
print("Trips        :", db.query(Trip).count())
print("Maintenance  :", db.query(Maintenance).count())
print("Fuel Logs    :", db.query(Fuel).count())
print("Expenses     :", db.query(Expense).count())
print("===================================")
