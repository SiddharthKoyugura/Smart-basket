
let serialno=2;
let totalPrice = 80;

const itemQuantity = $("#span1");
const itemPrice = $("#span2");

barcode={
    "5555555555":["LAYS",99],
    "6666666666":["SNICKERS",20],
    "7777777777":["CHEETOS",20]
}
function isBarcodeExist(eanvalue){
    const isInArray =barcode.hasOwnProperty(eanvalue);
    return isInArray;
}
$(document).ready(()=>{
    // Submit Event Listener
    $("#submit-btn").click(() => {
    var bardata=$("#barcode-data").val();
    var itemname = $("#item-name").val();
    var priceinput = $("#price-input").val();
    if(bardata===""&&itemname===""&&priceinput===""){
        alert("Enter details please");
        return;
    }
    if(bardata && (itemname || priceinput)){
        alert("Do not enter any other details when barcode entered.");
    }

    else{
        if(bardata===""){
            if(itemname==="" || priceinput==="" || priceinput<1){
                alert("Enter the correct details");
            }else{
                serialno+=1;
                totalPrice += parseInt(priceinput);
                createtable(itemname, priceinput);
            }
        }
        else if(isBarcodeExist(bardata)){
            serialno+=1;
            totalPrice += barcode[bardata][1];
            createtable(barcode[bardata][0], barcode[bardata][1]);
        }else if(!isBarcodeExist(bardata)){
            alert("Item not found");
        }
    }
    $("#item-name").val("");
    $("#price-input").val("");
    $("#barcode-data").val("");
    updateBill(serialno, totalPrice);
    });
});

function createtable(name, price) {
    var ourtable = $("#table");
    var trthat = $('<tr>');
    var nameofproduct = $('<td>');
    var priceofproduct = $('<td>');
    var forbutton = $('<td>');
    var buttonEl = $('<button>');
    
    trthat.attr("id","data"+serialno);
    nameofproduct.text(name);
    priceofproduct.text(`Rs.${price}/-`);
    buttonEl.text("delete");
    buttonEl.attr("onclick",`deletion(${serialno})`);
    
    forbutton.append(buttonEl);
    trthat.append(nameofproduct,priceofproduct,forbutton);
    ourtable.append(trthat);
}

function deletion(value){
    serialno-=1;
    iddelete="data"+value;
    totalPrice -= parseInt($(`#${iddelete} td`).eq(1).html().match(/\d+/)[0]);
    updateBill(serialno, totalPrice);
    $(`#${iddelete}`).remove();
}


function updateBill(quantity, price){
    $("#span1").text(quantity);
    $("#span2").text(`Rs.${price}/-`);
}