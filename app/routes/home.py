from flask import Blueprint, render_template, redirect, url_for, session

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html")

@home_bp.route("/shop-landing")
def shop_landing():
    return render_template("landing.html")

@home_bp.route("/enter-shop")
def enter_shop():
    for key in ["logs", "cart", "dark_mode", "student_discount", "international_shipping"]:
        session.pop(key, None)
    return redirect(url_for("shop.index"))