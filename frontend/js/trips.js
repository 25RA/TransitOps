/* ==========================================================
   TransitOps Trips
========================================================== */

let tripChart = null;
let allTrips = [];

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

function showToast(message){

    const toast = $("toast");

    if(!toast) return;

    toast.innerHTML = message;

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },2500);

}

/* ==========================================================
   Date Formatting
========================================================== */

function formatDate(dateString){

    if(!dateString) return "-";

    const date = new Date(dateString);

    return date.toLocaleString();

}

/* ==========================================================
   Load Trips
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadTrips();

});

async function loadTrips(){

    showLoader();

    try{

        const trips = await API.getTrips();

        if(!trips){

            hideLoader();

            return;

        }

        allTrips = trips;

        updateCards(trips);

        populateTable(trips);

        drawChart(trips);

        showToast("Trips Loaded Successfully");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   Dashboard Cards
========================================================== */

function updateCards(trips){

    const total = trips.length;

    const completed = trips.filter(t=>

        (t.status || "").toLowerCase()=="completed"

    ).length;

    const progress = trips.filter(t=>

        (t.status || "").toLowerCase()=="in progress"

    ).length;

    const scheduled = trips.filter(t=>

        (t.status || "").toLowerCase()=="scheduled"

    ).length;

    if($("totalTrips"))
        $("totalTrips").innerHTML = total;

    if($("completedTrips"))
        $("completedTrips").innerHTML = completed;

    if($("activeTrips"))
        $("activeTrips").innerHTML = progress;

    if($("scheduledTrips"))
        $("scheduledTrips").innerHTML = scheduled;

    if($("summaryTotalTrips"))
        $("summaryTotalTrips").innerHTML = total;

    if($("summaryCompletedTrips"))
        $("summaryCompletedTrips").innerHTML = completed;

    if($("summaryActiveTrips"))
        $("summaryActiveTrips").innerHTML = progress;

    if($("summaryScheduledTrips"))
        $("summaryScheduledTrips").innerHTML = scheduled;

}
/* ==========================================================
   Populate Trips Table
========================================================== */

function populateTable(trips){

    const table = $("tripTable");

    if(!table) return;

    table.innerHTML = "";

    if(trips.length===0){

        table.innerHTML = `
        <tr>
            <td colspan="9" style="text-align:center;padding:30px;">
                No Trips Found
            </td>
        </tr>
        `;

        return;

    }

    trips.forEach(trip=>{

        let badge = "badge-success";

        const status = (trip.status || "").toLowerCase();

        if(status==="scheduled")
            badge="badge-warning";

        else if(status==="in progress")
            badge="badge-primary";

        else if(status==="completed")
            badge="badge-success";

        table.innerHTML += `

        <tr>

            <td>${trip.id}</td>

            <td>VH-${trip.vehicle_id}</td>

            <td>DR-${trip.driver_id}</td>

            <td>${trip.source}</td>

            <td>${trip.destination}</td>

            <td>${trip.distance_km} km</td>

            <td>${trip.cargo_weight} Ton</td>

            <td>

                <span class="badge ${badge}">

                    ${trip.status}

                </span>

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

const search = $("searchTrip");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allTrips.filter(trip=>{

            return JSON.stringify(trip)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}


/* ==========================================================
   Refresh
========================================================== */

function refreshTrips(){

    loadTrips();

}
/* ==========================================================
   Trip Status Chart
========================================================== */

function drawChart(trips){

    const ctx = $("tripChart");

    if(!ctx) return;

    if(tripChart){

        tripChart.destroy();

    }

    const completed = trips.filter(t=>

        (t.status || "").toLowerCase() === "completed"

    ).length;

    const progress = trips.filter(t=>

        (t.status || "").toLowerCase() === "in progress"

    ).length;

    const scheduled = trips.filter(t=>

        (t.status || "").toLowerCase() === "scheduled"

    ).length;

    tripChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Completed",
                "In Progress",
                "Scheduled"
            ],

            datasets:[{

                data:[
                    completed,
                    progress,
                    scheduled
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

/* ==========================================================
   Status Badge Color
========================================================== */

function getStatusClass(status){

    status = (status || "").toLowerCase();

    if(status === "completed")
        return "badge-success";

    if(status === "scheduled")
        return "badge-warning";

    if(status === "in progress")
        return "badge-primary";

    return "badge-secondary";

}

/* ==========================================================
   Utility
========================================================== */

function formatNumber(value){

    if(value === null || value === undefined)
        return "-";

    return Number(value).toFixed(2);

}

/* ==========================================================
   Export Helpers (Future)
========================================================== */

function exportCSV(){

    showToast("CSV Export Coming Soon");

}

function exportPDF(){

    showToast("PDF Export Coming Soon");

}

console.log("TransitOps Trips Loaded Successfully");