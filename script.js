var serialno=2;
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
    $("#submit-btn").click(() => {
    var bardata=$("#barcode-data").val();
    var itemname = $("#item-name").val();
    var priceinput = $("#price-input").val();
    if(bardata===""&&itemname===""&&priceinput===""){
        alert("Enter details please");
    }
    serialno+=1;
    if(itemname===""&&priceinput===""){
        if(isBarcodeExist(bardata)){
            console.log(barcode[bardata]);
            createtable(barcode[bardata][0],barcode[bardata][1]);
            $("#barcode-data").val("");
        }
        else{
            alert("Enter correct value");
            $("#barcode-data").val("");
        }
    }
    if(bardata===''){
        console.log("done");
        createtable(itemname, priceinput);
        $("#item-name").val("");
        $("#price-input").val("");
    }
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
    priceofproduct.text(`Rs.${price}`);
    buttonEl.text("delete");
    buttonEl.attr("onclick",`deletion(${serialno})`);
    
    forbutton.append(buttonEl);
    trthat.append(nameofproduct,priceofproduct,forbutton);
    ourtable.append(trthat);
};
function deletion(value){
    iddelete="data"+value;
    $(`#${iddelete}`).remove();
}