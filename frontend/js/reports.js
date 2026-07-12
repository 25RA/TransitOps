/* ==========================================================
   TransitOps Reports Module
========================================================== */

let reportChart = null;
let reportData = null;

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

/* ==========================================================
   Load Daily Report
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadReports();

});

async function loadReports(){

    showLoader();

    try{

        reportData = await API.getDailyReport();

        updateCards(reportData);

        drawChart(reportData);

        showToast("Daily Report Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   Dashboard Cards
========================================================== */

function updateCards(report){

    $("todayTrips").innerHTML =
        report.trips;

    $("todayFuel").innerHTML =
        formatCurrency(report.fuel_cost);

    $("todayMaintenance").innerHTML =
        formatCurrency(report.maintenance_cost);

    $("todayTotal").innerHTML =
        formatCurrency(report.total_cost);

    $("reportDate").innerHTML =
        report.date;

    $("reportTrips").innerHTML =
        report.trips;

    $("reportExpenses").innerHTML =
        formatCurrency(report.expenses);

    $("reportTotal").innerHTML =
        formatCurrency(report.total_cost);

}
/* ==========================================================
   Cost Breakdown Chart
========================================================== */

function drawChart(report){

    const ctx = $("reportChart");

    if(!ctx) return;

    if(reportChart){

        reportChart.destroy();

    }

    reportChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:[
                "Fuel",
                "Maintenance",
                "Expenses"
            ],

            datasets:[{

                data:[
                    report.fuel_cost,
                    report.maintenance_cost,
                    report.expenses
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
   Report Loaders
========================================================== */

async function loadDailyReport(){

    try{

        const report = await API.getDailyReport();

        updateCards(report);

        drawChart(report);

        showToast("Daily Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}

async function loadWeeklyReport(){

    try{

        const report = await API.getWeeklyReport();

        console.log(report);

        showToast("Weekly Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}

async function loadMonthlyReport(){

    try{

        const report = await API.getMonthlyReport();

        console.log(report);

        showToast("Monthly Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}

async function loadFleetReport(){

    try{

        const report = await API.getFleetReport();

        console.log(report);

        showToast("Fleet Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}

async function loadDriverReport(){

    try{

        const report = await API.getDriverReport();

        console.log(report);

        showToast("Driver Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}

async function loadVehicleReport(){

    try{

        const report = await API.getVehicleReport();

        console.log(report);

        showToast("Vehicle Report Loaded");

    }

    catch(error){

        console.error(error);

    }

}
/* ==========================================================
   Export Functions
========================================================== */

function exportCSV(){

    showToast("CSV Export Coming Soon");

}

function exportPDF(){

    showToast("PDF Export Coming Soon");

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
   Refresh Reports
========================================================== */

function refreshReports(){

    loadReports();

}

/* ==========================================================
   Page Ready
========================================================== */

console.log("TransitOps Reports Module Loaded Successfully");