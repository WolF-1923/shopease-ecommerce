from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "shopease-demo-key-change-before-production")
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(Path(__file__).with_name("shop.db"))))

PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "price": 1499, "emoji": "🎧", "color": "lavender", "description": "Clear sound for music, classes and calls."},
    {"id": 2, "name": "Smart Watch", "category": "Electronics", "price": 2199, "emoji": "⌚", "color": "peach", "description": "A stylish everyday companion."},
    {"id": 3, "name": "Everyday Backpack", "category": "Accessories", "price": 999, "emoji": "🎒", "color": "mint", "description": "Roomy, lightweight and ready to go."},
    {"id": 4, "name": "Running Shoes", "category": "Fashion", "price": 1799, "emoji": "👟", "color": "blue", "description": "Comfortable steps for busy days."},
    {"id": 5, "name": "Ceramic Coffee Mug", "category": "Home", "price": 349, "emoji": "☕", "color": "peach", "description": "Make your coffee break feel special."},
    {"id": 6, "name": "Desk Lamp", "category": "Home", "price": 799, "emoji": "💡", "color": "lavender", "description": "A warm glow for your study desk."},
    {"id": 7, "name": "Sunglasses", "category": "Fashion", "price": 599, "emoji": "🕶️", "color": "mint", "description": "A simple style upgrade."},
    {"id": 8, "name": "Mini Speaker", "category": "Electronics", "price": 1199, "emoji": "🔊", "color": "blue", "description": "Small speaker, big weekend energy."},
]

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                items TEXT NOT NULL,
                total INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.template_filter("inr")
def inr(value):
    return f"₹{value:,.0f}"

def get_cart():
    cart = session.get("cart", {})
    items = []
    total = 0
    for product in PRODUCTS:
        qty = int(cart.get(str(product["id"]), 0))
        if qty > 0:
            line_total = product["price"] * qty
            items.append({**product, "qty": qty, "line_total": line_total})
            total += line_total
    return items, total

@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    filtered = PRODUCTS
    if category != "All":
        filtered = [p for p in filtered if p["category"] == category]
    if query:
        filtered = [p for p in filtered if query.lower() in (p["name"] + " " + p["category"] + " " + p["description"]).lower()]
    cart_items, cart_total = get_cart()
    return render_template("index.html", products=filtered, categories=["All", "Electronics", "Fashion", "Accessories", "Home"],
                           selected_category=category, query=query, cart_count=sum(x["qty"] for x in cart_items))

@app.post("/add/<int:product_id>")
def add_to_cart(product_id):
    if not any(p["id"] == product_id for p in PRODUCTS):
        flash("Product nahi mila.", "error")
        return redirect(url_for("home"))
    cart = session.get("cart", {})
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session["cart"] = cart
    flash("Product cart mein add ho gaya!", "success")
    return redirect(request.referrer or url_for("home"))

@app.route("/cart")
def cart():
    items, total = get_cart()
    return render_template("cart.html", items=items, total=total, cart_count=sum(x["qty"] for x in items))

@app.post("/update-cart")
def update_cart():
    cart_data = session.get("cart", {})
    for key in list(cart_data.keys()):
        try:
            qty = int(request.form.get(f"qty_{key}", 0))
        except ValueError:
            qty = 0
        if qty <= 0:
            cart_data.pop(key, None)
        else:
            cart_data[key] = min(qty, 99)
    session["cart"] = cart_data
    flash("Cart update ho gaya.", "success")
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = get_cart()
    if not items:
        flash("Checkout se pehle cart mein product add karein.", "error")
        return redirect(url_for("home"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not email or not address:
            flash("Saari details bharna zaroori hai.", "error")
            return render_template("checkout.html", items=items, total=total, cart_count=sum(x["qty"] for x in items))
        summary = "; ".join(f'{p["name"]} x {p["qty"]}' for p in items)
        with sqlite3.connect(DB_PATH) as con:
            cur = con.execute("INSERT INTO orders (customer_name, email, address, items, total) VALUES (?, ?, ?, ?, ?)",
                              (name, email, address, summary, total))
            order_id = cur.lastrowid
        session["cart"] = {}
        return render_template("success.html", order_id=order_id, name=name, total=total, cart_count=0)
    return render_template("checkout.html", items=items, total=total, cart_count=sum(x["qty"] for x in items))

@app.route("/orders")
def orders():
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("orders.html", orders=rows, cart_count=sum(x["qty"] for x in get_cart()[0]))

@app.route("/about")
def about():
    return render_template("about.html", cart_count=sum(x["qty"] for x in get_cart()[0]))

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
