/* ==========================================================
   TransitOps Maintenance Management
========================================================== */

let maintenanceChart = null;
let allMaintenance = [];

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
   Load Maintenance
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadMaintenance();

});

async function loadMaintenance(){

    showLoader();

    try{

        const records = await API.getMaintenance();

        if(!records){

            hideLoader();

            return;

        }

        allMaintenance = records;

        updateCards(records);

        populateTable(records);

        drawChart(records);

        showToast("Maintenance Records Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   KPI Cards
========================================================== */

function updateCards(records){

    const total = records.length;

    const completed = records.filter(r=>

        (r.status || "").toLowerCase() === "completed"

    ).length;

    const scheduled = records.filter(r=>

        (r.status || "").toLowerCase() === "scheduled"

    ).length;

    let totalCost = 0;

    records.forEach(record=>{

        totalCost += Number(record.cost || 0);

    });

    $("totalMaintenance").innerHTML = total;

    $("completedMaintenance").innerHTML = completed;

    $("scheduledMaintenance").innerHTML = scheduled;

    $("maintenanceCost").innerHTML = formatCurrency(totalCost);

    $("summaryMaintenance").innerHTML = total;

    $("summaryCompleted").innerHTML = completed;

    $("summaryScheduled").innerHTML = scheduled;

    $("summaryMaintenanceCost").innerHTML =
        formatCurrency(totalCost);

}
/* ==========================================================
   Maintenance Table
========================================================== */

function populateTable(records){

    const table = $("maintenanceTable");

    if(!table) return;

    table.innerHTML = "";

    if(records.length===0){

        table.innerHTML = `

        <tr>

            <td colspan="9"
                style="text-align:center;padding:30px;">

                No Maintenance Records Found

            </td>

        </tr>

        `;

        return;

    }

    records.forEach(record=>{

        let badge = "badge-success";

        const status = (record.status || "").toLowerCase();

        if(status==="scheduled")
            badge="badge-warning";

        else if(status==="completed")
            badge="badge-success";

        table.innerHTML += `

        <tr>

            <td>${record.id}</td>

            <td>VH-${record.vehicle_id}</td>

            <td>${record.service_type}</td>

            <td>${formatDate(record.service_date)}</td>

            <td>${formatDate(record.next_service_date)}</td>

            <td>${record.vendor}</td>

            <td>${formatCurrency(record.cost)}</td>

            <td>

                <span class="badge ${badge}">

                    ${record.status}

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

const search = $("searchMaintenance");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allMaintenance.filter(record=>{

            return JSON.stringify(record)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}

/* ==========================================================
   Refresh
========================================================== */

function refreshMaintenance(){

    loadMaintenance();

}
/* ==========================================================
   Maintenance Status Chart
========================================================== */

function drawChart(records){

    const ctx = $("maintenanceChart");

    if(!ctx) return;

    if(maintenanceChart){

        maintenanceChart.destroy();

    }

    const completed = records.filter(r=>

        (r.status || "").toLowerCase() === "completed"

    ).length;

    const scheduled = records.filter(r=>

        (r.status || "").toLowerCase() === "scheduled"

    ).length;

    maintenanceChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Completed",
                "Scheduled"
            ],

            datasets:[{

                data:[
                    completed,
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
   Utility Functions
========================================================== */

function formatNumber(value){

    if(value===null || value===undefined)

        return "-";

    return Number(value).toFixed(2);

}

/* ==========================================================
   Export Placeholders
========================================================== */

function exportMaintenanceCSV(){

    showToast("Maintenance CSV Export Coming Soon");

}

function exportMaintenancePDF(){

    showToast("Maintenance PDF Export Coming Soon");

}

/* ==========================================================
   Ready
========================================================== */

console.log("TransitOps Maintenance Module Loaded Successfully");