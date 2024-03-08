from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.models import User
from app.forms import RegisterForm, LoginForm
from flask_login import login_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/play")
def play_page():
    return render_template("play.html")


@app.route("/register", methods=["POST", "GET"])
def register_page():

    form = RegisterForm()

    if form.validate_on_submit():
        user_to_add = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password1.data,
        )

        db.session.add(user_to_add)
        db.session.commit()

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        # validate login details
        # check user exists
        user_to_check = User.query.filter_by(username=form.username.data).first()
        if user_to_check:
            # user exists check password match
            if user_to_check.check_password(form.password.data):
                # user and password match => login user
                print("Login successful")
                flash(f"User {user_to_check.username} logged in successfuly", "success")

                # login user
                login_user(user_to_check)

                next = request.args.get("next")

                return redirect(next or url_for("home_page"))

            else:
                # password is not correct
                flash("Password is not correct", "danger")
        else:
            # user does not exist
            flash("User does not exist", "danger")

    return render_template("login.html", form=form)
