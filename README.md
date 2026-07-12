# TransitOps

## Overview

TransitOps is a full-stack transport and fleet operations management platform developed to simplify the day-to-day management of commercial transportation systems. The platform centralizes fleet operations by providing a single interface for monitoring vehicles, drivers, trips, fuel usage, maintenance schedules, operational expenses, and analytical reports.

The application combines a responsive web interface with a RESTful backend built using FastAPI, enabling efficient data management and real-time operational visibility. By integrating multiple transport management functions into one platform, TransitOps helps organizations improve operational efficiency, reduce manual work, and make informed business decisions.

---

## Key Features

### Dashboard

The dashboard serves as the operational control center of the platform.

Features include:

- Real-time fleet statistics
- Total registered vehicles
- Driver availability
- Active and completed trips
- Fuel expenditure overview
- Maintenance cost tracking
- Business expense summary
- Fleet health indicator
- Operational alerts
- Fleet overview visualization
- Quick access to operational records

---

### Vehicle Management

The vehicle management module provides centralized control over the entire fleet.

Capabilities include:

- Register and manage fleet vehicles
- Vehicle availability tracking
- Vehicle status monitoring
- Maintenance status tracking
- Vehicle search functionality
- Vehicle utilization overview
- Fleet summary statistics

---

### Driver Management

The driver module maintains complete information about drivers and their operational status.

Features include:

- Driver profile management
- License information
- Safety score monitoring
- Assignment tracking
- Availability management
- Experience records
- Driver directory

---

### Trip Management

The trip management system enables monitoring of transportation operations from scheduling to completion.

Features include:

- Trip scheduling
- Active trip tracking
- Completed trip history
- Vehicle assignment
- Driver assignment
- Route information
- Cargo tracking
- Distance records
- Trip status management

---

### Fuel Management

Fuel management helps monitor one of the largest operational expenses.

Capabilities include:

- Fuel log records
- Quantity monitoring
- Fuel cost tracking
- Fuel station management
- Vehicle-wise fuel history
- Fuel consumption analysis
- Price monitoring

---

### Maintenance Management

The maintenance module ensures vehicles remain operational through preventive servicing.

Features include:

- Maintenance history
- Service scheduling
- Vendor information
- Service cost tracking
- Upcoming maintenance
- Completed maintenance records
- Next service reminders

---

### Expense Management

This module records and categorizes operational expenses across the organization.

Supported records include:

- Repairs
- Parking charges
- Cleaning expenses
- Permits
- Miscellaneous operational costs
- Vendor information
- Expense summaries

---

### Reports and Analytics

The reporting module provides operational insights through summarized business reports.

Available reports include:

- Daily reports
- Weekly reports
- Monthly reports
- Fleet reports
- Driver reports
- Vehicle reports

The reporting interface also provides graphical visualization of operational costs and business metrics.

---

### Settings

The settings page allows administrators to configure the platform.

Available options include:

- Administrator information
- Company information
- Notification preferences
- Security settings
- Backup management
- Appearance settings

---

# System Architecture

```
                Frontend
     HTML | CSS | JavaScript | Chart.js
                    │
                    │ REST API
                    ▼
             FastAPI Backend
                    │
         SQLAlchemy ORM Layer
                    │
                SQLite Database
```

---

# Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript (ES6)
- Chart.js
- Font Awesome

## Backend

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

---

# Project Structure

```
TransitOps
│
├── backend
│   ├── routers
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── drivers.py
│   │   ├── expenses.py
│   │   ├── fuel.py
│   │   ├── maintenance.py
│   │   ├── reports.py
│   │   ├── trips.py
│   │   └── vehicles.py
│   │
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── seed.py
│   ├── utils.py
│   └── requirements.txt
│
├── frontend
│   ├── css
│   │   ├── dashboard.css
│   │   ├── responsive.css
│   │   ├── animations.css
│   │   └── style.css
│   │
│   ├── js
│   │   ├── api.js
│   │   ├── dashboard.js
│   │   ├── drivers.js
│   │   ├── expenses.js
│   │   ├── fuel.js
│   │   ├── maintenance.js
│   │   ├── reports.js
│   │   ├── trips.js
│   │   └── vehicles.js
│   │
│   ├── dashboard.html
│   ├── drivers.html
│   ├── expenses.html
│   ├── fuel.html
│   ├── maintenance.html
│   ├── reports.html
│   ├── settings.html
│   ├── trips.html
│   └── vehicles.html
│
└── README.md
```

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/25RA/TransitOps.git
```

Move into the project directory.

```bash
cd TransitOps
```

---

## Create a Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Run the Backend

Navigate to the backend directory.

```bash
cd backend
```

Start the FastAPI server.

```bash
uvicorn app:app --reload
```

The backend will be available at

```
http://127.0.0.1:8000
```

Swagger API Documentation

```
http://127.0.0.1:8000/docs
```

---

## Run the Frontend

Open the frontend folder using Visual Studio Code and launch the application using Live Server.

Open

```
frontend/dashboard.html
```

---

# API Modules

The backend exposes REST APIs for the following modules.

- Authentication
- Dashboard
- Vehicles
- Drivers
- Trips
- Fuel
- Maintenance
- Expenses
- Reports

The APIs are documented automatically using FastAPI Swagger UI.

---

# Future Improvements

The current architecture has been designed to support future enhancements, including:

- Role-based authentication
- GPS-based live vehicle tracking
- Route optimization
- AI-powered maintenance prediction
- Fuel consumption forecasting
- Driver performance analytics
- Email notifications
- SMS alerts
- PDF and Excel report exports
- Cloud deployment
- Mobile application support
- Multi-organization management
- Live map integration

---

# Design Goals

TransitOps was designed with the following objectives:

- Clean and intuitive user interface
- Responsive layout for different screen sizes
- Modular backend architecture
- RESTful API design
- Easy scalability
- Maintainable codebase
- Separation of frontend and backend
- Real-time operational visibility

---

# License

This project is released under the MIT License.

---

# Author

TransitOps is a full-stack fleet management platform developed using FastAPI, SQLAlchemy, HTML, CSS, and JavaScript to provide an integrated solution for transport operations management.
