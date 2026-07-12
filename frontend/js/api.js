/* ==========================================================
   TransitOps API Service
========================================================== */

const API = (() => {

    const BASE_URL = "http://127.0.0.1:8000";

    async function request(endpoint, options = {}) {

        try {

            const response = await fetch(BASE_URL + endpoint, {
                headers: {
                    "Content-Type": "application/json"
                },
                ...options
            });

            if (!response.ok) {

                throw new Error(
                    `API Error : ${response.status}`
                );

            }

            return await response.json();

        } catch (error) {

            console.error(error);

            showToast(error.message, "error");

            return null;

        }

    }

    /* ===========================
       Health
    =========================== */

    const getHealth = () =>
        request("/health");

    /* ===========================
       Dashboard
    =========================== */

    const getDashboardSummary = () =>
        request("/dashboard/summary");

    const getFleetAnalytics = () =>
        request("/dashboard/fleet");

    const getDriverAnalytics = () =>
        request("/dashboard/drivers");

    const getFuelAnalytics = () =>
        request("/dashboard/fuel");

    const getMaintenanceAnalytics = () =>
        request("/dashboard/maintenance");

    const getExpenseAnalytics = () =>
        request("/dashboard/expenses");

    const getAlerts = () =>
        request("/dashboard/alerts");

    /* ===========================
       Vehicles
    =========================== */

    const getVehicles = () =>
        request("/vehicles/");

    const getVehicle = id =>
        request(`/vehicles/${id}`);

    const addVehicle = data =>
        request("/vehicles/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateVehicle = (id, data) =>
        request(`/vehicles/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteVehicle = id =>
        request(`/vehicles/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Drivers
    =========================== */

    const getDrivers = () =>
        request("/drivers/");

    const getDriver = id =>
        request(`/drivers/${id}`);

    const addDriver = data =>
        request("/drivers/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateDriver = (id, data) =>
        request(`/drivers/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteDriver = id =>
        request(`/drivers/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Trips
    =========================== */

    const getTrips = () =>
        request("/trips/");

    const addTrip = data =>
        request("/trips/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateTrip = (id, data) =>
        request(`/trips/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteTrip = id =>
        request(`/trips/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Maintenance
    =========================== */

    const getMaintenance = () =>
        request("/maintenance/");

    const addMaintenance = data =>
        request("/maintenance/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateMaintenance = (id, data) =>
        request(`/maintenance/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteMaintenance = id =>
        request(`/maintenance/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Fuel
    =========================== */

    const getFuel = () =>
        request("/fuel/");

    const addFuel = data =>
        request("/fuel/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateFuel = (id, data) =>
        request(`/fuel/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteFuel = id =>
        request(`/fuel/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Expenses
    =========================== */

    const getExpenses = () =>
        request("/expenses/");

    const addExpense = data =>
        request("/expenses/", {
            method: "POST",
            body: JSON.stringify(data)
        });

    const updateExpense = (id, data) =>
        request(`/expenses/${id}`, {
            method: "PUT",
            body: JSON.stringify(data)
        });

    const deleteExpense = id =>
        request(`/expenses/${id}`, {
            method: "DELETE"
        });

    /* ===========================
       Reports
    =========================== */

    const getDailyReport = () =>
        request("/reports/daily");

    const getWeeklyReport = () =>
        request("/reports/weekly");

    const getMonthlyReport = () =>
        request("/reports/monthly");

    const getFleetReport = () =>
        request("/reports/fleet");

    const getDriverReport = () =>
        request("/reports/drivers");

    const getVehicleReport = () =>
        request("/reports/vehicles");

    const downloadCSV = () =>
        window.open(BASE_URL + "/reports/export/csv");

    const downloadPDF = () =>
        window.open(BASE_URL + "/reports/export/pdf");

    return {

        getHealth,

        getDashboardSummary,
        getFleetAnalytics,
        getDriverAnalytics,
        getFuelAnalytics,
        getMaintenanceAnalytics,
        getExpenseAnalytics,
        getAlerts,

        getVehicles,
        getVehicle,
        addVehicle,
        updateVehicle,
        deleteVehicle,

        getDrivers,
        getDriver,
        addDriver,
        updateDriver,
        deleteDriver,

        getTrips,
        addTrip,
        updateTrip,
        deleteTrip,

        getMaintenance,
        addMaintenance,
        updateMaintenance,
        deleteMaintenance,

        getFuel,
        addFuel,
        updateFuel,
        deleteFuel,

        getExpenses,
        addExpense,
        updateExpense,
        deleteExpense,

        getDailyReport,
        getWeeklyReport,
        getMonthlyReport,
        getFleetReport,
        getDriverReport,
        getVehicleReport,

        downloadCSV,
        downloadPDF

    };

})();