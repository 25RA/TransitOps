/* ==========================================================
   TransitOps Dashboard
========================================================== */

let fleetChart = null;
let fuelChart = null;
let driverChart = null;

/* ==========================================================
   Helpers
========================================================== */

function $(id){
    return document.getElementById(id);
}

function showLoader(){

    const loader = $("loader");

    if(loader)
        loader.style.display="flex";

}

function hideLoader(){

    const loader=$("loader");

    if(loader)
        loader.style.display="none";

}

function updateValue(id,value){

    const el=$(id);

    if(el)
        el.innerHTML=value;

}

function currency(value){

    return "₹"+Number(value).toLocaleString("en-IN",{
        maximumFractionDigits:2
    });

}

function showToast(message,type="success"){

    const toast=$("toast");

    if(!toast) return;

    toast.innerHTML=message;

    toast.style.background=
        type==="error"
        ?"#ef4444"
        :"#111827";

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },3000);

}

/* ==========================================================
   Dashboard Init
========================================================== */

document.addEventListener("DOMContentLoaded",async()=>{

    showLoader();

    try{

        await loadSummary();

        await Promise.all([

            loadFleetChart(),

            loadFuelChart(),

            loadDriverChart(),

            loadAlerts(),

            loadTrips()

        ]);

        showToast("Dashboard Loaded");

    }

    catch(e){

        console.error(e);

        showToast("Unable to load dashboard","error");

    }

    hideLoader();

});

/* ==========================================================
   Summary Cards
========================================================== */

async function loadSummary(){

    const summary=await API.getDashboardSummary();

    if(!summary) return;

    updateValue(
        "vehicleCount",
        summary.total_vehicles
    );

    updateValue(
        "driverCount",
        summary.total_drivers
    );

    updateValue(
        "tripCount",
        summary.active_trips
    );

    updateValue(
        "fuelCost",
        currency(summary.fuel_cost)
    );

    updateValue(
        "maintenanceCost",
        currency(summary.maintenance_cost)
    );

    updateValue(
        "expenseCost",
        currency(summary.expense_cost)
    );

    /* Fleet Health */

    const health=Math.round(

        (summary.available_vehicles/

        summary.total_vehicles)*100

    );

    updateValue(
        "fleetHealth",
        health+"%"
    );

    /* Alerts Card */

    const alerts=await API.getAlerts();

    if(alerts){

        updateValue(
            "alertCount",
            alerts.upcoming_services
        );

    }

}
/* ==========================================================
   Fleet Chart
========================================================== */

async function loadFleetChart(){

    const fleet = await API.getFleetAnalytics();

    if(!fleet) return;

    const ctx = $("fleetChart");

    if(!ctx) return;

    if(fleetChart)
        fleetChart.destroy();

    fleetChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Available",
                "In Use",
                "Maintenance",
                "Inactive"
            ],

            datasets:[{

                data:[
                    fleet.available,
                    fleet.in_use,
                    fleet.maintenance,
                    fleet.inactive
                ],

                backgroundColor:[
                    "#10b981",
                    "#2563eb",
                    "#f59e0b",
                    "#ef4444"
                ],

                borderWidth:2,

                borderColor:"#ffffff"

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{
                    position:"bottom"
                }

            }

        }

    });

}


/* ==========================================================
   Fuel Chart
========================================================== */

async function loadFuelChart(){

    const fuel = await API.getFuelAnalytics();

    if(!fuel) return;

    const ctx = $("fuelChart");

    if(!ctx) return;

    if(fuelChart)
        fuelChart.destroy();

    fuelChart = new Chart(ctx,{

        type:"bar",

        data:{

            labels:[
                "Fuel Logs",
                "Quantity",
                "Total Cost",
                "Avg Price"
            ],

            datasets:[{

                label:"Fuel Statistics",

                data:[

                    fuel.total_logs,

                    fuel.total_quantity,

                    fuel.total_cost,

                    fuel.average_price_per_unit

                ],

                backgroundColor:[

                    "#2563eb",

                    "#10b981",

                    "#f59e0b",

                    "#ef4444"

                ],

                borderRadius:8

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{
                legend:{
                    display:false
                }
            },

            scales:{
                y:{
                    beginAtZero:true
                }
            }

        }

    });

}


/* ==========================================================
   Driver Chart
========================================================== */

async function loadDriverChart(){

    const driver = await API.getDriverAnalytics();

    if(!driver) return;

    const ctx = $("driverChart");

    if(!ctx) return;

    if(driverChart)
        driverChart.destroy();

    driverChart = new Chart(ctx,{

        type:"pie",

        data:{

            labels:[

                "Available",

                "Assigned",

                "Inactive"

            ],

            datasets:[{

                data:[

                    driver.available,

                    driver.assigned,

                    driver.inactive

                ],

                backgroundColor:[

                    "#10b981",

                    "#2563eb",

                    "#ef4444"

                ],

                borderWidth:2,

                borderColor:"#ffffff"

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                title:{

                    display:true,

                    text:"Average Safety Score : "+driver.average_safety_score

                },

                legend:{

                    position:"bottom"

                }

            }

        }

    });

}
/* ==========================================================
   Alerts
========================================================== */

async function loadAlerts(){

    const alerts = await API.getAlerts();

    const container = $("alertsContainer");

    if(!container) return;

    container.innerHTML = "";

    if(!alerts){

        container.innerHTML = `
            <div class="alert-item">
                <span class="badge badge-danger">
                    Unable to load alerts
                </span>
            </div>
        `;

        return;

    }

    const alertData = [

        {
            title:"Upcoming Services",
            value:alerts.upcoming_services,
            color:"warning",
            icon:"fa-screwdriver-wrench"
        },

        {
            title:"Expired Licenses",
            value:alerts.expired_driver_licenses,
            color:"danger",
            icon:"fa-id-card"
        },

        {
            title:"Active Trips",
            value:alerts.active_trips,
            color:"success",
            icon:"fa-route"
        }

    ];

    alertData.forEach(item=>{

        container.innerHTML += `

            <div class="alert-item">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div>

                        <h4>${item.title}</h4>

                        <p style="
                            margin-top:8px;
                            font-size:26px;
                            font-weight:700;
                        ">
                            ${item.value}
                        </p>

                    </div>

                    <i class="fas ${item.icon}"
                       style="
                       font-size:32px;
                       color:#2563eb;
                       "></i>

                </div>

            </div>

        `;

    });

}


/* ==========================================================
   Recent Trips
========================================================== */

async function loadTrips(){

    const trips = await API.getTrips();

    const table = $("tripTable");

    if(!table) return;

    table.innerHTML="";

    if(!trips || trips.length===0){

        table.innerHTML=`
        <tr>
            <td colspan="6"
                style="text-align:center;padding:30px;">
                No Trips Available
            </td>
        </tr>
        `;

        return;

    }

    trips.slice(0,10).forEach(trip=>{

        let badge="badge-success";

        const status=(trip.status || "").toLowerCase();

        if(status.includes("maintenance"))
            badge="badge-danger";

        else if(status.includes("trip"))
            badge="badge-warning";

        table.innerHTML+=`

        <tr>

            <td>#${trip.id}</td>

            <td>${trip.vehicle_id}</td>

            <td>${trip.driver_id}</td>

            <td>${trip.source}</td>

            <td>${trip.destination}</td>

            <td>

                <span class="badge ${badge}">
                    ${trip.status}
                </span>

            </td>

        </tr>

        `;

    });

}


/* ==========================================================
   Auto Refresh
========================================================== */

function startAutoRefresh(){

    setInterval(async()=>{

        await loadSummary();

        await loadFleetChart();

        await loadFuelChart();

        await loadDriverChart();

        await loadAlerts();

    },60000);

}

startAutoRefresh();


/* ==========================================================
   Debug
========================================================== */

window.dashboard={

    loadSummary,

    loadFleetChart,

    loadFuelChart,

    loadDriverChart,

    loadAlerts,

    loadTrips

};

console.log("TransitOps Dashboard Ready");