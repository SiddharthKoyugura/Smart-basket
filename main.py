from flask import *
import pandas
from barcode import Barcode
import random

app = Flask(__name__)
# Implementing csv
data = pandas.read_csv("items.csv")
stock_items = data.to_dict(orient="records")

# Items data definition
id = 1
items = [{
    "id" : id,
    "name": "Colgate",
    "quantity": 1,
    "price": 50,
}]
total_price = 50

# Home Page Route
@app.route("/")
def home():
    return render_template("index.html", items=items, total_price=total_price, no_of_items=len(items))

# Add Items into Cart
@app.route("/name", methods=["POST"])
def add_item():
    # new Item method
    def add_item(id, name, quantity, price):
        return {"id":id, "name":name, "quantity":quantity, "price":price}

    global items, id, total_price
    id += 1
    quantity = 1
    try:
        scrape = Barcode(request.form["barcode-data"])
        name = scrape.find_barcode()
        new_item = add_item(id, name, quantity, random.randint(100, 200))
    
    except:
        if not request.form["barcode-data"]:
            if request.form["quantity"]:
                quantity = int(request.form["quantity"])

            new_item = add_item(id, request.form["itemName"].title(), quantity, int(request.form["priceAmt"]) * quantity)

        else:
            bar_data = request.form["barcode-data"]
            for item in stock_items:
                if bar_data == str(item["BARCODE"]):
                    new_item = add_item(id, item["PRODUCT_NAME"] + " " +item["WEIGHT"], quantity, int(item["PRICE"].split("/")[0]))

    items.append(new_item)
    total_price += new_item["price"] 
    return redirect(url_for("home"))

# Delete an item 
@app.route("/delete/<int:index>")
def delete_item(index):
    global items, total_price
    for item in items:
        if item["id"] == index:
            items.remove(item)
            total_price -= item["price"] 
    return redirect(url_for("home"))

# Add csv interface
@app.route("/add")
def add_into_csv():
    return render_template("add.html")

if __name__ == "__main__":
    app.run(host="localhost", port=3000 ,debug=True)
    