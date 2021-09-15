# flask imports
from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/about")
def about():
    return render_template("about.html")