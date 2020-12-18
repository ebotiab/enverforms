from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db, bcrypt
import flask_login
from . import model

bp = Blueprint("auth", __name__)


@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    # Check if the email is already at the database
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("Sorry, the email you provided is already registered")
        return redirect(url_for("auth.signup"))
        # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Sorry, passwords are different")
        return redirect(url_for("auth.signup"))
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash("You've successfully signed up!")
    return redirect(url_for("main.index"))


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    user = model.User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # The user exists and the password is correct
        #flash("You've successfully login!")
        flask_login.login_user(user)
        return redirect(url_for("main.index"))
    else:
        flash("Wrong email or password")
        return redirect(url_for("auth.login"))


@bp.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template("auth/login.html")