from flask import *
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt

app = Flask(__name__)
Bootstrap(app)


app.secret_key = "HelloMyNameIsSiddharth"

# Database credentials
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///available-stock.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# MQTT credentials
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_PASSWORD'] = ''  # Set this item when you need to verify username and password
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
topic = '/flask/mqtt'
mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)

# Database Definition
class Cart(db.Model):
    barcode_number = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Cart {self.barcode_number}>"

with app.app_context():
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
    barcode = StringField(label="Barcode:", render_kw={"autofocus": True})
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
    db_items = db.session.query(Cart).all()
    try:
        try:
            for item in db_items:
                if item.barcode_number == int(request.form["barcode-data"]):
                    for cart_item in items:
                        if cart_item["name"].lower() == item.item_name.lower():
                            item_price = items[items.index(cart_item)]["price"] // items[items.index(cart_item)]["quantity"]
                            items[items.index(cart_item)]["quantity"] += 1
                            items[items.index(cart_item)]["price"] += item_price
                            total_price += item_price
                            total_items += 1
                            return redirect(url_for("home"))
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
    except:
        flash("Invalid Details")
    return redirect(url_for("home"))

# Delete an item 
@app.route("/delete/<int:index>")
def delete_item(index):
    global items, total_price,total_items
    for item in items:
        if item["id"] == index:
            price = item["price"] // item["quantity"]
            total_price -= price
            total_items -= 1
            if item["quantity"] == 1:
                items.remove(item)
            else:
                items[items.index(item)]["quantity"] -= 1
                items[items.index(item)]["price"] -= price
    return redirect(url_for("home"))

# Add into Database interface
@app.route("/add", methods=["GET", "POST"])
def add_into_db():
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
        return redirect(url_for("add_into_db"))
    return render_template("add.html", form=cform)

if __name__ == "__main__":
    app.run(debug=True)