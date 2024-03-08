from app import app, db
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from app.models import User
from app.forms import RegisterForm, LoginForm
from flask_login import login_user
from app.game_logic import start_new_game, print_board, check_board


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("index.html")


@app.route("/play")
def play_page():

    letters = "abcdefghijklmnopqrstuvwxyz"
    letters_list = list(letters)

    # Keep the previous gamemode by default
    # print(session.keys())
    # if "wordsfile" in session.keys():
    #     start_new_game(session["wordsfile"])
    # else:
    #     start_new_game("200words.txt")
    #     session["wordsfile"] = "200words.txt"

    start_new_game("countries.txt")

    return render_template(
        "play.html",
        letters_list=letters_list,
        board=print_board(session["board"]),
        lives=session["lives"],
        wordlist=session["wordsfile"],
    )


@app.route("/guess", methods=["POST"])
def guess_letter():
    # Access JSON data

    board = session["board"]
    word = session["word"]
    previous_lives = session["lives"]
    slected_letter = request.json.get("letter")

    board, lives, won = check_board(slected_letter, board, word, previous_lives)

    if lives != previous_lives:
        update_lives = True
    else:
        update_lives = False

    data_return = {
        "updatedWord": print_board(board),
        "updateLives": update_lives,
        "lives": lives,
        "won": won,
    }

    return jsonify(data_return)


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
