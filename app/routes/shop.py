from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os

shop_bp = Blueprint("shop", __name__, url_prefix="/shop")

with open(os.path.join(os.path.dirname(__file__), "../../data/products.json")) as f:
    products = json.load(f)

@shop_bp.app_context_processor
def inject_settings():
    return {
        "dark_mode": session.get("dark_mode", False),
        "student_discount": session.get("student_discount", False),
        "international_shipping": session.get("international_shipping", False),
        "categories": sorted(set(p["category"] for p in products))
    }

@shop_bp.route("/")
@shop_bp.route("/category/<category>")
def index(category=None):
    query = request.args.get("q", "").lower()
    filtered = [
        p for p in products
        if (query in p["name"].lower()) and (p["category"] == category if category else True)
    ]
    return render_template("shop/index.html", products=filtered, query=query, selected_category=category)

@shop_bp.route("/toggle/<setting>")
def toggle_setting(setting):
    if setting in ["dark_mode", "student_discount", "international_shipping"]:
        session[setting] = not session.get(setting, False)
    return redirect(request.referrer or url_for("shop.index"))

@shop_bp.route("/product/<int:pid>")
def product_detail(pid):
    product = next((p for p in products if p["id"] == pid), None)
    return render_template("shop/product.html", product=product)

@shop_bp.route("/add-to-cart/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    qty = int(request.form.get("quantity", 1))
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session["cart"] = cart
    return redirect(url_for("shop.cart"))

@shop_bp.route("/cart")
def cart():
    cart = session.get("cart", {})
    cart_items, total = [], 0
    for pid, qty in cart.items():
        product = next((p for p in products if p["id"] == int(pid)), None)
        if product:
            item = product.copy()
            price = item["price"]
            if session.get("student_discount"):
                price *= 0.8
            item["price"] = round(price, 2)
            item["quantity"] = qty
            item["subtotal"] = round(item["price"] * qty, 2)
            total += item["subtotal"]
            cart_items.append(item)
    if session.get("international_shipping"):
        total += 100
    return render_template("shop/cart.html", products=cart_items, total=round(total, 2))

@shop_bp.route("/update-cart", methods=["POST"])
def update_cart():
    cart = {}
    for pid, qty in request.form.items():
        qty = int(qty)
        if qty > 0:
            cart[pid] = qty
    session["cart"] = cart
    return redirect(url_for("shop.cart"))