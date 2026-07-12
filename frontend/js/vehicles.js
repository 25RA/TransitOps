/* ==========================================================
   TransitOps Vehicles
========================================================== */

let vehicleChart = null;
let allVehicles = [];

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

    const loader = $("loader");

    if(loader)
        loader.style.display="none";

}

function showToast(msg){

    const toast = $("toast");

    if(!toast) return;

    toast.innerHTML = msg;

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },2500);

}

/* ==========================================================
   Load Vehicles
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadVehicles();

});

async function loadVehicles(){

    showLoader();

    try{

        const vehicles = await API.getVehicles();

        if(!vehicles){

            hideLoader();

            return;

        }

        allVehicles = vehicles;

        populateTable(vehicles);

        updateCards(vehicles);

        drawChart(vehicles);

        showToast("Vehicles Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   Cards
========================================================== */

function updateCards(vehicles){

    const total = vehicles.length;

    const available =
        vehicles.filter(v=>

            (v.status || "").toLowerCase()=="available"

        ).length;

    const running =
        vehicles.filter(v=>

            (v.status || "").toLowerCase()=="in_use" ||

            (v.status || "").toLowerCase()=="running"

        ).length;

    const maintenance =
        vehicles.filter(v=>

            (v.status || "").toLowerCase()=="maintenance"

        ).length;

    $("totalVehicles").innerHTML=total;

    $("availableVehicles").innerHTML=available;

    $("inUseVehicles").innerHTML=running;

    $("maintenanceVehicles").innerHTML=maintenance;

    $("fleetTotal").innerHTML=total;

    $("fleetAvailable").innerHTML=available;

    $("fleetRunning").innerHTML=running;

    $("fleetMaintenance").innerHTML=maintenance;

}

/* ==========================================================
   Table
========================================================== */

function populateTable(data){

    const table = $("vehicleTable");

    table.innerHTML="";

    if(data.length===0){

        table.innerHTML=`
        <tr>
            <td colspan="8">
                No Vehicles Found
            </td>
        </tr>
        `;

        return;

    }

    data.forEach(vehicle=>{

        table.innerHTML += `

        <tr>

            <td>${vehicle.id}</td>

            <td>${vehicle.vehicle_number || vehicle.registration_number || "-"}</td>

            <td>${vehicle.model || "-"}</td>

            <td>${vehicle.vehicle_type || vehicle.type || "-"}</td>

            <td>${vehicle.capacity || "-"}</td>

            <td>

                <span class="badge badge-success">

                    ${vehicle.status}

                </span>

            </td>

            <td>

                ${vehicle.driver_name || "-"}

            </td>

            <td>

                <button class="btn btn-primary">

                    View

                </button>

            </td>

        </tr>

        `;

    });

}

/* ==========================================================
   Search
========================================================== */

const search = $("searchVehicle");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allVehicles.filter(v=>{

            return JSON.stringify(v)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}

/* ==========================================================
   Chart
========================================================== */

function drawChart(vehicles){

    const ctx = $("vehicleChart");

    if(!ctx) return;

    if(vehicleChart)
        vehicleChart.destroy();

    const available =
        vehicles.filter(v=>(v.status || "").toLowerCase()=="available").length;

    const running =
        vehicles.filter(v=>

            (v.status || "").toLowerCase()=="in_use" ||

            (v.status || "").toLowerCase()=="running"

        ).length;

    const maintenance =
        vehicles.filter(v=>

            (v.status || "").toLowerCase()=="maintenance"

        ).length;

    vehicleChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[

                "Available",

                "Running",

                "Maintenance"

            ],

            datasets:[{

                data:[

                    available,

                    running,

                    maintenance

                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:true,
            aspectRatio:2.5,

            plugins:{

                legend:{

                    position:"bottom"

                }

            }

        }

    });

}