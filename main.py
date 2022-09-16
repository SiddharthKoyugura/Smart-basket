from flask import *
import pandas
from barcode import Barcode
import random
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
from csv import writer

app = Flask(__name__)
Bootstrap(app)

app.secret_key = "HelloMyNameIsSiddharth"
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

class NewItemForm(FlaskForm):
    barcode = StringField(label="Barcode:")
    item_name = StringField(label="Item Name:")
    price = FloatField(label="Price:")
    submit = SubmitField(label="Add Item")

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
    try:
        items.append(new_item)
        total_price += new_item["price"] 
    except:
        flash("Barcode not found")
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
@app.route("/add", methods=["GET", "POST"])
def add_into_csv():
    cform = NewItemForm()
    if cform.validate_on_submit():
        barcode = cform.barcode.data
        item_name = cform.item_name.data
        price = int(cform.price.data)
        with open("items.csv", "a", newline="") as f_object:
            writer_obj = writer(f_object)
            writer_obj.writerow([barcode, item_name, f"{price}/-"])
            f_object.close()
        flash("Item Added to Database")
        return redirect(url_for("add_into_csv"))

    return render_template("add.html", form=cform)

if __name__ == "__main__":
    app.run(host="localhost", port=3000 ,debug=True)
