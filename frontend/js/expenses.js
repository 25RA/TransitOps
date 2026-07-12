/* ==========================================================
   TransitOps Expense Management
========================================================== */

let expenseChart = null;
let allExpenses = [];

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
   Load Expenses
========================================================== */

document.addEventListener("DOMContentLoaded",()=>{

    loadExpenses();

});

async function loadExpenses(){

    showLoader();

    try{

        const expenses = await API.getExpenses();

        if(!expenses){

            hideLoader();

            return;

        }

        allExpenses = expenses;

        updateCards(expenses);

        populateTable(expenses);

        drawChart(expenses);

        showToast("Expense Records Loaded");

    }

    catch(error){

        console.error(error);

    }

    hideLoader();

}

/* ==========================================================
   Dashboard Cards
========================================================== */

function updateCards(expenses){

    const total = expenses.length;

    let totalAmount = 0;

    const categories = new Set();

    expenses.forEach(expense=>{

        totalAmount += Number(expense.amount || 0);

        categories.add(expense.expense_type);

    });

    const average = total===0
        ? 0
        : totalAmount/total;

    $("totalExpenses").innerHTML = total;

    $("totalExpenseAmount").innerHTML =
        formatCurrency(totalAmount);

    $("averageExpense").innerHTML =
        formatCurrency(average);

    $("expenseCategories").innerHTML =
        categories.size;

    $("summaryExpenses").innerHTML =
        total;

    $("summaryAmount").innerHTML =
        formatCurrency(totalAmount);

    $("summaryAverage").innerHTML =
        formatCurrency(average);

    $("summaryCategories").innerHTML =
        categories.size;

}
/* ==========================================================
   Expense Table
========================================================== */

function populateTable(expenses){

    const table = $("expenseTable");

    if(!table) return;

    table.innerHTML = "";

    if(expenses.length===0){

        table.innerHTML = `

        <tr>

            <td colspan="8"
                style="text-align:center;padding:30px;">

                No Expense Records Found

            </td>

        </tr>

        `;

        return;

    }

    expenses.forEach(expense=>{

        table.innerHTML += `

        <tr>

            <td>${expense.id}</td>

            <td>${formatDate(expense.expense_date)}</td>

            <td>VH-${expense.vehicle_id}</td>

            <td>${expense.expense_type}</td>

            <td>${formatCurrency(expense.amount)}</td>

            <td>${expense.vendor}</td>

            <td>${expense.notes || "-"}</td>

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

const search = $("searchExpense");

if(search){

    search.addEventListener("keyup",()=>{

        const value = search.value.toLowerCase();

        const filtered = allExpenses.filter(expense=>{

            return JSON.stringify(expense)

                .toLowerCase()

                .includes(value);

        });

        populateTable(filtered);

    });

}

/* ==========================================================
   Refresh
========================================================== */

function refreshExpenses(){

    loadExpenses();

}
/* ==========================================================
   Expense Distribution Chart
========================================================== */

function drawChart(expenses){

    const ctx = $("expenseChart");

    if(!ctx) return;

    if(expenseChart){

        expenseChart.destroy();

    }

    const categories = {};

    expenses.forEach(expense=>{

        const type = expense.expense_type || "Other";

        categories[type] = (categories[type] || 0)
            + Number(expense.amount || 0);

    });

    expenseChart = new Chart(ctx,{

        type:"doughnut",

        data:{

            labels:Object.keys(categories),

            datasets:[{

                data:Object.values(categories)

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

function exportExpensesCSV(){

    showToast("Expense CSV Export Coming Soon");

}

function exportExpensesPDF(){

    showToast("Expense PDF Export Coming Soon");

}

/* ==========================================================
   Ready
========================================================== */

console.log("TransitOps Expense Module Loaded Successfully");