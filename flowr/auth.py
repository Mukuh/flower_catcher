# flask imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

# external imports
import bcrypt

# local imports
from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/sign_in", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            # https://hackernoon.com/hashing-passwords-in-python-bcrypt-tutorial-with-examples-77dh36ef
            if bcrypt.checkpw(password.encode(), user.password_hash):
                flash("Logged in!", category="success")
                # TODO: change this to a button value
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password incorrect!", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("sign_in.html", user=current_user)


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        if email != "" and username != "" and password != "" and password_confirm != "":
            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()

            if email_exists:
                flash("Email already in use.", category='error')
            elif username_exists:
                flash("Username already in use.", category='error')
            elif password != password_confirm:
                flash("Passwords do not match!", category='error')
            # TODO: add more errors here
            else:
                # https://hackernoon.com/hashing-passwords-in-python-bcrypt-tutorial-with-examples-77dh36ef
                # hash the password with a salt and just save the hased password
                password_hash = bcrypt.hashpw(
                    password=password.encode(),
                    salt=bcrypt.gensalt()
                    )
                
                # create the user
                new_user = User(
                    email = email,
                    username = username,
                    password_hash = password_hash
                )
                # store the user in the database
                db.session.add(new_user)
                db.session.commit()
                flash("new user created")
                # redirect to home
                return redirect(url_for("views.home"))
        else:
            flash("Please complete every input.")

    return render_template("sign_up.html", user=current_user)


@auth.route("/sign_out")
@login_required
def sign_out():
    logout_user()
    return redirect(url_for("views.home"))
