from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lol.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    orders = db.relationship("Order", backref="user")

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

@app.route("/")
def index():
    return "AAAA"

@app.route("/orders_by_user", methods=["GET"])
def get_orders_by_user():
    user_name = request.args.get("user")

    if not user_name:
        return "User parameter is missing"

    user = User.query.filter_by(name=user_name).first()

    if not user:
        return "User not found"

    orders = Order.query.filter_by(user=user).all()

    if not orders:
        return "User has no orders"

    orders_data = [order.order_number for order in orders]
    return orders_data


def fill_database():
    users_data = [
        {"name": "lol", "orders": ["lol", "lol"]},
        {"name": "olololol", "orders": ["ololol", "olol", "lolo"]},
        {"name": "olololooll", "orders": ["olololl"]}
    ]

    for user_data in users_data:
        user = User(name=user_data["name"])
        db.session.add(user)
        db.session.commit()

        for order_number in user_data["orders"]:
            order = Order(order_number=order_number, user=user)
            db.session.add(order)
            db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)