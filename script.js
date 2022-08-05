var serialno = 0;
var totalPrice = 0;
var totalQuantity = 0;

$(document).ready(() => {
    $("#barcode-data").focus();
    $("#submit-btn").click(() => {
        var bardata = $("#barcode-data").val();
        var itemname = $("#item-name").val();
        var priceinput = $("#price-input").val();
        var quaninput = $("#quant-input").val();
        if (bardata && !itemname && !priceinput) {
            whenwe(bardata, quaninput);
        };
        if (!bardata) {
            var itemname = $("#item-name").val();
            var priceinput = $("#price-input").val();
            var quaninput = $("#quant-input").val();
            if (!quaninput) {
                createtable(itemname, priceinput, 20, 1);
            } else {
                createtable(itemname, priceinput, 20, quaninput);
            }
            $("#item-name").val("");
            $("#price-input").val("");
            $("#quant-input").val("");
        }
    });
});

function bar_update(val, price, weight, quantity = 1) {
    if (!quantity) {
        createtable(val, price, weight, 1);
        $("#barcode-data").val("");
        $("#quant-input").val("");
    } else if (quantity) {
        createtable(val, price, weight, quantity);
        $("#barcode-data").val("");
        $("#quant-input").val("");
    }
}

function whenwe(barcode, quantity = 1) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "https://cors-anywhere.herokuapp.com/https://www.modstore.in/catalogsearch/result/?q=" + barcode, true);
    xhr.responseType = "document";

    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = xhr.responseXML.querySelectorAll('div.product-item-details h2');
            var responsep = xhr.responseXML.querySelectorAll('span.regular-price span');
            try {
                namep = response[0].textContent;
                price = responsep[0].textContent;
                itemnamep = namep.split(" ");
                console.log(itemnamep)
                console.log(namep, price);
                grams = itemnamep[itemnamep.length - 1];
                itemnamep.pop()
                namep = itemnamep.join(" ");
                bar_update(namep, price, grams, quantity);
            } catch (err) {
                alert("adhi ledu amma");
                console.log(err);
            }

        }
    };

    xhr.onerror = function () {

        console.error("Mujhe athi nehi aur kisiko jathi nehi");
        console.error(xhr.status, xhr.statusText);
    }
    xhr.send();

}

function createtable(item_name, price, weight, quaninput) {
    var ourtable = $("#table");
    var trthat = $('<tr>');
    var nameofproduct = $('<td>');
    var priceofproduct = $('<td>');
    var weightOfProduct = $('<td>');
    var quantityOfProduct = $('<td>');
    var forbutton = $('<td>');
    var buttonEl = $('<button>');

    trthat.attr("id", "data" + serialno);

    nameofproduct.text(item_name);
    nameofproduct.attr('id', 'name');
    priceofproduct.text(`${price}`);
    priceofproduct.attr('id', 'price');
    weightOfProduct.text(`${weight}`);
    weightOfProduct.attr('id', 'weight');
    quantityOfProduct.text(`${quaninput}`);
    quantityOfProduct.attr('id', 'quantity');

    buttonEl.text("delete");
    buttonEl.attr("onclick", `deletion(${serialno})`);

    forbutton.append(buttonEl);
    trthat.append(nameofproduct, priceofproduct, weightOfProduct, quantityOfProduct, forbutton);
    ourtable.append(trthat);

    serialno += 1;
    quanprice = 0;
    console.log();

    totalQuantity += parseInt(quaninput);
    quanprice = parseInt(quaninput) * parseInt(price);
    
    if(!quanprice){
        quanprice = parseInt(quaninput) * parseInt(price.replace("Rs", ""));
    }
    totalPrice += parseInt(quanprice);

    updateBill(totalQuantity, totalPrice);
};

function deletion(value) {
    x = 0;

    iddelete = "data" + value;
    deletethis = $(`#${iddelete}`);

    rq = $(`#${iddelete}> #quantity`).text().replace('gm', "");
    totalQuantity -= rq;

    console.log($(`#${iddelete} > #price`).text());
    rp = $(`#${iddelete} > #price`).text().replace("Rs", "");
    console.log(rp);
    totalPrice -= rp * rq;
    updateBill(totalQuantity, totalPrice);
    deletethis.remove();
}

function updateBill(quantity, price) {
    $("#barcode-data").focus();
    $("#span1").text(quantity);
    $("#span2").text(`Rs.${price}/-`);
}