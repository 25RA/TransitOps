/* ==========================================================
   TransitOps Drivers
========================================================== */

let driverChart = null;
let allDrivers = [];

/* ==========================================================
   Helpers
========================================================== */

function $(id){
    return document.getElementById(id);
}

function showLoader(){
    const loader = $("loader");
    if(loader) loader.style.display = "flex";
}

function hideLoader(){
    const loader = $("loader");
    if(loader) loader.style.display = "none";
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
   Load Drivers
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadDrivers();

});

async function loadDrivers(){

    showLoader();

    try{

        const drivers = await API.getDrivers();

        if(!drivers){

            hideLoader();
            return;

        }

        allDrivers = drivers;

        populateTable(drivers);

        updateCards(drivers);

        drawChart(drivers);

        showToast("Drivers Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   KPI Cards
========================================================== */

function updateCards(drivers){

    const total = drivers.length;

    const available = drivers.filter(d=>

        (d.status || "").toLowerCase() === "available"

    ).length;

    const assigned = drivers.filter(d=>

        (d.status || "").toLowerCase() === "assigned"

    ).length;

    let safety = 0;

    drivers.forEach(d=>{

        safety += Number(d.safety_score || 0);

    });

    safety = total ? (safety/total).toFixed(1) : 0;

    $("totalDrivers").innerHTML = total;
    $("availableDrivers").innerHTML = available;
    $("assignedDrivers").innerHTML = assigned;
    $("avgSafety").innerHTML = safety + "%";

    $("summaryTotalDrivers").innerHTML = total;
    $("summaryAvailableDrivers").innerHTML = available;
    $("summaryAssignedDrivers").innerHTML = assigned;
    $("summarySafety").innerHTML = safety + "%";

}

/* ==========================================================
   Driver Table
========================================================== */

function populateTable(drivers){

    const table = $("driverTable");

    table.innerHTML = "";

    if(drivers.length === 0){

        table.innerHTML = `
            <tr>
                <td colspan="8" style="text-align:center;">
                    No Drivers Found
                </td>
            </tr>
        `;

        return;

    }

    drivers.forEach(driver=>{

        table.innerHTML += `

        <tr>

            <td>${driver.id}</td>

            <td>${driver.name || "-"}</td>

            <td>${driver.license_number || "-"}</td>

            <td>${driver.phone || "-"}</td>

            <td>${driver.experience || 0} yrs</td>

            <td>${driver.safety_score || 0}%</td>

            <td>

                <span class="badge badge-success">

                    ${driver.status}

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

const search = $("searchDriver");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allDrivers.filter(driver=>{

            return JSON.stringify(driver)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}

/* ==========================================================
   Driver Chart
========================================================== */

function drawChart(drivers){

    const ctx = $("driverChart");

    if(!ctx) return;

    if(driverChart){

        driverChart.destroy();

    }

    const available = drivers.filter(d=>

        (d.status || "").toLowerCase() === "available"

    ).length;

    const assigned = drivers.filter(d=>

        (d.status || "").toLowerCase() === "assigned"

    ).length;

    const inactive = drivers.filter(d=>

        (d.status || "").toLowerCase() === "inactive"

    ).length;

    driverChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Available",
                "Assigned",
                "Inactive"
            ],

            datasets:[{

                data:[
                    available,
                    assigned,
                    inactive
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