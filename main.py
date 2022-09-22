from flask import *
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)

app.secret_key = "HelloMyNameIsSiddharth"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///available-stock.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Database Definition
class Cart(db.Model):
    barcode_number = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cart {self.barcode_number}>"

db.create_all()

# Items data definition
id = 1
items = [{
    "id" : id,
    "name": "Colgate",
    "quantity": 1,
    "price": 50,
}]
total_price = 50
total_items = 1

class NewItemForm(FlaskForm):
    barcode = StringField(label="Barcode:")
    item_name = StringField(label="Item Name:")
    price = FloatField(label="Price:")
    submit = SubmitField(label="Add Item")

# Home Page Route
@app.route("/")
def home():
    return render_template("index.html", items=items, total_price=total_price, no_of_items=total_items)
    

# Add Items into Cart
@app.route("/name", methods=["POST"])
def add_item():
    # new Item method
    def add_item(id, name, quantity, price):
        return {"id":id, "name":name, "quantity":quantity, "price":price}

    global items, id, total_price, total_items
    id += 1
    quantity = 1
    cart_items = db.session.query(Cart).all()
    try:
        for item in cart_items:
            if item.barcode_number == int(request.form["barcode-data"]):
                new_item = add_item(id, item.item_name, quantity, item.price)
    except:
        if request.form["quantity"]:
            quantity = int(request.form["quantity"])
        new_item = add_item(id, request.form["itemName"].title(), quantity, int(request.form["priceAmt"]) * quantity)
    try:
        items.append(new_item)
        total_price += new_item["price"] 
        total_items += new_item["quantity"]
    except:
        flash("Barcode not found")
    return redirect(url_for("home"))

# Delete an item 
@app.route("/delete/<int:index>")
def delete_item(index):
    global items, total_price,total_items
    for item in items:
        if item["id"] == index:
            items.remove(item)
            total_price -= item["price"] 
            total_items -= item["quantity"]
    return redirect(url_for("home"))

# Add csv interface
@app.route("/add", methods=["GET", "POST"])
def add_into_csv():
    cform = NewItemForm()
    if cform.validate_on_submit():
        new_item = Cart(
            barcode_number = cform.barcode.data,
            item_name = cform.item_name.data,
            price = int(cform.price.data)
        )
        try:
            db.session.add(new_item)
            db.session.commit()
            flash("Item Added to Database")
        except:
            flash("Item already exists")
        return redirect(url_for("add_into_csv"))
    return render_template("add.html", form=cform)

if __name__ == "__main__":
    app.run(host="localhost", port=3000 ,debug=True)
