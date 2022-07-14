
const form = document.getElementById("form");
const itemContainer = document.getElementById("item-container");
const submitBtn = document.getElementById("submit-btn");
const itemEl = document.getElementById("item-name");
const priceEl = document.getElementById("price-input");

// table data
const tableEl = document.getElementById("table");

let itemInput = "";
let priceInput = 0;
let serialNo = 0;

function createItemEl(name, price){
    const tableRow = document.createElement("tr");
    const tableData1 = document.createElement("td");
    const tableData2 = document.createElement("td");
    const tableData3 = document.createElement("td");
    const tableData4 = document.createElement("td");
    const buttonEl = document.createElement("button");

    tableData1.textContent = serialNo;
    tableData2.textContent = name;
    tableData3.textContent = `Rs.${price}`;
    
    buttonEl.textContent = "delete";
    tableData4.appendChild(buttonEl);

    tableRow.append(tableData1, tableData2, tableData3, tableData4);

    // Append to the table tag
    tableEl.appendChild(tableRow);
}

// Getting the form data
function submit_onClick(e){
    itemInput =  form.itemName.value;
    priceInput = form.priceAmt.value;

    if(itemInput==="" || priceInput===""){
        alert("Please fill the input fields.");
        return;
    }

    serialNo += 1;

    createItemEl(itemInput, priceInput)

    console.log(itemInput, priceInput);

    itemEl.value="";
    priceEl.value="";

    e.preventDefault();
}

submitBtn.addEventListener("click",submit_onClick);