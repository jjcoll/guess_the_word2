from app import app, db
from flask import render_template
from app.models import User
from app.forms import RegisterForm


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


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


@app.route("/login")
def login_page():

    return render_template("login.html")
