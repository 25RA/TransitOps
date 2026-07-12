/* ==========================================================
   TransitOps Fuel Management
========================================================== */

let fuelChart = null;
let allFuelLogs = [];

/* ==========================================================
   Helpers
========================================================== */

function $(id){
    return document.getElementById(id);
}

function showLoader(){

    const loader = $("loader");

    if(loader)
        loader.style.display = "flex";

}

function hideLoader(){

    const loader = $("loader");

    if(loader)
        loader.style.display = "none";

}

function showToast(message){

    const toast = $("toast");

    if(!toast) return;

    toast.innerHTML = message;

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },2500);

}

function formatCurrency(value){

    return "₹" + Number(value).toLocaleString(undefined,{
        maximumFractionDigits:2
    });

}

function formatDate(date){

    if(!date) return "-";

    return new Date(date).toLocaleDateString();

}

/* ==========================================================
   Load Fuel Logs
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadFuel();

});

async function loadFuel(){

    showLoader();

    try{

        const logs = await API.getFuel();

        if(!logs){

            hideLoader();

            return;

        }

        allFuelLogs = logs;

        updateCards(logs);

        populateTable(logs);

        drawChart(logs);

        showToast("Fuel Records Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   Dashboard Cards
========================================================== */

function updateCards(logs){

    const totalLogs = logs.length;

    let totalQuantity = 0;

    let totalCost = 0;

    logs.forEach(log=>{

        totalQuantity += Number(log.fuel_quantity || 0);

        totalCost += Number(log.fuel_cost || 0);

    });

    const avgPrice = totalQuantity===0
        ? 0
        : totalCost/totalQuantity;

    $("totalLogs").innerHTML = totalLogs;

    $("totalQuantity").innerHTML =
        totalQuantity.toFixed(2) + " L";

    $("totalFuelCost").innerHTML =
        formatCurrency(totalCost);

    $("avgFuelPrice").innerHTML =
        "₹" + avgPrice.toFixed(2);

    $("summaryLogs").innerHTML =
        totalLogs;

    $("summaryQuantity").innerHTML =
        totalQuantity.toFixed(2) + " L";

    $("summaryCost").innerHTML =
        formatCurrency(totalCost);

    $("summaryPrice").innerHTML =
        "₹" + avgPrice.toFixed(2);

}
/* ==========================================================
   Fuel Table
========================================================== */

function populateTable(logs){

    const table = $("fuelTable");

    if(!table) return;

    table.innerHTML = "";

    if(logs.length===0){

        table.innerHTML = `

        <tr>

            <td colspan="8"
                style="text-align:center;padding:30px;">

                No Fuel Records Found

            </td>

        </tr>

        `;

        return;

    }

    logs.forEach(log=>{

        const pricePerLiter =
            log.fuel_quantity > 0
            ? (log.fuel_cost/log.fuel_quantity).toFixed(2)
            : "0.00";

        table.innerHTML += `

        <tr>

            <td>${log.id}</td>

            <td>VH-${log.vehicle_id}</td>

            <td>${formatDate(log.date)}</td>

            <td>${Number(log.fuel_quantity).toFixed(2)} L</td>

            <td>₹${pricePerLiter}</td>

            <td>${formatCurrency(log.fuel_cost)}</td>

            <td>${log.fuel_station}</td>

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

const search = $("searchFuel");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allFuelLogs.filter(log=>{

            return JSON.stringify(log)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}

/* ==========================================================
   Refresh
========================================================== */

function refreshFuel(){

    loadFuel();

}
/* ==========================================================
   Fuel Consumption Chart
========================================================== */

function drawChart(logs){

    const ctx = $("fuelChart");

    if(!ctx) return;

    if(fuelChart){

        fuelChart.destroy();

    }

    const stations = {};

    logs.forEach(log=>{

        const station = log.fuel_station || "Unknown";

        stations[station] = (stations[station] || 0)
            + Number(log.fuel_quantity || 0);

    });

    fuelChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:Object.keys(stations),

            datasets:[{

                data:Object.values(stations)

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

/* ==========================================================
   Utilities
========================================================== */

function formatNumber(value){

    if(value===null || value===undefined)

        return "-";

    return Number(value).toFixed(2);

}

function exportFuelCSV(){

    showToast("Fuel CSV Export Coming Soon");

}

function exportFuelPDF(){

    showToast("Fuel PDF Export Coming Soon");

}

/* ==========================================================
   Page Ready
========================================================== */

console.log("TransitOps Fuel Module Loaded Successfully");